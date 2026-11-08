from pydantic import BaseModel, EmailStr, ConfigDict

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
