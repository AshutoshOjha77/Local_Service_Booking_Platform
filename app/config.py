import os 
class setting:
    SECRET_KEY: str = os.getenv("SECRET_KEY","super-secret-key-for-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_URL: str = os.getenv("REDIS_URL","https://localhost://6379:0/")
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL","https://localhost://9200")
    

    