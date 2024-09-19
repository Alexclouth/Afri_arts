#!/usr/bin/python3
"""Review Module for Afri-Arts Gallery Showcase project"""
from sqlalchemy import Column, String, ForeignKey, Integer
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """Review class that inherits from BaseModel and Base."""

    __tablename__ = 'reviews'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    artwork_id = Column(String(60), ForeignKey('artworks.id'), nullable=False)
    comment = Column(String(1024), nullable=True)
    likes = Column(Boolean, nullable=False, default=False)
