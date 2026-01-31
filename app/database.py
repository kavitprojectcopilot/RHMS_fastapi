from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:kavit@localhost:5432/RHMS"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:SwrCmWxTLUmabDsywSRqxfnFONvMUEWD@postgres.railway.internal:5432/railway"
                          
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()