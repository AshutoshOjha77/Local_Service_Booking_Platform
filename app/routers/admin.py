from fastapi import HTTPException, status, Depends, APIRouter
from database import get_db
from sqlalchemy.orm import Session
import schemas
from auth import get_current_user_id
import models

router = APIRouter(prefix="/admins", tags=["Admin"])

@router.get("/admin/users", response_model=schemas.UserResponse)
def show_users(db: Session = Depends(get_db), current_user_id: int = Depends(get_db)):
     user = db.query(models.User).filter(models.User.id == current_user_id).first()
     if user is None:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
     if user.role != "admin":
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can access")
     users = db.query(models.User).all()
     return users
