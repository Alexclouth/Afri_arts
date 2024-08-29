import uuid
import models
from datetime import datetime

class BaseModel:
    """Defines all common attributes/methods for other classes."""
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        value = datetime.fromisoformat(value) #This method expects the string to be in the format YYYY-MM-DDTHH:MM:SS.ssssss
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)  # Add instance to storage

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the updated_at attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()  # Save all instances to file

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance."""
        dict_representation = self.__dict__.copy()
        dict_representation['__class__'] = self.__class__.__name__
        dict_representation['created_at'] = self.created_at.isoformat()
        dict_representation['updated_at'] = self.updated_at.isoformat()
        return dict_representation
