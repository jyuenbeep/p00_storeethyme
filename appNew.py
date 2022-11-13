from flask import Flask
from flask import render_template
from flask import request
from flask import session
import sqlite3

app = Flask(__name__)
app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

# HELPER METHODS

db = sqlite3.connect("database.db", check_same_thread=False) 
c = db.cursor()

# AUTHENTICATE RETURNS:
# 0 = USERNAME DOES NOT EXIST
# 1 = PASSWORD IS INCORRECT
# 2 = GOOD TO GO
def authenticate(user, passw):
    c.execute(f"SELECT * FROM users WHERE username='{user}'")
    accountInfo = c.fetchall()
    if len(accountInfo)>0:
        if (accountInfo[0][1]==passw):
            return 2
        return 1
    return 0

# # TEST CASES FOR AUTHENTICATE
# # right now TABLE users has [hi, bye] as its only row
# print(authenticate('bye', 'rand')) #should return 0
# print(authenticate('hi', 'rand')) #should return 1
# print(authenticate('hi', 'bye')) #should return 2

def addUser(user, passw):
    if authenticate(user, passw)==0:
        c.execute("INSERT INTO users VALUES (?,?)", (user, passw))
        db.commit()
    # # TESTING
    # c.execute("SELECT * FROM users")
    # print(c.fetchall())

# FLASK APP ROUTING

# LANDING PAGE
# checks if user is logged into session
# if yes, displays welcome page
# if no, displays login page
@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        return render_template('response.html', functional="WORKS!", username=session['username'])
    return render_template('login.html')

# LOGIN PAGE
# has login section, which will say bad user or pass accordingly
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        loginResult = authenticate(request.form['usernameLog'], request.form['passwordLog'])
        if loginResult==2:
            session['username'] = request.form['usernameLog']
            return render_template('response.html', functional="WORKS!", username=session['username'])
        elif loginResult==0:
            return render_template('login.html', loginMSG="Bad username.")
        else:
            return render_template('login.html', loginMSG="Bad password.")

# REGISTER ROUTE
# will display different html templates depending on status of request.method
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        userForm = request.form['usernameReg']
        passForm = request.form['passwordReg']
        if userForm=="" or passForm=="":
            return render_template('register.html', registerMSG="username and password fields cannot be blank")
        addUser(userForm, passForm)
        return render_template('login.html')
    return render_template('register.html')

# LOGOUT ROUTE
# logs user out of the session
@app.route('/logout', methods=['POST'])
def logout():
    if request.method == "POST":
        session.pop('username', None)
        return render_template('login.html', loginMSG="Logged out")

# RUNNNING IT ALL

if __name__ == "__main__":
    app.debug = True
    app.run()