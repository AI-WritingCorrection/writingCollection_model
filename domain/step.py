from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from domain.typeEnum import WritingType
from . import Base

# Step 테이블 (공통 스텝 정의)
class Step(Base):
    __tablename__ = "steps"

    step_id = Column(Integer, primary_key=True, index=True)
    step_mission = Column(String(500), nullable=False)
    step_type = Column(Enum(WritingType), nullable=False)
    step_charcter = Column(String(10), nullable=False)
    step_text = Column(String(500), nullable=False)
    step_time = Column(Integer, nullable=True, default=120)

    mission_records = relationship("MissionRecord", back_populates="step", cascade="all, delete-orphan")    