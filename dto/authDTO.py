from pydantic import BaseModel
from domain.typeEnum import UserType
from dto.userDTO import UserResponse


class AuthResponse(UserResponse):
    jwt: str

class LoginResponse(BaseModel):
    user_id: int
    firebase_uid: str
    jwt: str
    email: str
    user_type: UserType
    