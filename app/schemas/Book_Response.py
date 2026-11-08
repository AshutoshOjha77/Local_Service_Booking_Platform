from pydantic import BaseModel, ConfigDict
from datetime import datetime

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