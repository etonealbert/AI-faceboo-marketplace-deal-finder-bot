from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///database/marketplace.db"

# Create the database engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
def init_db():
    """
    Creates or updates the database schema using SQLAlchemy.
    """
    logger.info(f"Smth happend")

#    Base.metadata.create_all(bind=engine)

