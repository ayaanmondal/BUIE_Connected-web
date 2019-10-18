from flask import Flask, render_template, json, request,url_for
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/signup')
def singup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=False)