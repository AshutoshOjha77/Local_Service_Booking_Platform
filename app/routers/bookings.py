from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.schemas import Book_Create, Book_Response, BookStatus_Update
from app.models import User_model, Bookings_model, Services_model
from app.services.bookings import create_booking, provider_bookings, update_status, customer_bookings, booking_details

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/create/booking", response_model=Book_Response.BookResponse, status_code=status.HTTP_201_CREATED)
def creating_booking(booking:Book_Create.BookCreate ,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return create_booking(db, booking, current_user_id)

@router.get("/provider/bookings", response_model=Book_Response.BookResponse)
def see_provider_bookings( db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return provider_bookings(db, current_user_id)

@router.put("/provider/booking/status/{booking_id}")
def updated_status(booking_id: int, booking_status:BookStatus_Update.BookStatusUpdate , db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
   return update_status(db,booking_id, booking_status, current_user_id)

@router.get("/costumer/bookings", response_model=Book_Response.BookResponse)
def customer_booking(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return customer_bookings(db, current_user_id)

@router.get("/booking/details/{id}", response_model=Book_Response.BookResponse)
def booking_detail(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return booking_details(db, id, current_user_id )



    