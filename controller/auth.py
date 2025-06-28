import os
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from dto.authDTO import AuthResponse
from dto.userDTO import UserCreate
from service.userService import create_user, get_user_by_firebase_uid
from firebase import verify_firebase_token
import jwt
from datetime import datetime, timedelta, timezone

# JWT 설정
# 클라이언트와 서버 간에 인증·인가 정보를 안전하게 주고받기 위해 쓰이는 간단한 토큰 형식
# 서버가 별도 세션 저장소(세션 DB/Redis 등) 없이도 “누가 요청했는지” 검증할 수 있습니다.

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES"))


router = APIRouter()

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
def signup(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    print("received payload:", payload)

    # UserCreate에 들어온 데이터를 바탕으로 firebase OAuth로 신규회원을 생성
    # 하면서 firebase_uid를 발급받고, JWT 토큰을 생성하여 반환합니다.

    # 1) 토큰 검증
    decoded = verify_firebase_token(payload.id_token)
    if not decoded:
        raise HTTPException(401, "유효하지 않은 토큰입니다.")
    uid = decoded["uid"]
    existing = get_user_by_firebase_uid(db, uid)
    if existing:
        raise HTTPException(400, "이미 가입된 계정입니다.")

    new_user = create_user(
       db,
       firebase_uid=uid,
       provider=payload.provider,
       email=payload.email,
       nickname=payload.nickname,
       birthdate=payload.birthdate,
       profile_pic=payload.profile_pic,
   )

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
