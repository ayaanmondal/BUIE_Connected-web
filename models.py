from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from wtform import *
db = SQLAlchemy()
class User(UserMixin,db.Model):
    __tablename__ = "buieuser3"
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

"""CREATE TABLE buieuser3(
id SERIAL PRIMARY KEY,
username VARCHAR(25) UNIQUE NOT NULL,
password TEXT NOT NULL,
email TEXT NOT NULL,
profile_image TEXT ,
time_inserted DATE,
time_updated DATE
);"""
class Post(db.Model):
    __tablename__ = "buiepost1"
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

"""CREATE TABLE buiepost1(
post_id SERIAL PRIMARY KEY,
title TEXT NOT NULL,
content TEXT NOT NULL,
user_id INT,
date_posted DATE,
FOREIGN KEY (user_id) REFERENCES buieuser3 (id)
);"""
#class Postcontent(db.Model):
    #__tablename__ = "buiecontent"
    #content_id = db.Column(db.Integer, primary_key=True)
    #content = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #def __repr__(self):
        #return f"Post('{self.content}', '{self.date_posted}')"
    
"""CREATE TABLE buiecontent(
content_id SERIAL PRIMARY KEY,
content TEXT NOT NULL,
user_id INT,
date_posted DATE,
FOREIGN KEY (user_id) REFERENCES buieuser2 (id)
);"""