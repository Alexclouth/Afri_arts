import json
import os
from models.base_model import BaseModel
from models.user import User

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file at __file_path."""
        with open(self.__file_path, 'w') as f:
            json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists).
        """
        try:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = key.split(".")[0]
                    cls = eval(class_name) # eval is used to dynamically retrieve a class from its name as a string.
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass
