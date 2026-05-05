from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from .models import Base, AssuranceLog
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_assurance(db, record: AssuranceLog):
    """Append-only. No updates allowed."""
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_latest_status(db, account_id: str):
    return db.query(AssuranceLog).filter(AssuranceLog.account_id == account_id).order_by(desc(AssuranceLog.created_at)).first()

def get_history(db, account_id: str, limit: int = 50):
    return db.query(AssuranceLog).filter(AssuranceLog.account_id == account_id).order_by(desc(AssuranceLog.created_at)).limit(limit).all()
