from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import Service_Create, ProviderUpdate_profile, User_Response, Service_Response
from app.models import User_model, Services_model
from typing import List
from app.services.admin import show_users
router = APIRouter(prefix="/admins", tags=["Admin"])

@router.get("/admin/users", response_model=User_Response.UserResponse)
def show_user(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
     return show_users(db, current_user_id)
