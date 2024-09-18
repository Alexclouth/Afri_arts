from datetime import datetime
from web_flask import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Many-to-many table for likes
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(128), nullable=False)
    is_artist = db.Column(db.String(10), nullable=False, default='member')
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    country = db.Column(db.String(128), nullable=True)
    bio = db.Column(db.String(1024), nullable=True)
    posts = db.relationship('Artwork', backref='uploader', lazy=True)
    comments = db.relationship('Comment', backref='commented_by', lazy=True)
    liked_artworks = db.relationship('Artwork', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



class Artwork(db.Model):
    """Represents an artwork for the Afri-Arts Gallery Showcase."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    image = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    art_type = db.Column(db.String(128), nullable=False)
    style = db.Column(db.String(128), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='commented_on', lazy=True)

    def total_likes(self):
        """Returns the total number of likes this artwork has received."""
        return self.liked_by.count()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Foreign keys
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

