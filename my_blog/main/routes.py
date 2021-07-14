from flask import Blueprint, render_template, request
from my_blog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/index")
def index():
    """
    This method displays main page.
    :return: renders main page template
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('index.html', posts=posts)


@main.route("/about")
def about():
    """
    This method displays about page.
    :return: renders about page template.
    """
    return render_template('about.html', title='About')