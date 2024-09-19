import secrets
import os
<<<<<<< HEAD
=======
from web_flask import app
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9

def save_artwork(art_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(art_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/artworks', picture_fn)
    art_picture.save(picture_path)

    return picture_fn