from email import message
from flask import Flask
from flask import render_template, request, url_for, flash, redirect
# from flask_wtf import Form
# from wtforms import StringField, PasswordField, validators
from flask import request
from flask_wtf import Form
from auth import global_ldap_authentication
from flask import Blueprint
from flask_login import login_user
from flask_login import login_required, current_user
from user import User
from flask_login import LoginManager


# main app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# login manager stuff
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template("403.html")

# routes
@app.route('/')
def index():
    return render_template("home.html")

@app.route('/about1')
def about1():
    return render_template("about1.html")


@app.route('/about2')
def about2():
    return render_template("about2.html")

# more dynamic routing
@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    # initiate the form..

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)

        if not username:
            flash('Title is required!')
        elif not password:
            flash('Content is required!')
        login_msg = global_ldap_authentication(username, password)
        print(login_msg)

        # validate the connection
        if login_msg == "Success":
            print("LOGGED IN")
            user = User(username)
            login_user(user)
            
            return redirect(url_for('admin'))

        else:
            print("NOT LOGGED IN")
            return render_template("login.html",message="COULD NOT AUTHENTICATE")

    return render_template('login.html')

@app.route('/whoami')
@login_required
def whoami():
    return render_template("whoami.html",name=current_user.user)

@app.route('/admin')
@login_required
def admin():
    if current_user.user == "admin":
        return render_template("admin.html",name=current_user.user)
        
    return render_template("whoami.html",name=current_user.user)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
