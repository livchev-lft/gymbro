from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int