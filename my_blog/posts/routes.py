from flask import (render_template, url_for, flash,
                   redirect, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from my_blog import db
from my_blog.models import Post, Comment, User
from my_blog.posts.forms import PostForm
from my_blog.users.utils import save_picture, delete_picture, validate_comment

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    This method creates new post.
    If all fields in post form are validated redirect user to the main view.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, sub_title=form.sub_title.data, content=form.content.data,
                    author=current_user)
        if form.picture.data:
            picture_folder = 'static/post_pics'
            post.image_file = save_picture(form.picture.data, picture_folder, False)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def display_post(post_id):
    """
    This method displays single post view.
    :param post_id:
    :return: post.html
    """
    post = Post.query.get_or_404(post_id)
    form = PostForm() #TODO
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc())
    return render_template('post.html',form=form, title=post.title, sub_title=post.sub_title, post=post, comments=comments)


@posts.route("/post/<int:post_id>/update")
@login_required
def show_post_update(post_id):
    """
    This method renders create_post view.
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    This method allows users to update theirs post.
    If all fields are validated post will be updated.
    :param post_id:
    :return: redirect to post page
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_folder = 'static/post_pics'
            picture_path = picture_folder + '/' + post.image_file
            if post.image_file != "default.jpg":
                delete_picture(picture_path)
            post.image_file = save_picture(form.picture.data, picture_folder, False)
        post.title = form.title.data
        post.sub_title = form.sub_title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.display_post', post_id=post.id))
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    This method allows users delete theirs posts.
    :param post_id:
    :return: redirect to main view
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.query(Comment).filter(Comment.post_id == post_id).delete()
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))


@posts.route('/posts/add_comment', methods=['POST'])
def add_comment():
    """
    This method allows add comments to posts.
    :return: new comment
    """
    _json = validate_comment({"comment": str, "post_id": int, "user": str})
    if _json:
        body = _json['comment']
        user_name = _json['user']
        post_id = _json['post_id']
        user = User.query.filter_by(username=user_name).first_or_404()
        new_comment = Comment(body=body, post_id=post_id, user_id=user.id)
        db.session.add(new_comment)
        db.session.commit()
    return jsonify({})
