from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, logout_user, login_required
from my_blog import db
from my_blog.models import User, Post
from my_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm)
from my_blog.users.utils import send_reset_email, db_update_pass, db_get_login, db_register_user, update_img

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    This method registers new user.
    :return: redirect user to login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit() and db_register_user(form=form):
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login_get'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['POST'])
def login_post():
    """
    This method allows users to login
    :return: redirect to main page
    """
    form = LoginForm()
    if form.validate_on_submit() and db_get_login(form=form):
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))

    flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/login")
def login_get():
    """
    This method displays login page
    :return: render login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    """
    This method logouts user
    :return: redirect to main page
    """
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account")
@login_required
def show_account():
    """
    This method displays account page.
    :return: render account page.
    """
    form = UpdateAccountForm()
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/account", methods=['POST'])
@login_required
def update_account():
    """
    This method allows user to change theirs name, email and profile picture.
    :return: redirect to main page.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            update_img(form)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.index'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """
    This method allows users see all posts created by other user.
    :param username: user name
    :return: render page with all user posts.
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.date_posted.desc())\
                      .paginate(page=page, per_page=6)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    This method allows users to reset theirs password
    :return: redirect to login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login_get'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """
    This method updates user password.
    :param token: token send to user email
    :return: redirect to login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit() and db_update_pass(user,form):
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login_get'))
    return render_template('reset_token.html', title='Reset Password', form=form)


