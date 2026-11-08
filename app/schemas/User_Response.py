from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    role: str

    model_config = ConfigDict(from_attributes=True)


