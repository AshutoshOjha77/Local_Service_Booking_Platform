from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import Service_Create, ProviderUpdate_profile, User_Response, Service_Response
from app.models import User_model, Services_model
from typing import List
from app.services.providers import show_provider_services, update_profile


router = APIRouter(prefix="/providers", tags=["Provider"])

@router.get("/provider/services/all", response_model=List[Service_Response.ServiceResponse])
def show_provider_service(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return show_provider_services(db, current_user_id)
   

@router.put("/provider/update/profile", response_model=User_Response.UserResponse)
def updated_profile(profile_update:ProviderUpdate_profile.ProviderUpdate,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return update_profile(profile_update, db, current_user_id)
