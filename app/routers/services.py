from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import Service_Create, Service_Response 
from app.models import User_model, Bookings_model, Services_model
from app.services.services import add_services, show_all_services, search_services, get_service, update_services, delete_service
from typing import List
import json

router = APIRouter(prefix="/Services", tags=["Services"])

@router.post("/add/services", response_model=Service_Response.ServiceResponse, status_code=status.HTTP_201_CREATED)
async def adding_services(payload: Service_Create.ServiceCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
   return add_services(payload, db, current_user_id)

@router.get("/see/all/services", response_model=List[Service_Response.ServiceResponse])
async def see_all_services(db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
   return show_all_services(db, current_user_id)

@router.get("/search")
async def search_service(q: str):
    return search_services(q)
    
@router.get("/service/{id}", response_model=Service_Response.ServiceResponse)
def get_services(id: int, db : Session = Depends(get_db), current_user_id:int = Depends(get_current_user_id)):
    return get_service(id, db, current_user_id)

@router.put("/services/update/{id}", response_model=Service_Response.ServiceResponse)
async def update_service(payload: Service_Create.ServiceCreate ,id: int, db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)):
    return update_services(payload, id, db, current_id)

@router.delete("/services/delete/{id}")
async def delete_services(service_delete_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return delete_service(service_delete_id, db, current_user_id)
