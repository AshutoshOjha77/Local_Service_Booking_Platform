from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.User_Create import UserCreate 
from app.models import User_model
from app.security import hash_password, verify_password, create_access_tokens, create_refresh_tokens, verify_token, blacklist_token


def register_user(db: Session, user_data):
    username = user_data.username.strip().lower()
    email = user_data.email.strip().lower()
    phone = user_data.phone.strip()
    role = user_data.role.strip().lower()

    if role not in ["customer", "provider"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only be customer or provider")
    if db.query(User_model.User).filter(User_model.User.username == username).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The username already exists")
    if db.query(User_model.User).filter(User_model.User.email == email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account is already created from this email")
    if db.query(User_model.User).filter(User_model.User.phone == phone).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists from this phone number")
    
    new_user = User_model.User(
            username = username,
            email = email,
            phone = phone,
            hashed_password= hash_password(user_data.password),
            role= role
        )
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(payload, db: Session):
    user = db.query(User_model.User).filter(User_model.User.username == payload.username.lower().strip()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token_data = {
        "sub": str(user.id),
        "role": user.role,
        "username": user.username
    }

    access_token = create_access_tokens(token_data)
    refresh_token = create_refresh_tokens(token_data)

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

async def refresh_access_token(refresh_token: str ):
    payload = await verify_token(refresh_token, expected_type="refresh")

    new_access_token = create_refresh_tokens({
        "sub": payload["sub"],
        "role": payload.get("role"),
        "username": payload.get("username")
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

async def logout_user(access_token: str):
    
    await verify_token(access_token, expected_type="access")
    await blacklist_token(access_token)
    return {"message": "You successfully logged out"}

def user_profile(db: Session , current_id: int ):
    user = db.query(User_model.User).filter(User_model.User.id == current_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return{
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role
    }