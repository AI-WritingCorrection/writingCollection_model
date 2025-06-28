from pydantic import BaseModel

from domain.typeEnum import WritingType

class StepSchema(BaseModel):
    step_id: int
    step_mission: str
    step_type: WritingType
    step_character: str
    step_text: str
    step_time: int

    model_config = { "from_attributes": True }  # orm_mode 대체