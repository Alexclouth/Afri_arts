#!/usr/bin/python3
"""Order Module for Afri-Arts Gallery Showcase project"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base

class Order(BaseModel, Base):
    """Order class that represents an order placed by a user."""

    __tablename__ = 'orders'

    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    artwork_id = Column(String(60), ForeignKey('artworks.id'), nullable=False)
    status = Column(String(128), nullable=False)
