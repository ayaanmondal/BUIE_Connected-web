from flask import Flask, render_template, json, request,url_for
from wtform import *

app = Flask(__name__)
app.secret_key="winner winner chicken dinner"
app.config['SECRET_KEY'] = 'any secret string'
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def singup():
    reg_form = RegistrationFrom()
    if reg_form.validate_on_submit():
        return "Successfully Register"

    return render_template('signup.html',form =reg_form)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=False)