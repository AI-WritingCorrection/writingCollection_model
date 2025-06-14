from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from domain.typeEnum import AuthProvider

# User 관련 dto들

#User 가입할 때 DTO
class UserCreate(BaseModel):
    firebase_uid: str
    email: str
    nickname: str
    profile_pic: Optional[str]
    birthdate: datetime
    provider: AuthProvider

# User 응답용 DTO(ex. 마이페이지)
class UserResponse(BaseModel):
    user_id: int
    firebase_uid: str
    email: str
    nickname: str
    profile_pic: Optional[str]
    birthdate: datetime
    provider: AuthProvider
    
    class Config:
        orm_mode = True






