from flask import Flask, render_template, json, request,url_for,redirect,flash
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from wtform import *
from models import *



app = Flask(__name__)
app.secret_key="winner winner chicken dinner"
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI']='postgres://kmckkawkyhqpbl:adfd02bf7120f1368b1d52a02e5a5acbd75de157627c0557e1103ed070cb53a1@ec2-54-225-76-136.compute-1.amazonaws.com:5432/d8ev1f4qtpbka5'
db = SQLAlchemy(app)


login=LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def singup():
    reg_form = RegistrationFrom()
    if reg_form.validate_on_submit():
        username = reg_form.username.data 
        password = reg_form.password.data
        email = reg_form.email.data


        user_object1 = User.query.filter_by(username=username).all()
        if user_object1:
            return "User name already in use"
        user_object2 = User.query.filter_by(email=email).all()
        if user_object2:
            return "email already in use"
        user = User(username=username, password=password,email=email)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))


    return render_template('signup.html',form =reg_form)

@app.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chatroom'))

    return render_template('login.html',form=login_form)


@app.route("/logout",methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully','success')
    return redirect(url_for('login'))




@app.route('/chatroom',methods=['GET','POST'])
def chatroom():
    if not current_user.is_authenticated:
        flash("you are unautharased",'denger')
        return redirect(url_for('login'))

    flash("You are logged is successfully",'success')
    return render_template('chat.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        #return redirect(url_for('users.account'))
        return render_template('account.html')

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image =url_for('static',filename='images/' + current_user.profile_image)
    return render_template('account.html',
                           profile_image=profile_image, form=form)



if __name__ == "__main__":
    app.run(debug=False)