from fastapi import HTTPException, Cookie, Query, status, APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from app.security import verify_token, blacklist_token
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import setting
from app.schemas import User_Login, User_Create
from app.services.auth import register_user, login_user, refresh_access_token, logout_user, user_profile



router = APIRouter(prefix="/authenticate", tags=["Authetication"])
oauth_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_scheme)
) -> int:
    token = credentials.credentials
    payload = await verify_token(token, expected_type="access")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: User_Create.UserCreate , db: Session=Depends(get_db)):
    new_user = register_user(db, user_data)
    return {
        "message": f"Your account has been created, {new_user.username}",
        "user_id": new_user.id
    }

@router.post("/login")
def login(payload: User_Login.UserLogin, db: Session= Depends(get_db)):
    return login_user(db, payload)



@router.post("/refresh")
async def refresh_access(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    refresh_token = authorization.split(" ")[1]
    return await refresh_access_token(refresh_token)

@router.post("/logout")
async def logout(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    return logout_user(token)

@router.get("/profile/me")
def see_profile(db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)):
    return user_profile(db, current_id)


