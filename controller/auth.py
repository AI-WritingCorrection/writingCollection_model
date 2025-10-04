import os
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from dto.authDTO import AuthResponse
from dto.userDTO import UserCreate
from service.userService import create_user, get_user_by_firebase_uid
from firebase import verify_firebase_token
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4

# JWT 설정
# 클라이언트와 서버 간에 인증·인가 정보를 안전하게 주고받기 위해 쓰이는 간단한 토큰 형식
# 서버가 별도 세션 저장소(세션 DB/Redis 등) 없이도 “누가 요청했는지” 검증할 수 있습니다.

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", 60))



router = APIRouter()

# 이미지 업로드 설정 (회원가입 멀티파트용)
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",     # 일부 클라이언트가 image/jpg 로 보냄
    "image/pjpeg": "jpg",   # progressive jpeg
    "image/png": "png",
    "image/webp": "webp",
}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_DIR = os.getenv("STATIC_PROFILE_DIR", "/app/static/profile")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL")  # 예: https://your-domain.com

class TokenPayload(BaseModel):
    id_token: str

@router.post("/login", response_model=AuthResponse)
def login(payload: TokenPayload, db: Session = Depends(get_db)):
    #print("received payload:", payload)
    # 1) Firebase ID 토큰 검증
    decoded = verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    uid = decoded["uid"]

    # 2) 기존 사용자 조회
    user = get_user_by_firebase_uid(db, uid)
    
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    
    # 3) 로그인 성공: JWT 발급 후 사용자 정보 + 토큰 반환
    new_jwt = create_jwt_token(user.firebase_uid)
    return AuthResponse(
        user_id=user.user_id,
        firebase_uid=user.firebase_uid,
        provider=user.provider,
        email=user.email,
        nickname=user.nickname,
        birthdate=user.birthdate,
        profile_pic=user.profile_pic,
        jwt=new_jwt
    )

@router.post("/signup", response_model=AuthResponse)
async def signup(
    payload: UserCreate = Depends(UserCreate.as_form),
    file: UploadFile | None = File(None),  # 선택적 프로필 이미지 파일
    db: Session = Depends(get_db),
    request: Request = None,
):
    # 1) Firebase 토큰 검증
    decoded = verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    uid = decoded["uid"]

    # 2) 중복 가입 확인
    existing = get_user_by_firebase_uid(db, uid)
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 계정입니다.")

    # 3) 선택적 프로필 이미지 처리
    profile_url = None
    if file is not None:
        # 디버그: 들어온 content_type/파일명 확인
        print(f"[SIGNUP UPLOAD] uid={uid}, content_type={file.content_type}, filename={file.filename}")

        # 확장자 결정: MIME 우선, 실패 시 파일명 확장자 폴백
        mime = (file.content_type or "").lower()
        if mime in ALLOWED_IMAGE_TYPES:
            ext = ALLOWED_IMAGE_TYPES[mime]
        else:
            name = (file.filename or "").lower()
            if name.endswith((".jpg", ".jpeg")):
                ext = "jpg"
            elif name.endswith(".png"):
                ext = "png"
            elif name.endswith(".webp"):
                ext = "webp"
            else:
                raise HTTPException(status_code=415, detail="Unsupported media type")

        content = await file.read()
        if len(content) > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        fname = f"{uid}_{uuid4().hex}.{ext}"
        fpath = os.path.join(UPLOAD_DIR, fname)
        with open(fpath, "wb") as f:
            f.write(content)

        url_path = f"/static/profile/{fname}"
        if PUBLIC_BASE_URL:
            profile_url = f"{PUBLIC_BASE_URL.rstrip('/')}" + url_path
        else:
            scheme = request.headers.get("x-forwarded-proto") if request else None
            host = request.headers.get("x-forwarded-host") if request else None
            if not host and request:
                host = request.headers.get("host")
            if scheme and host:
                profile_url = f"{scheme}://{host}{url_path}"
            else:
                profile_url = url_path

    # 4) 사용자 생성
    new_user = create_user(
        db,
        firebase_uid=uid,
        provider=payload.provider,
        email=payload.email,
        nickname=payload.nickname,
        birthdate=payload.birthdate,
        profile_pic=profile_url,
    )

    # 5) JWT 발급 및 응답
    new_jwt = create_jwt_token(new_user.firebase_uid)
    return AuthResponse(
        user_id=new_user.user_id,
        firebase_uid=new_user.firebase_uid,
        provider=new_user.provider,
        email=new_user.email,
        nickname=new_user.nickname,
        birthdate=new_user.birthdate,
        profile_pic=new_user.profile_pic,
        jwt=new_jwt
    )

@router.post("/logout")
async def logout(authorization: str = Header(...)):
    try:
        token = authorization.split("Bearer ")[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = decoded.get("sub")
        print(f"Logging out user: {uid}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Logged out successfully"}

def create_jwt_token(firebase_uid: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": firebase_uid, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
