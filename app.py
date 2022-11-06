from email import message
from flask import Flask
from flask import render_template, request, url_for, flash, redirect, send_file
from flask import request
from flask_wtf import Form
from auth import global_ldap_authentication
from flask_login import login_user, login_required, current_user
from user import User
from flask_login import LoginManager
from flask_mysqldb import MySQL
import os 
from ftp import FTPServer 
from werkzeug.utils import secure_filename
import tempfile
import mysql.connector as m

# main app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_HOST'] = '10.0.86.76'
app.config['MYSQL_USER'] = 't86'
app.config['MYSQL_PASSWORD'] = 'SuperSecure69'
app.config['MYSQL_DB'] = 'solar'
app.config['UPLOAD_FOLDER'] = 'uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

mysql = MySQL(app)

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
    cursor = mysql.connection.cursor()
    cursor.execute("select arrayID,arrayVoltage,arrayCurrent from solar_arrays")
    data = cursor.fetchall()
    return render_template("home.html",solar_arr=data)

@app.route('/about1')
def about1():
    return render_template("about1.html")

# @app.route('/testsql')
# def testsql():
    # cursor = mysql.connection.cursor()
    # cursor.execute("select arrayID,arrayVoltage,arrayCurrent from solar_arrays")
    # data = cursor.fetchall()
    # print(data)
    # cursor.close()
    # output="ID\tVOLTAGE\tCURR\n"
    # for d in data:
    #     output += f"{d[0]}\t{d[1]}\t{d[2]}\n"

#     print(output)
#     return output

    

@app.route('/about2')
def about2():
    return render_template("about2.html")

# more dynamic routing
@app.route('/contact',methods=['GET', 'POST'])
def contact():
    sess = FTPServer("anonymous","c7f7bcad6ec62836efad15954fd9b1a2","10.0.86.73")
    if request.method == 'POST':
        # print(request.form["email"])
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(upload_path)
            sess.upload_file(filename)
    
        email = request.form["email"]
        if email:
            print(f"UPLOADING {email}")
            conn = m.connect(
                user='blueteam', password='SuperSecure69', host='10.0.86.74', database='mysql'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO emails VALUES (%s);",(email,))
            conn.commit()

        return render_template("contact.html")

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

@app.route('/admin',methods=['GET', 'POST'])
# @login_required
def admin():
    sess = FTPServer("anonymous","c7f7bcad6ec62836efad15954fd9b1a2","10.0.86.73")
        
    
    files = sess.list_files()
    # mysql magic
    conn = m.connect(
        user='blueteam', password='SuperSecure69', host='10.0.86.74', database='mysql'
    )
    cursor = conn.cursor()
    cursor.execute("select * from emails;")

    emails = [a[0] for a in cursor.fetchall()]

    if request.method == "POST":
        f =  (request.form["file"])
        print(f)
        filename = secure_filename(f)
        saveto = tempfile.NamedTemporaryFile().name
        sess.get_file(filename,saveto)
        
        # return the file
        return send_file(saveto,as_attachment=True)



    # if current_user.user == "admin":
        # return render_template("admin.html",files=files,emails=emails)
        
    # return render_template("login.html")
    return render_template("admin.html",files=files,emails=emails)





if __name__ == "__main__":
    app.run(host='0.0.0.0')
