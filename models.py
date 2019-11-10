from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
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
            'password_hash': self.password}

    def __repr__(self):
        return f"Username {self.username}"

    
