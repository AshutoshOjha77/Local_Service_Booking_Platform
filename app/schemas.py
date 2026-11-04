from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username : str
    password: str
    email: EmailStr
    phone: str
    role: str = "customer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class ProviderUpdateProfile(BaseModel):
    username: str
    email: EmailStr
    phone: str
    city: str


class ServiceCreate(BaseModel):
    
    title: str
    description: str | None = None
    service: str
    charge_rs: int
    city: str
    is_active: bool

class ServiceResponse(BaseModel):
    id: int
    title: str
    description: str | None
    service: str
    charge_rs: int
    city: str
    provider_id: int
    provider_name: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    service_id: int
    note: str | None=None

class BookResponse(BaseModel):
    
    id: int
    service_id: int
    customer_id : int
    customer_name: str
    provider_id: int
    provider_name: str
    status: str
    note: str | None
    booking_created: datetime

    model_config = ConfigDict(from_attributes=True)

class BookStatusUpdate(BaseModel):
    status: str