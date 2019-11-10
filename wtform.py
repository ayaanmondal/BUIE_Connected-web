from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, csrf
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email
#from models import User
from flask_wtf.file import FileField, FileAllowed
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

    email = StringField('username_lable',
    validators=[InputRequired(message="email required"),Length(min=4,max=25,
    message="email not fitting"), Email()])

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

    def validate_email(self,email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email id already exists, Select a different username.")

class LoginForm(FlaskForm):
    username = StringField('username_lable',
    validators=[InputRequired(message="Username required")])

    password = PasswordField('password_lable',
    validators=[InputRequired(message="password required"),invalid_credentials])

    submit_botton = SubmitField('Login')



class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has already been registered!')



