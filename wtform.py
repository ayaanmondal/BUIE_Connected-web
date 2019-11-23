from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, csrf , TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email
#from models import User
from flask_wtf.file import FileField, FileAllowed
from models import User, Post
from flask_login import current_user

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
    validators=[InputRequired(message="email required"),Length(min=4,max=50,
    message="email not fitting"), Email()])

    password = PasswordField('password_lable',
    validators=[InputRequired(message="Username required"),Length(min=4,max=25,
    message="Password must be between 4 and 25 characters")])

    confirm_pswd = PasswordField('confirm_pswd_lable',
     validators=[InputRequired(message="Password required"), 
     EqualTo('password', message="Passwords must match")])

    submit_botton = SubmitField('Create Account')

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
    username = StringField('Username', validators=[])
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit_botton = SubmitField('Update')

    def validate_username(self,username):
        if current_user.username != username.data: 
            user_object = User.query.filter_by(username=username.data).first()
            if user_object:
                raise ValidationError("Usernamename already exists, Select a different username.")

    def validate_email(self,email):
        if current_user.email != email.data:
            user_object = User.query.filter_by(email=email.data).first()
            if user_object:
                raise ValidationError("Email id already exists, Select a different username.")



class PostForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired(message="Title required")])
    content = TextAreaField('Content',validators=[InputRequired(message="Description required")])
    submit_botton = SubmitField('Post')


class AnswerForm(FlaskForm):
    content = TextAreaField('Answer',validators=[InputRequired(message="Description required")])
    submit_botton = SubmitField('Post')