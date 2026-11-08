from app.database import base
from sqlalchemy import Column,String, Integer, DateTime, ForeignKey
from datetime import datetime

class Bookings(base):
    __tablename__ = "bookings"

    id = Column(Integer, index=True, primary_key=True)
    service_id= Column(Integer, ForeignKey("services.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_name = Column(String, nullable=False)
    status = Column(String,default="pending", nullable= False)
    booking_created = Column(DateTime, default=datetime.utcnow)
    note = Column(String, nullable=True)