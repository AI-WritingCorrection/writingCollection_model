from typing import Dict, List
from pydantic import BaseModel

"""
이것은 한글 글자 연습을 위한 데이터 모델입니다.
각 글자는 획의 순서와 획의 (시점, 종점)좌표를 포함합니다.
"""

class Offset(BaseModel):
    x: float
    y: float

class Metadata(BaseModel):
    user_id: str
    practice_text: str
    cellImages: Dict[str, List[str]]  # Base64 이미지 문자열 리스트
    detailedStrokeCounts: Dict[str, List[int]] # 각 글자자에 대한 세부 획수
    firstAndLastStroke: Dict[str, List[Offset]] # 각 획에 대한 첫 번째와 마지막 획의 좌표