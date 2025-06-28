from pydantic import BaseModel

from domain.typeEnum import WritingType


class PracticeSchema(BaseModel):
    practice_id: int
    practice_text: str
    practice_type: WritingType
    practice_character: str

    model_config = { "from_attributes": True }  
