"""
Blue Haired Gals With Pronouns: Jasmine Yuen, Talia Hsia, Ziying Jian
SoftDev
K19 - Flask app that uses session capabilites to allow user to login and logout
2022-11-03
time spent:
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import session

# SQLITE
import sqlite3   #enable control of an sqlite database


DB_FILE="database.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

createUser = "CREATE TABLE if not exists users (username STRING, password STRING);"
c.execute(createUser)

# FLASK

app = Flask(__name__)

# #hard-coded login info
# username = "ziying"
# password = "john"

app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

def authenticate(user, passw):
    return (user == username and passw == password)

# def addUser(user, passw):
#     addUser = f"INSERT INTO users VALUES('{user}', '{passw}');"
#     c.execute(addUser)
#     db.commit() #save changes

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        #if the user is already logged into the session
        return render_template('response.html', functional="WORKS!", username=session['username'])
    return render_template('login.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    #authenticate login info from form using "request.args"
    if request.method=="POST": 
        if authenticate(request.form['username'], request.form['password']):
            #establishes a session
            session['username'] = request.form['username']
            #session['username'] = request.args['username']
            #bring to new page
            return render_template('response.html', functional="WORKS!", username=session['username'])
            #error messages
        else:
            if username != request.form['username']:
                return render_template('login.html', loginMSG="Bad username.")
            return render_template('login.html', loginMSG="Bad password.")

@app.route("/register", methods=['GET', 'POST'])
def disp_register():
    return render_template('register.html')

def addUser(user, passw):
    addUser = f"INSERT INTO users VALUES('{user}', '{passw}');"
    c.execute(addUser)
    db.commit() #save changes

@app.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    if request.method == "POST":
        session.pop('username', None)
        return render_template('login.html', loginMSG="Logged out")


if __name__ == "__main__":
    app.debug = True
    app.run()
    db.close()  #close database
