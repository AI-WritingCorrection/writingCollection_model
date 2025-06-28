from pydantic import BaseModel
from datetime import datetime

class MissionRecordSchema(BaseModel):
    step_id: int
    user_id: int
    isCleared: bool

    model_config = {
        "from_attributes": True
    }