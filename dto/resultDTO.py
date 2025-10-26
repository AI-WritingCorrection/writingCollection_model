from pydantic import BaseModel, ConfigDict
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

# Result 응답용 DTO - 글자별 상세 결과
class CharacterResult(BaseModel):
    original_text: str
    score: int
    stage: str
    feedback: List[Optional[str]]
    recognized_text: str
    stage2_debug_state: Optional[str] = None  # 2차 스테이지 디버그 정보 (없을 수도 있음)
    stage3_debug_state: Optional[str] = None  # 3차 스테이지 디버그 정보 (없을 수도 있음)
    stage4_debug_state: Optional[str] = None  # 4차 스테이지 디버그 정보 (없을 수도 있음)


#  Result 응답용 DTO (최종 응답으로 사용할 메인 모델)
class ResultResponse(BaseModel):
    avg_score: float
    summary: List[str]
    feedback: List[List[Optional[str]]]
    results: List[CharacterResult] 
    model_config = ConfigDict(from_attributes=True)