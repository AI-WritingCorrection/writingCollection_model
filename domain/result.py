from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

# Result 테이블 (채점 결과 저장)
class Result(Base):
    __tablename__ = "results"

    result_id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("mission_records.mission_id"), nullable=False)
    score = Column(Integer, nullable=True)

    mission_record = relationship("MissionRecord", back_populates="result")