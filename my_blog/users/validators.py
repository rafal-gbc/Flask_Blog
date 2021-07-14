from flask_login import current_user
from wtforms import ValidationError

from my_blog.models import User


def check_if_exception(user, msg):
    """
    This method raise ValidationError with message
    """
    if user:
        raise ValidationError(f"That {msg} is taken. Please choose a different one.")


def request_reset_validate_email(_, field):
    """
    This method validates reset password.
    Checks if the account exists.
    """
    user = User.query.filter_by(email=field.data).first()
    if user is None:
        raise ValidationError('There is no account with that email. You must register first.')


def register_user_validate_username(_, field):
    """
    This method validates new user registration.
    Checks whether user is already registered.
    """
    user = User.query.filter_by(username=field.data).first()
    check_if_exception(user, 'username')


def register_user_validate_email(_, field):
    """
    This method validates new user registration.
    Checks whether email is already registered.
    """
    user = User.query.filter_by(email=field.data).first()
    check_if_exception(user, 'email')


def update_account_validate_username(_, field):
    """
    This method validates account update.
    Checks whether user name is already in use.
    """
    if field.data != current_user.username:
        user = User.query.filter_by(username=field.data).first()
        check_if_exception(user, 'username')


def update_account_validate_email(_, field):
    """
    This method validates user email update.
    Checks whether user name is already in use..
    """
    if field.data != current_user.email:
        user = User.query.filter_by(email=field.data).first()
        check_if_exception(user, 'email')
