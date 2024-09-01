#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Artwork(BaseModel, Base):
    """Represents an artwork for the Afri-Arts Gallery Showcase."""

    __tablename__ = 'artwork'

    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    image_url = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    art_type = Column(String(128), nullable=False)
    style = Column(String(128), nullable=False)
    available = Column(Boolean, default=True, nullable=False)
    artist_id = Column(String(60), ForeignKey('artist.id'), nullable=False)
    orders = relationship('Order', backref='user', cascade='delete')
    reviews = relationship('Review', backref='artwork', cascade='delete')
