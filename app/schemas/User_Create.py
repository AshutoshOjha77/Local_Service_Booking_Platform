from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str
    role: str = "customer"
    @field_validator("role")
    @classmethod
    def validate(cls, v: str) -> str:
        allowed = {"customer", "provider"}
        v = v.strip().lower()
        if v  not in allowed:
            raise ValueError("Role must be either 'provider' or 'customer'")
        return v
