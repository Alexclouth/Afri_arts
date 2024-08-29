from models.base_model import BaseModel

class User(BaseModel):
    """User class that inherits from BaseModel."""
    
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    is_artist = ""
    profile_picture = ""
    bio = ""
    city = ""
    country = ""
