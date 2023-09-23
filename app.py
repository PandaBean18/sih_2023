from flask import Flask 
from markupsafe import escape
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
from user import User

app = Flask(__name__)

app.secret_key = b'3bbeb23b5e850898a4b872c5908302899d3fa8f63cda539cd2ce03205531349d'

def current_user():
    if session.get('session_token'):
        return User.find_by_session_token(session.get('session_token'))
    else: 
        return None
    
@app.route('/')
def home():
    user = current_user()
    
    return "{} {} {}".format(user.username, user.mail, user.phone)
    
@app.route("/register/")
def register():
    return render_template('register.html')

@app.route("/users/new", methods=['POST'])
def new():
    if not current_user():
        username = request.form['user[username]']
        password = request.form['user[password]']
        mail = request.form['user[mail]']
        phone = request.form['user[phone]']
        user_type = request.form['user[type]']
        user = User(username, password, mail, phone, user_type).create()

        if user:
            session['session_token'] = user.session_token
            return redirect('/')
        else: 
            return redirect('/register')

