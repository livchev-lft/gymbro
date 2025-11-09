from pydantic import BaseModel

class HintResponse(BaseModel):
    user_id: int
    section: str