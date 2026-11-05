from fastapi import HTTPException, Cookie, Query, status, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import security
from sqlalchemy.orm import Session
import models
from database import get_db
from config import setting
import schemas


router = APIRouter()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user_id(
    token: str = Depends(oauth_scheme)) -> int:
    payload = await security.verify_token(token, expected_token="access") 
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user id not found"
        )

    return int(user_id)  

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: schemas.UserCreate, db: Session=Depends(get_db)):
    username_clean = user_data.username.strip().lower()
    email_clean = user_data.email.strip().lower()
    phone_clean = user_data.phone.strip()

    if db.query(models.User).filter(models.User.username == username_clean).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The username already exists")
    if db.query(models.User).filter(models.User.email == email_clean).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account is already created from this email")
    if db.query(models.User).filter(models.User.phone == phone_clean).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists from this phone number")

    new_user = models.User(
        username = username_clean,
        email = email_clean,
        phone = phone_clean,
        hashed_password= security.hash_password(user_data.password),
        role= user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":f"Your account has been created, {username_clean}"}

@router.post("/login")
def login_user(payload: schemas.UserLogin, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not security.verify_password(payload.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token_data = {
        "sub": str(user.id),
        "role": user.role,
        "username": user.username
    }

    access_token = security.create_access_tokens(token_data)
    refresh_token = security.create_refresh_tokens(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user":{
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }


@router.post("/refresh")
async def refresh_access_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    refresh_token = authorization.split(" ")[1]
    payload = await security.verify_token(refresh_token, expected_token="refresh")

    new_access_token = security.create_refresh_tokens({
        "sub": payload["sub"],
        "role": payload.get("role"),
        "username": payload.get("username")
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    await security.verify_token(token, expected_token="access")
    await security.blacklist_tokens(token)
    return {"message": "You successfully logged out"}

@router.get("/profile/me")
def user_profile(db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return{
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role
    }
