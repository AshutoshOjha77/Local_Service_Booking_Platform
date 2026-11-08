from app.database import base
from sqlalchemy import Column,String, Integer, Text, ForeignKey, Boolean

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