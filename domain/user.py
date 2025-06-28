from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from domain.typeEnum import AuthProvider
from . import Base
from domain.practiceRecord import PracticeRecord
from domain.missionRecord import MissionRecord

class User(Base):
    __tablename__ = "users"

    #user_id → 내부 DB 조인/성능 최적화용 정수 PK
    user_id = Column(Integer, primary_key=True, index=True)
    #firebase_uid → 외부 인증(ID 토큰 검증 시 사용)
    firebase_uid = Column(String(100), unique=True, nullable=False)
    provider = Column(Enum(AuthProvider), nullable=False)  # AuthProvider Enum 사용

    email = Column(String(255), unique=True, nullable=False)
    nickname= Column(String(10), nullable=False)
    profile_pic= Column(String(500), nullable=True)
    birthdate= Column(DateTime, nullable=False)

    # 두 테이블 간 양방향 관계를 설정
    mission_records= relationship("MissionRecord", back_populates="user", cascade="all, delete-orphan")
    practice_records= relationship("PracticeRecord", back_populates="user", cascade="all, delete-orphan")