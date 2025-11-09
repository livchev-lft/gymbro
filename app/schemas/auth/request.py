from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: int


class RefreshRequest(BaseModel):
    session_id: str
    refresh_token: str