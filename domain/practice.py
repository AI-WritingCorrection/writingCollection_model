from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from domain.typeEnum import WritingType
from . import Base

# Practice 테이블 (자유 연습 유형 정의)
class Practice(Base):
    __tablename__ = "practices"

    practice_id = Column(Integer, primary_key=True, index=True)
    practice_text = Column(String(500), nullable=False)
    practice_type = Column(Enum(WritingType), nullable=False)
    practice_character = Column(String(100), nullable=False)
    practice_tip = Column(String(500), nullable=True, server_default="천천히 왼쪽, 오른쪽, 위, 아래 간격을 맞추면서 적어봐요")
    practice_records = relationship("PracticeRecord", back_populates="practice", cascade="all, delete-orphan")