# models.py
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    # We'll store `preferences` as JSON in a TEXT field in SQLite
    preferences = Column(Text, nullable=True)

    # Relationship to ContactedSeller
    contacted_sellers = relationship("ContactedSeller", back_populates="user")

class ContactedSeller(Base):
    __tablename__ = 'contacted_sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Basic info about the vehicle
    make_model = Column(String, nullable=True)
    seller_info = Column(Text, nullable=True)
    # Store messages as JSON in a TEXT field
    seller_messages_json = Column(Text, nullable=True)
    # Optionally store additional data
    kbb_data_json = Column(Text, nullable=True)

    user = relationship("User", back_populates="contacted_sellers")
