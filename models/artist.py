#!/usr/bin/python3
from models.user import User
from models.artwork import Artwork
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import models

class Artist(User):
    """Artist class that inherits from User."""

    __tablename__ = 'artist'

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    country = Column(String(128), nullable=True)
    bio = Column(String(1024), nullable=True)
    artwork = relationship("Artwork", backref="artist", cascade="delete")


    @property
    def artist_id(self):
        return self.id  # Referring to the same ID as artist_id
    
    if getenv('AFRI_TYPE_STORAGE') != 'db':
        @property
        def artworks(self):
            """get a list of all related artwork instances
            with artist_id = to the current artist id
            """
            artwork_list = []

            for artwork in list(models.storage.all(Artwork).values()):
                if artwork.artist_id == self.id:
                    artwork_list.append(artwork)
            return artwork_list
    
