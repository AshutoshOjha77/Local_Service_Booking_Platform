from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import Service_Create, ProviderUpdate_profile, User_Response, Service_Response
from app.models import User_model, Services_model
from typing import List
from app.services.providers import show_provider_services, update_profile

def show_users(db: Session , current_user_id: int):
     user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
     if user is None:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
     if user.role != "admin":
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can access")
     users = db.query(User_model.User).all()
     return users