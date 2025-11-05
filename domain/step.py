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
    step_character = Column(String(100), nullable=False)
    step_text = Column(String(500), nullable=False)
    step_time = Column(Integer, nullable=True, default=120)
    step_tip = Column(String(500), nullable=True, server_default="천천히 왼쪽, 오른쪽, 위, 아래 간격을 맞추면서 적어봐요")
    mission_records = relationship("MissionRecord", back_populates="step", cascade="all, delete-orphan")    
    