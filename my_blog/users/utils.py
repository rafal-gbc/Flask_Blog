import json
import os
import secrets
from PIL import Image
from flask import url_for, current_app, request
from flask_login import login_user, current_user
from flask_mail import Message
from my_blog import mail, bcrypt, db
from my_blog.models import User


def save_picture(form_picture, picture_folder, thumbnail=True):
    """
    This method save picture in folder.
    :param form_picture:
    :param picture_folder: picture folder path
    :param thumbnail: image size
    :return: picture file name
    """
    print(form_picture)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, picture_folder, picture_fn)
    if thumbnail:
        output_size = (125, 125)
    else:
        output_size = (780, 520)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def update_img(form):
    """
    This method updates user account picture.
    :param form: UpdateAccountForm
    """
    picture_folder = 'static/profile_pics'
    picture_path = picture_folder + '/' + current_user.image_file
    if current_user.image_file != "default.jpg":
        delete_picture(picture_path)
    current_user.image_file = save_picture(form.picture.data, picture_folder)


def delete_picture(picture_path):
    """
    This method delete picture from picture folder.
    :param picture_path: picture path
    """
    picture = os.path.join(current_app.root_path, picture_path)
    if os.path.exists(picture):
        os.remove(picture)


def send_reset_email(user):
    """
    This method sends the activation token to the user's email address.
    :param user: The email address of the user
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def db_register_user(form):
    """
    This method hashes the password for security and adds new user to the database.
    :param form: RegistrationForm
    :return: True
    """
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return True


def db_get_login(form):
    """
    This method gets user from database.
    :param form: LoginForm
    :return: True
    """
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return True
    return False


def db_update_pass(user, form):
    """
    This method updates user password.
    :param user: user token
    :param form: ResetPasswordForm
    :return: True
    """
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    return True


def validate_comment(required):
    """
    This method validates jason data.
    :param required: dict with required keys and value types.
    :return: json dict
    """
    _json = json.loads(request.data)
    missing_data = [r for r in required.keys()
                    if r not in _json or _json[r] == ""]
    wrong_types = [r for r in required.keys()
                   if not isinstance(_json[r], required[r])]
    if missing_data or wrong_types:
        return False
    return _json
