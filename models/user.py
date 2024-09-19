#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """User class that inherits from BaseModel and Base for SQLAlchemy ORM."""

    __tablename__ = 'users'

    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    reviews = relationship('Review', backref='reviewer', lazy='True')
