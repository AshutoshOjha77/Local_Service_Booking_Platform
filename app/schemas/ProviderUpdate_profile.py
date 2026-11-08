from pydantic import BaseModel, EmailStr

class ProviderUpdate(BaseModel):
    username: str
    email: EmailStr
    phone: str
    city: str

    