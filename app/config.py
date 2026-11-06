import os 
class Setting:
    SECRET_KEY: str = os.getenv("SECRET_KEY","c641bf1d0b0d36ec0344bcf886d8d65da54d1413f6c75ad1011cf23f09b430f8")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ELASTICSEARCH_URL: str =   os.getenv(
    "ELASTICSEARCH_URL",
    "http://localhost:9200"
)
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5434/local_services_db"

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    
setting = Setting()

    