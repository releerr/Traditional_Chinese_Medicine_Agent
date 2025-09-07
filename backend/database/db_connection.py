from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings
from backend.database.db_models import Base 

#create database engine
db_engine = create_engine(settings.DATABASE_URL, echo=True,future=True)

# 创建所有表
Base.metadata.create_all(bind=db_engine)

#create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


#create session, session to fastAPI, then close session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
