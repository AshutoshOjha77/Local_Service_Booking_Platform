import jwt
from app.config import setting
from fastapi import HTTPException, status
import bcrypt
from datetime import datetime,timedelta,timezone
from app.redis_client import get_redis

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_tokens(data: dict)->str:
    payload = data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp":expire, "type":"access"})
    return jwt.encode(payload,setting.SECRET_KEY, algorithm=setting.ALGORITHM)

def create_refresh_tokens(data: dict)-> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS)
    payload.update({"exp":expire,"type":"refresh"})
    return jwt.encode(payload, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

async def blacklist_token(token: str, expired_time: int = 60 * 60 * 24 * 7) -> None:
    r = get_redis()
    await r.setex(f"blacklist:{token}", expired_time, "1")


async def is_blacklist_token(token: str) -> bool:
    r = get_redis()
    value = await r.get(f"blacklist:{token}")
    return value is not None


async def verify_token(token: str, expected_type: str) -> dict:
    if await is_blacklist_token(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(
            token,
            setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM]
        )
        if payload.get("type") != expected_type:
            raise HTTPException(status_code=401, detail="Token is invalid")
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")