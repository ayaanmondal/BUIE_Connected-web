from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, csrf
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError


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