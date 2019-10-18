from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, csrf
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

def invalid_credentials(form,field):

    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or Password is incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Username or Password is incorrect")

class RegistrationFrom(FlaskForm):

    username = StringField('username_lable',
    validators=[InputRequired(message="Username required"),Length(min=4,max=25,
    message="Username must be between 4 and 25 characters")])

    password = PasswordField('password_lable',
    validators=[InputRequired(message="Username required"),Length(min=4,max=25,
    message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_lable',
     validators=[InputRequired(message="Password required"), 
     EqualTo('password', message="Passwords must match")])

    submit_botton = SubmitField('Create')

    def validate_username(self,username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Usernamename already exists, Select a different username.")

class LoginForm(FlaskForm):
    username = StringField('username_lable',
    validators=[InputRequired(message="Username required")])

    password = PasswordField('password_lable',
    validators=[InputRequired(message="password required"),invalid_credentials])

    submit_botton = SubmitField('Login')
