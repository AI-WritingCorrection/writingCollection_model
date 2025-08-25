from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from domain.user import User
from dto.userDTO import UserResponse
from service.userService import get_user_by_id, update_profile_pic

import os
from uuid import uuid4


router=APIRouter()

# Image upload config
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_DIR = os.getenv("STATIC_PROFILE_DIR", "/srv/writing-collection/static/profile")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL")  # e.g., https://your-domain.com

# DB에서 해당 유저의 정보를 가져오는 함수
@router.get("/getProfile/{user_id}", response_model=UserResponse)
def get_userProfile_from_db(user_id:int, db: Session = Depends(get_db)):

    try:
        records = (
            db.query(User)
              .filter(User.user_id == user_id)
              .first()
        )
        return records
    except Exception as e:
        print(f"Error fetching mission records for user {user_id}: {e}")
        return []
    
# 프로필 사진을 업데이트 하는 함수

@router.post("/uploadProfileImage/{user_id}")
async def upload_profile_image(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    request: Request = None,
):
    """
    프로필 이미지를 업로드하고 User.profile_pic(URL)을 갱신합니다.
    - multipart/form-data 로 파일을 전송해야 합니다. 필드명: 'file'
    - 허용 포맷: jpeg/png/webp, 최대 크기: 5MB
    - 저장 경로: static/profile/
    - 반환: {"data": {"profile_pic_url": "<완성 URL>"}}
    """

    # 사용자 존재 여부 확인
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # MIME 타입 확인
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    # 파일 크기 확인
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 디렉토리 준비
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 파일 저장
    ext = ALLOWED_IMAGE_TYPES[file.content_type]
    fname = f"{user_id}_{uuid4().hex}.{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(content)

    # 정적 URL 구성 (Nginx가 /static을 서빙한다고 가정)
    url_path = f"/static/profile/{fname}"
    if PUBLIC_BASE_URL:
        profile_url = f"{PUBLIC_BASE_URL.rstrip('/')}{url_path}"
    else:
        # 프록시 헤더 기반 도메인/프로토콜 추정 (uvicorn --proxy-headers 필요)
        scheme = request.headers.get("x-forwarded-proto") if request else None
        host = request.headers.get("x-forwarded-host") if request else None
        if not host and request:
            host = request.headers.get("host")
        if scheme and host:
            profile_url = f"{scheme}://{host}{url_path}"
        else:
            # 마지막 수단: 상대경로
            profile_url = url_path

    # DB 업데이트 (서비스 레이어 사용)
    try:
        updated = update_profile_pic(db, user_id, profile_url)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB commit failed")
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return {"data": {"profile_pic_url": profile_url}}