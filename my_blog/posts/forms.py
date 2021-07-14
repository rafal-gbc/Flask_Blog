from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    This class stores "post form"
    """
    title = StringField('Title', validators=[DataRequired()])
    sub_title = StringField('Sub Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Add Picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


