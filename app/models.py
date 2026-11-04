from database import base
from sqlalchemy import Column,String, Integer, Text, DateTime, ForeignKey, Boolean
from datetime import datetime

class User(base):
    __tablename__ = "users"

    id = Column(Integer, index= True, primary_key=True)
    username = Column(String,index=True,nullable=False, unique=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True)
    phone= Column(String,nullable=False)
    role = Column(String,default="customer")

class Services(base):
    __tablename__ = "services"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String,index=True)
    description = Column(Text, nullable=False)
    service = Column(String,index=True,nullable=False)
    charge_rs = Column(Integer,nullable=False)
    city = Column(String, nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Bookings(base):
    __tablename__ = "bookings"

    id = Column(Integer, index=True, primary_key=True)
    service_id= Column(Integer, ForeignKey("services.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_name = Column(String, nullable=False)
    status = Column(String,default="pending")
    booking_created = Column(DateTime, default=datetime.utcnow)
    note = Column(String, nullable=True)

