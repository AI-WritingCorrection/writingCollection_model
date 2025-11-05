from typing import Optional
from pydantic import BaseModel, ConfigDict
from domain.typeEnum import WritingType


class PracticeSchema(BaseModel):
    practice_id: int
    practice_text: str
    practice_type: WritingType
    practice_character: str
    practice_tip: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
