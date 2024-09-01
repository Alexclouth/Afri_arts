#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class User(BaseModel, Base):
    """User class that inherits from BaseModel and Base for SQLAlchemy ORM."""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    profile_picture = Column(String(256), nullable=True)
    orders = relationship('Order', backref='user', cascade='delete')
    reviews = relationship('Review', backref='user', cascade='delete')
