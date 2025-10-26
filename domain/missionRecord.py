from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import Base

# Mission_Record 테이블 (유저별 스텝 수행 기록)
class MissionRecord(Base):
    __tablename__ = "mission_records"

    mission_id = Column(Integer, primary_key=True, index=True)
    step_id = Column(Integer, ForeignKey("steps.step_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    isCleared = Column(Boolean, nullable=False, default=False)
    submission_time = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="mission_records")
    step = relationship("Step", back_populates="mission_records")
    result = relationship(
        "Result", uselist=False, back_populates="mission_record", cascade="all, delete-orphan"
    )