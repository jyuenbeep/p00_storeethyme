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

#Creates table and executes
#db.execute("DROP TABLE if exists users")
createUser = "CREATE TABLE if not exists users (username STRING, password STRING);"
c.execute(createUser)

#print("----COURSES TABLE----")

#Fetch all rows from ONE data table
# c.execute('SELECT * from courses;') #query
# for i in c.fetchall(): #
#     print(i) #Prints out each data 
    
# print("----STUDENTS TABLE----")

# c.execute('SELECT * from students;') #query
# for i in c.fetchall():
#     print(i) #Prints out each data 

# for i in range(len(students)):
#     c.execute(f"INSERT INTO students VALUES (students['name'][{i}], students['age'][{i}], students['id'][{i}]);")

# for i in range(len(courses)):
#     c.execute(f"INSERT INTO students VALUES (courses['code'][{i}], courses['mark'][{i}], courses['id'][{i}]);")

#==========================================================



# FLASK

app = Flask(__name__)

#hard-coded login info
username = "ziying"
password = "john"

app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

def authenticate(user, passw):
    return (user == username and passw == password)

def addUser(user, passw):
    addUser = f"INSERT INTO users VALUES('{user}', '{passw}');"
    c.execute(addUser)

    db.commit() #save changes
    db.close()  #close database

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        #if the user is already logged into the session
        return render_template('response.html', functional="WORKS!", username=session['username'])
    return render_template('login.html')


@app.route(, methods=['GET', 'POST'])
def login():
    #authenticate login info from form using "request.args"
    if authenticate(request.args['username'], request.args['password']):
        #establishes a session
        session['username'] = request.args['username']
        #bring to new page
        return render_template('response.html', functional="WORKS!", username=session['username'])
    #error messages
    else:
        if username != request.args['username']:
            return render_template('login.html', loginMSG="Bad username.")
        return render_template('login.html', loginMSG="Bad password.")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html', loginMSG="Logged out")


if __name__ == "__main__":
    app.debug = True
    app.run()