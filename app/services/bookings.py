from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user_id
from app.database import get_db
from app.schemas import BookStatus_Update, Book_Response, Book_Create 
from app.models import User_model, Bookings_model, Services_model

def create_booking(db: Session, booking, current_user_id: int):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only constumer can book")
    service = db.query(Services_model.Services).filter(Services_model.Services.id == booking.service_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The service you booked isn't found")
    if service.provider_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provider cannot book services")

    book_service = Bookings_model.Bookings(
        service_id = service.id,
        customer_id = user.id,
        customer_name = user.username,
        provider_id = service.provider_id,
        provider_name = service.provider_name,
        status = "pending",
        note = booking.note
    )
    db.add(book_service)
    db.commit()
    db.refresh(book_service)

    return book_service

def provider_bookings( db: Session , current_user_id: int):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can access")
    bookings = db.query(Bookings_model.Bookings).filter(Bookings_model.Bookings.provider_id == current_user_id).all()
    return bookings


def update_status(db: Session,booking_id: int, booking_status,current_user_id: int ):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only providers can access")
    book = db.query(Bookings_model.Bookings).filter(Bookings_model.Bookings.id == booking_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if book.provider_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only the provider can update its own bookings")
    status_response = ["confirmed", "completed", "cancelled"]
    if booking_status.status not in status_response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update the status to confirmed, complete or cancelled")
    if book.status == "pending":
        if booking_status not in ["confirmed", "cancelled"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only confirmed or cancelled can be done here")
    elif book.status == "confirmed":
        if booking_status.status != "completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only completed can be done")

    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You cant update the status now becuase youu already cancelled the booking")
    book.status = booking_status.status
    db.commit()
    db.refresh(book)

    return book

def customer_bookings(db: Session , current_user_id: int):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only costumer is allowed to check their bookings")
    bookings = db.query(Bookings_model.Bookings).filter(Bookings_model.Bookings.customer_id == current_user_id).all()

    return bookings

def booking_details(db: Session, id: int , current_user_id: int):
    user = db.query(User_model.User).filter(User_model.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    book = db.query(Bookings_model.Bookings).filter(Bookings_model.Bookings.id == id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking id is invalid")
    if book.customer_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer id is invalid")

    return book
