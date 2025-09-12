from pydantic import BaseModel
from typing import Dict, List, Optional

class Offset(BaseModel):
    x: float
    y: float

# Result 요청용 DTO(채점 요청을 위해 받는 데이터)
class ResultCreate(BaseModel):
    user_id: int
    step_id: int
    practice_text: str
    cell_images: Dict[str, List[str]]  # Base64 이미지 문자열 리스트
    detailed_strokecounts: Dict[str, List[int]] # 각 글자자에 대한 세부 획수
    firstandlast_stroke: Dict[str, List[Offset]] # 각 획에 대한 첫 번째와 마지막 획의 좌표

# Result 응답용 DTO(기존 사용 모델 || 구식모델)
class ResultResponse(BaseModel):
    score: int
    summary: str
    #recognized_texts : Dict[int,str]
    class Config:
        orm_mode = True



# Result 응답용 DTO - 글자별 상세 결과
class CharacterResult(BaseModel):
    original_text: str
    recognized_text: str
    score: int
    stage: str
    feedback: List[Optional[str]]


#  Result 응답용 DTO (최종 응답으로 사용할 메인 모델)
class ResultResponse(BaseModel):
    avg_score: float
    summary: List[str]
    feedback: List[List[Optional[str]]]
    results: List[CharacterResult] 
