from pydantic import BaseModel, ConfigDict

class MissionRecordSchema(BaseModel):
    step_id: int
    user_id: int
    isCleared: bool

    model_config = ConfigDict(from_attributes=True)