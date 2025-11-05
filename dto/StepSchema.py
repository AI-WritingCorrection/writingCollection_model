from pydantic import BaseModel, ConfigDict

from domain.typeEnum import WritingType

class StepSchema(BaseModel):
    step_id: int
    step_mission: str
    step_type: WritingType
    step_character: str
    step_text: str
    step_time: int
    step_tip: str
    model_config = ConfigDict(from_attributes=True)