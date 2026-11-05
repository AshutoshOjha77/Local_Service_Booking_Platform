from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from typing import List
from app import  schemas
from app.routers.auth import get_current_user_id


router = APIRouter(prefix="/providers", tags=["Provider"])

@router.get("/provider/services/all", response_model=List[schemas.ServiceResponse])
def show_provider_services(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):

    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "providers":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can check their services")
    services = db.query(models.Services).filter(models.Services.provider_id == current_user_id).all()
    return services

@router.put("/provider/update/profile", response_model=schemas.UserResponse)
def update_profile(profile_update:schemas.ProviderUpdateProfile,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can access it")
    


    
    user.username = profile_update.username,
    user.email = profile_update.email,
    user.phone = profile_update.phone,
    schemas.ServiceCreate.city = profile_update.city
    db.commit()
    db.refresh(user)

    return user
