from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import setting

engine = create_engine(setting.DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)
base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

