from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

# PracticeRecord 테이블 (유저별 자유 연습 기록)
class PracticeRecord(Base):
    __tablename__ = "practice_records"

    practiceRecord_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    practice_id = Column(Integer, ForeignKey("practices.practice_id"), nullable=False)
    practice_time = Column(DateTime(timezone=True), nullable=True, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="practice_records")
    practice = relationship("Practice", back_populates="practice_records")