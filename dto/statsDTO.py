from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from domain.typeEnum import WritingType

class StatsResponse(BaseModel):
    """
    차트 생성을 위한 개별 미션 수행 기록 DTO
    (MissionRecord + Result + Step 정보 조합)
    """
    mission_id: int
    step_type: WritingType  
    
    score: float  # 채점 결과 (Result.score)
    isCleared: bool       # 클리어 여부 (MissionRecord.isCleared)
    submission_time: datetime  # 제출 시간 (MissionRecord.submission_time)

    model_config = ConfigDict(from_attributes=True)