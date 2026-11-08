from pydantic import BaseModel

class ServiceCreate(BaseModel):
    
    title: str
    description: str | None = None
    service: str
    charge_rs: int
    city: str
    is_active: bool