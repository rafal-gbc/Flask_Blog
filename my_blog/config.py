import os
from dataclasses import dataclass

@dataclass
class Config:
    """
    This is the default configuration for application.
    """
    SECRET_KEY = 'YOUR SECRET KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'USER_NAME'
    MAIL_PASSWORD = 'PASSWORD'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
