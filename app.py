from flask import Flask
from flask import render_template
from flask import request
from flask import session
import sqlite3

app = Flask(__name__)
app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

db = sqlite3.connect("database.db", check_same_thread=False) 
c = db.cursor()

# MAKING TABLES -------------------------------------------

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username STRING, 
    password STRING
    );
""")

c.execute("""
CREATE TABLE IF NOT EXISTS stories (
    story_id INTEGER, 
    title STRING, 
    thumbnail STRING, 
    genres STRING, 
    caption STRING,
    user STRING
);
""")

# GLOBAL VARIABLES --------------------------------------------------------------------------------------

global_storyid = int(0)

# HELPER METHODS ----------------------------------------------------------------------------------------

def authenticate(user, passw):
    c.execute(f"SELECT * FROM users WHERE username='{user}'")
    accountInfo = c.fetchall()
    if len(accountInfo)>0:
        if (accountInfo[0][1]==passw):
            return 2
        return 1
    return 0

def addUser(user, passw):
    if authenticate(user, passw)==0:
        c.execute("INSERT INTO users VALUES (?,?)", (user, passw))
        db.commit()

# TEMPLATES --------------------------------------------------------------------------------------------

headingTemplate = """
    <!DOCTYPE html>
    <html>
    <head>
    <title> {pageName} </title>
    <link rel="stylesheet" type = "text/css" href="../static/{pageName}.css">
    </head>

    <body>
        <h1>
         STOREETHYME {pageName}
        </h1>
        Made by Blue Haired Gals w/ Pronouns (Ziying Jian, Talia Hsia, Jasmine Yuen)
    
        <div>
        <h2>
            WELCOME {username}
        </h2>
        </div>
    """

endTemplate = """
    </body>
    </html>
    """

addingForm = """
    <div>
        <h2> ADD TO THIS STORY! </h2>
        <form action="/add" method="POST">
            <h3> which story? </h3>
            <input type='text' name='sID'>
            <br>
            <h3> make a caption: </h3>
            <input type='text' name='cap'>
            <br>
            <input type='submit' name='submitEntry' value='add'>
        </form>
    </div>
"""


newForm = """
    <div>
        <h2> CREATE A NEW STORY! </h2>
        <form action="/new" method="POST">
            <h3> title </h3>
            <input type='text' name='title_query'>
            <br>
            <h3> make a caption: </h3>
            <input type='text' name='caption_query'>
            <br>
            <input type='submit' name='submitEntry' value='new'>
        </form>
    </div>
"""

# HTML BUILDING HELPER METHODS ---------------------------------------------------------------------------------

def writeHTML(htmlTemplate, file):
    with open("templates/"+file, 'w') as f:
        f.write(htmlTemplate)
    f.close()

def html_AddToStories(user):
    this_html_template = headingTemplate.format(pageName="adding to story", username=user) + addingForm + endTemplate
    writeHTML(this_html_template, "add.html")

def html_newStory(user):
    this_html_template = headingTemplate.format(pageName="creating new story", username=user) + newForm + endTemplate
    writeHTML(this_html_template, "new.html")

def writeToStory(storyID, imageLink, caption, genres, user):
    c.execute("SELECT title FROM stories WHERE id=\"{storyID}\"")
    title_get = c.fetchall()
    c.execute(f"""
        INSERT INTO stories VALUES (
            {storyID},
            {title_get},
            {imageLink},
            {genres},
            {caption},
            {user}
        );
    """)
    db.commit()

def writeNewStory(title_input, img_link, genre, cap, user_sesh):
    global global_storyid
    c.execute(f"""
        INSERT INTO stories VALUES (
            {global_storyid},
            \"{title_input}\",
            \"{img_link}\",
            \"{genre}\",
            \"{cap}\",
            '{user_sesh}'
        )
    """)
    db.commit()
    #global_storyid+=1

# FLASK APP ROUTING --------------------------------------------------------------------------------------

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

@app.route('/add', methods=['GET', 'POST'])
def add_story():
    if request.method == "POST":
        writeToStory(request.form['sID'], "TESTING", request.form['cap'], ["testing1", "testing2"], session['username'])
        return render_template('login.html')
    html_AddToStories(session['username'])
    return render_template('add.html')    

@app.route('/new', methods=['GET', 'POST'])
def new_story():
    if request.method == "POST":
        writeNewStory(request.form['title_query'], "testing image", "testing genre", request.form['caption_query'], session['username'])
        return render_template('response.html')
    html_newStory(session['username'])
    return render_template('new.html')

# RUNNING THIS! -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run()