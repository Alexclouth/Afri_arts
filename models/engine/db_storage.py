#!/usr/bin/python3
"""Database storage"""
from models.base_model import BaseModel, Base
from models.order import Order
from models.artwork import Artwork
from models.artist import Artist
from models.review import Review
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from os import getenv


class DBStorage:
    """Database storage class
    Attributes: __engine, __session
    """
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('AFRI_MYSQL_USER'),
                                              getenv('AFRI_MYSQL_PWD'),
                                              getenv('AFRI_MYSQL_HOST'),
                                              getenv('AFRI_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('AFRI_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Method that queries on the currect database session"""
        objects_dictionary = {}

        if cls is None:
            objects_list = self.__session.query(Artist).all()
            objects_list.extend(self.__session.query(Artwork).all())
            objects_list.extend(self.__session.query(User).all())
            objects_list.extend(self.__session.query(Order).all())
            objects_list.extend(self.__session.query(Review).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects_list = self.__session.query(cls).all()

        for obj in objects_list:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects_dictionary[key] = obj

        return objects_dictionary

    def new(self, obj):
        """Method that adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Method that commits all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Method that deletes from the current database
        session obj if not None"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Method that creates all tables in the database"""

        Base.metadata.create_all(self.__engine)
        my_session = sessionmaker(bind=self.__engine,
                                  expire_on_commit=False)
        Session = scoped_session(my_session)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()
