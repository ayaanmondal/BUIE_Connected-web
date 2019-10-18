from flask import Flask, render_template, json, request,url_for,redirect
from wtform import *
from models import *

app = Flask(__name__)
app.secret_key="winner winner chicken dinner"
app.config['SECRET_KEY'] = 'any secret string'

app.config['SQLALCHEMY_DATABASE_URI']='postgres://kmckkawkyhqpbl:adfd02bf7120f1368b1d52a02e5a5acbd75de157627c0557e1103ed070cb53a1@ec2-54-225-76-136.compute-1.amazonaws.com:5432/d8ev1f4qtpbka5'
db = SQLAlchemy(app)





@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def singup():
    reg_form = RegistrationFrom()
    if reg_form.validate_on_submit():
        username = reg_form.username.data 
        password =reg_form.password.data

        user_object = User.query.filter_by(username=username).all()
        if user_object:
            return "User name already in use"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('signup.html',form =reg_form)

@app.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()

    if login_form.validate_on_submit():
        return "Logged in, successfully"

    return render_template('login.html',form=login_form)

if __name__ == "__main__":
    app.run(debug=False)