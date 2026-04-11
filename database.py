from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/codit"
engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()