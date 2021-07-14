from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from my_blog.users.validators import *


class RegistrationForm(FlaskForm):
    """
    This class stores registration form.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20), register_user_validate_username])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), register_user_validate_email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    This class stores login form.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    This class stores update account form.
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20), update_account_validate_username])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), update_account_validate_email])
    picture = FileField('Update Profile Picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    """
    This class stores request reset form.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email(), request_reset_validate_email])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """
    This class stores reset password form.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
