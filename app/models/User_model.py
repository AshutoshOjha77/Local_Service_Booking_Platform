from app.database import base
from sqlalchemy import Column,String, Integer


class User(base):
    __tablename__ = "users"

    id = Column(Integer, index= True, primary_key=True)
    username = Column(String,index=True,nullable=False, unique=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True)
    phone= Column(String,nullable=False)
    role = Column(String,default="customer")