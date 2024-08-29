from models.base_model import BaseModel

class Review(BaseModel):
    user_id = ""
    artwork_id = ""
    comment = ""
    likes = ""
