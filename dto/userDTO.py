from fastapi import Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from domain.typeEnum import AuthProvider

# User 관련 dto들

#User 가입할 때 DTO
# class UserCreate(BaseModel):
#     id_token: str
#     # firebase_uid: str
#     email: str
#     nickname: str
#     profile_pic: Optional[str]
#     birthdate: datetime
#     provider: AuthProvider

class UserCreate(BaseModel):
    id_token: str
    email: str
    nickname: str
    profile_pic: Optional[str] = None
    birthdate: datetime
    provider: AuthProvider

    @classmethod
    def as_form(
        cls,
        id_token: str = Form(...),
        email: str = Form(...),
        nickname: str = Form(...),
        birthdate: datetime = Form(...),
        provider: AuthProvider = Form(...),
        profile_pic: Optional[str] = Form(None),
    ):
        return cls(
            id_token=id_token,
            email=email,
            nickname=nickname,
            birthdate=birthdate,
            provider=provider,
            profile_pic=profile_pic,
        )

# User 응답용 DTO(ex. 마이페이지)
class UserResponse(BaseModel):
    user_id: int
    email: str
    nickname: str
    profile_pic: Optional[str]
    
    class Config:
        from_attributes = True






