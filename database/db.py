# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATABASE_URL = "sqlite:///marketplace.db"

def init_db():
    """
    Creates or updates the database schema using SQLAlchemy.
    Returns a SQLAlchemy session.
    """
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

