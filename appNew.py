from flask import Flask
from flask import render_template
from flask import request
from flask import session
import sqlite3

app = Flask(__name__)
app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

# OTHER GLOBAL VARIABLES

# keeping a count of how many stories are in the current database (this will act as the story ID)
storyid = 0

# CREATING DATABASE AND TABLES

db = sqlite3.connect("database.db", check_same_thread=False) 
c = db.cursor()
c.execute("""
CREATE TYPE addedTo_object AS OBJECT (
    storyID INTEGER,
    title STRING
);
CREATE TYPE addedTo_subtable IS TABLE OF addedTo_object;
CREATE TABLE if not exists users (
    username STRING, 
    password STRING,
    addedTo addedTo_object
);
""")
# use sql join tables to make tables within tables
# this table within the row will capture already added to stories
c.execute("""
CREATE TYPE updates_object as OBJECT (
    updateNum INTEGER
    image STRING,
    caption STRING,
    user STRING
);
CREATE TYPE updates_subtable IS TABLE OF updates_object;
CREATE TABLE if not exists stories (
    id INTEGER, 
    title STRING, 
    thumbnail STRING, 
    genres STRING[], 
    updateNum INTEGER
);
""")
# use sql join tables to make tables within tables
# this table within the row will capture story updates

# HELPER METHODS

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

# HELPER METHODS FOR WRITING INTO HTML TEMPLATES

# HTML templates
headingTemplate = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title> {pageName} </title>
    </head>

    <body>
        <h1>
         STOREETHYME {pageName}
        </h1>
        Made by Blue Haired Gals w/ Pronouns (Ziying Jian, Talia Hsia, Jasmine Yuen)
    
        <div>
        <h2>
            WELCOME {user}
        </h2>
        </div>
    """
# still need to make a navbar

endTemplate = """
    </body>
    </html>
    """

addedToStories = """
    <div>
    """

# writes html to the file
# will take the name of the html template, the name of the page, and the user in session
def writeHTML(htmlTemplate, file, pageName, user):
    f = open(file, 'w')
    f.write(htmlTemplate)
    f.close()

def writeAddedStories(user):
# will go through the ADDED_TO_STORIES column of the specified user in table users in database.db
# displays all the stories already added to

def writeToStory(storyID, image, caption, user):
# will go through the UPDATES column of the specified story in table stories in database.db
# INSERT INTO UPDATES WHERE STORIES.ID = STORYID
    c.execute(f"""
        INSERT INTO stories.updates WHERE stories.id={storyID} VALUES (
            update num,
            {image},
            {caption},
            {user}
        );
        INSERT INTO users.addedTo WHERE users.username={user} VALUES (
            {storyID},
            stories.title WHERE stories.id={storyID}
        );
    """)

def writeNewStory(title, genres, thumbnail, caption, user):
# INSERT INTO STORIES [all the information]
# INSERT INTO UPDATES WHERE STORIES.ID = STORYID
    c.execute(f"""
        INSERT INTO stories VALUES (
            {storyid}, 
            {title}, 
            {thumbnail}, 
            updates_subtable(
                updates_object(0, {thumbnail}, {caption}, {user})
            )
        );
        
    """)
    storyid+=1

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