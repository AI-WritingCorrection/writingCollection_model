from pydantic import BaseModel
from typing import Dict, List

class Offset(BaseModel):
    x: float
    y: float

# Result 요청용 DTO(채점 요청을 위해 받는 데이터)
class ResultCreate(BaseModel):
    user_id: str
    practice_text: str
    cellImages: Dict[str, List[str]]  # Base64 이미지 문자열 리스트
    detailedStrokeCounts: Dict[str, List[int]] # 각 글자자에 대한 세부 획수
    firstAndLastStroke: Dict[str, List[Offset]] # 각 획에 대한 첫 번째와 마지막 획의 좌표

# Result 응답용 DTO(채점 결과를 반환하기 위한 데이터)
class ResultResponse(BaseModel):
    result_id: int
    mission_id: int
    score: int
    summary: str

    class Config:
        orm_mode = True