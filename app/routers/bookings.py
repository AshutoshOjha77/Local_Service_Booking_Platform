from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from sqlalchemy.orm import Session
from auth import get_current_user_id
import models
import redis_client
import elasticsearch_client
import schemas

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/create/booking", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking:schemas.BookCreate ,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "constumer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only constumer ")
    service = db.query(models.Services).filter(models.Services.id == booking.service_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The service you booked isn't found")
    if service.provider_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provider cannot book services")

    book_service = models.Bookings(
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

@router.get("/provider/bookings", response_model=schemas.BookResponse)
def provider_bookings( db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only provider can access")
    bookings = db.query(models.Bookings).filter(models.Bookings.id == current_user_id).all()
    return bookings

@router.put("/provider/booking/status/{booking_id}")
def update_status(booking_id: int, booking_status:schemas.BookStatusUpdate ,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only providers can access")
    book = db.query(models.Bookings).filter(models.Bookings.id == booking_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if book.provider_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only the provider can update its own bookings")
    status_response = ["confirmed", "complete", "cancelled"]
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

@router.get("/costumer/bookings", response_model=schemas.BookResponse)
def constumer_bookings(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "costumer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only costumer is allowed to check their bookings")
    bookings = db.query(models.Bookings).filter(models.Bookings.customer_id == current_user_id).all()

    return bookings

@router.get("/booking/details/{id}", response_model=schemas.BookResponse)
def booking_details(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    book = db.query(models.Bookings).filter(models.Bookings.id == id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking id is invalid")
    if book.customer_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer id is invalid")

    return book




    