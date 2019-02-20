from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, EqualTo, Email
from wtforms import ValidationError
from ..models import User

class RegisterForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Email()])
    username = StringField('Username', validators= [Required()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message= "Both passwords must match")])
    password_confirm = PasswordField('Repeat Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(selfself, data_field):
        if User.query.filter_by(email= data_field.data).first():
            raise ValidationError('An account with that email already exists')
    def validate_username(self, data_field):
        if User.query.filter_by(password=data_field.data).first():
            raise ValidationError('Choose a unique Username')
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')
