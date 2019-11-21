import os
import secrets
import psycopg2
from sqlalchemy import update
from PIL import Image
from flask_blogging import BloggingEngine, SQLAStorage
from datetime import datetime
from flask import Flask, render_template, json, request,url_for,redirect,flash
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from wtform import *
from models import *

app = Flask(__name__)
app.secret_key="winner winner chicken dinner"
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////tmp/test.db'
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
    if current_user.is_authenticated:
        return redirect(url_for('chatroom'))
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
    if current_user.is_authenticated:
        return redirect(url_for('chatroom'))
    
    login_form=LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        flash("You are logged is successfully",'success')
        return redirect(url_for('chatroom'))

    return render_template('login.html',form=login_form)


@app.route("/logout",methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully','success')
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_form = UpdateUserForm()
    if update_form.validate_on_submit():
        if update_form.picture.data:
            picture_file = save_picture(update_form.picture.data)
            current_user.profile_image = picture_file
        

        db.session.query(User).filter_by(id=current_user.id).update({"username": update_form.username.data})
        db.session.query(User).filter_by(id=current_user.id).update({"email": update_form.email.data})
        db.session.query(User).filter_by(id=current_user.id).update({"profile_image": picture_file})
        db.session.query(User).filter_by(id=current_user.id).update({"time_updated": datetime.now()})
        db.session.commit()

        flash('User Account Updated!','success')
        #return redirect(url_for('logout'))
        return redirect(url_for('login'))

    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    profile_image =url_for('static',filename='images/' + current_user.profile_image)
    return render_template('account.html',profile_image=profile_image, form=update_form)

def deleteaccount(old_user):
    db.session.delete(old_user.all())
    db.session.commit()

@app.route('/viewaccount', methods=['GET', 'POST'])
@login_required
def view_account():
    username=current_user.username
    email=current_user.email
    profile_image =url_for('static',filename='images/' + current_user.profile_image)
    posts = Post.query.all()
    user = current_user
    return render_template('view_account.html',posts=posts,user=user,profile_image=profile_image,username=username,email=email)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/chatroom',methods=['GET','POST'])
@login_required
def chatroom():
    users= User.query.all()
    posts = Post.query.all()
    return render_template('chat.html',users=users,posts=posts,current_user=current_user)

@app.route('/allusers', methods=['GET', 'POST'])
@login_required
def allusers():
    users = User.query.all()
    return render_template('alluser.html',users=users,current_user=current_user)


@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.is_submitted():
        title = post_form.title.data
        content = post_form.content.data
        new_post = Post(title=title,content=content,user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
    
        #new_content = Postcontent(content=content,user_id=current_user.id)
        #db.session.add(new_content)
        #db.session.commit()

        profile_image =url_for('static',filename='images/' + current_user.profile_image)
        flash('your post has been created!','success')
        return redirect(url_for('chatroom'))
    return render_template('create_post.html',title='New post',form=post_form)

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    users = User.query.all()
    return render_template("post.html",post=post,users = users)

@app.route("/user/<int:user_id>")
@login_required
def searchuser(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.all()
    return render_template("search_user.html",user=user,posts=posts)



if __name__ == "__main__":
    app.run(debug=False)