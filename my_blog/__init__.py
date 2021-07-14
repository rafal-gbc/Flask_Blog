from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from my_blog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """
    This method creates and configure an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from my_blog.users.routes import users
    from my_blog.posts.routes import posts
    from my_blog.main.routes import main
    from my_blog.errors.handlers import errors

    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    create_database(app)

    return app


def create_database(app):
    """
     This method creates new database.
    """
    if not path.exists('/my_blog/database.db'):
        db.create_all(app=app)
        print("Created database")
