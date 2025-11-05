import enum

class WritingType(str, enum.Enum):
    PHONEME = "PHONEME"
    WORD = "WORD"
    SENTENCE = "SENTENCE"
    FREE = "FREE"

class AuthProvider(str, enum.Enum):
    GOOGLE = "GOOGLE"
    KAKAO = "KAKAO"
    NAVER = "NAVER"
    APPLE = "APPLE"

class UserType(str, enum.Enum):
    CHILD = "CHILD"
    ADULT = "ADULT"
    FOREIGN = "FOREIGN"