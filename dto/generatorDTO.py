from pydantic import BaseModel

class TextRequest(BaseModel):
    form: str
    length: int
    con: str

