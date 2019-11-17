from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from wtform import *
db = SQLAlchemy()
class User(UserMixin,db.Model):
    __tablename__ = "users5"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, index=True)
    profile_image = db.Column(db.String(250), nullable=False,default='default_profile.png')
    time_inserted = db.Column(db.DateTime(), default=datetime.utcnow)
    time_updated = db.Column(db.DateTime(), default=datetime.utcnow)
    #posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.password}','{self.profile_image}')"

#<!-- CREATE TABLE users5(
#id SERIAL PRIMARY KEY,
#username VARCHAR(25) UNIQUE NOT NULL,
#password TEXT NOT NULL,
#email TEXT NOT NULL,
#profile_image TEXT ,
#time_inserted DATE,
#time_updated DATE
#);
class Post(db.Model):
    __tablename__ = "users6"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_inserted = db.Column(db.DateTime(), default=datetime.utcnow)
    time_updated = db.Column(db.DateTime(), default=datetime.utcnow)

#CREATE TABLE users6(
#id SERIAL PRIMARY KEY,
#title TEXT NOT NULL,
#content TEXT NOT NULL,
#user_id INT,
#time_inserted DATE,
#time_updated DATE
#);

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



    def __init__(self, email, username, password='1234'):
        self.email = email
        self.username = username
        self.password = password

    def check_password(self, password):
        return password(self, password)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        return {
            'email': self.id,
            'profile_image': self.profile_image,
            'email': self.email,
            'username': self.username,
            'password': self.password}

    
