import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
<<<<<<< HEAD
from web_flask.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'
mail = Mail()

migrate = Migrate(db)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)

    from web_flask.users.routes import users
    from web_flask.posts.routes import posts
    from web_flask.main.routes import main
    from web_flask.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
=======

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://afri_dev:Ala123.,@localhost/afri_db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)
>>>>>>> bd7c580235255908c4cca384db881c411e0799b9

    return app

<<<<<<< HEAD
=======
from web_flask.users.routes import users
from web_flask.posts.routes import posts
from web_flask.main.routes import main
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

>>>>>>> bd7c580235255908c4cca384db881c411e0799b9
