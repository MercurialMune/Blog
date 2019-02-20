from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title=StringField('Blog Title')
    description= TextAreaField('Blog Here...')
    submit = SubmitField('Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Say something about you...')
    submit = SubmitField('Update')

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    description = TextAreaField('Say Something...', validators=[Required()])
    submit = SubmitField('Post')

class UpdateForm(FlaskForm):
    title = StringField('Blog Title')
    description = TextAreaField('Blog Here...')
    submit = SubmitField('Change')