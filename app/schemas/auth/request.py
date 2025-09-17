from pydantic import BaseModel, constr
from datetime import date
from app.models.enum_models import Gender, Goal, Experience

class LoginRequest(BaseModel):
    user_id: int


class RefreshRequest(BaseModel):
    session_id: str
    refresh_token: str

class RegisterRequest(BaseModel):
    user_id: int
    username: str | None = None
    gender: Gender
    birthdate: date
    height: int
    goal: Goal
    experience: Experience