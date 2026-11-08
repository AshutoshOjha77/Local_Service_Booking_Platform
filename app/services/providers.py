from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import Service_Create
from app.models import User_model, Services_model

def show_provider_services(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):

    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "providers":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can check their services")
    services = db.query(Services_model.Services).filter(Services_model.Services.provider_id == current_user_id).all()
    return services

def update_profile(profile_update,db: Session , current_user_id: int ):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can access it")
    


    
    user.username = profile_update.username,
    user.email = profile_update.email,
    user.phone = profile_update.phone,
    Service_Create.ServiceCreate.city = profile_update.city
    db.commit()
    db.refresh(user)

    return user