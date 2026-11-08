from pydantic import BaseModel, EmailStr

class BookCreate(BaseModel):
    service_id: int
    note: str | None = None