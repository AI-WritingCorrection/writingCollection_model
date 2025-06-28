from dto.userDTO import UserResponse


class AuthResponse(UserResponse):
    jwt: str