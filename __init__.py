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

def story_unadded_to(user, storyid):
    c.execute(f"SELECT * FROM stories WHERE story_id={storyid}")
    output = c.fetchall()
    if len(output)==0:
        return 0
    if output[0][4]==user:
        return 1

# TEMPLATES --------------------------------------------------------------------------------------------

headingTemplate = """
    <!DOCTYPE html>
    <html>
    <head>
    <title> {pageName} </title>
    <link rel="stylesheet" type = "text/css" href="../static/{pageName}.css">
    </head>

    <body>
        Made by Blue Haired Gals w/ Pronouns (Ziying Jian, Talia Hsia, Jasmine Yuen)

        <div>
        <h1>
            WELCOME, {username}!
        </h1>
        </div>
        <div class = #navabar>
            <a href="/">Profile</a>
            <a href="/add">Add to an existing story!</a>
            <a href="/new">Create a new story!</a>
        </div>
    """

endTemplate = """
    </body>
    </html>
"""

addingForm = """
    <div>
        <h2> ADD TO A STORY! </h2>
        <form action="/add" method="POST">
            <h3> Provide the story's unique story ID: </h3>
            <input type='text' name='storyid_query'>
            <br>
            <br>
            <h3> Input your awesome one-liner: </h3>
            <input type='text' name='caption_query'>
            <br>
            <br>
            <h3> Genre??? </h3>
            <input type='text' name='genre_query'>
            <br>
            <input type='submit' name='submitEntry' value='add'>
            <br>
            {message}
        </form>
        <br>
        <form action="/viewRecent" method="POST">
            <h3> view this story's recent update </h3>
            <input type='text' name='storyid_query2'>
            <br>
            <input type='submit' name='view' value='view'>
            <br>
            {message2}
        </form>
    </div>
"""

newForm = """
    <div>
        <h2> CREATE A NEW STORY! </h2>
        <form action="/new" method="POST">
            <h3> Input your *dazzling* title: </h3>
            <input type='text' name='title_query'>
            <br>
            <h3> Enter your awesome one-liner to start off: </h3>
            <input type='paragraph' name='caption_query'>
            <br>
            <br>
            <h3> Genre?? </h3>
            <input type='text' name='genre_query'>
            <br>
            <input type='submit' name='submitEntry' value='new'>
            <br>
            {message}
        </form>
    </div>
"""

landingPage_skeleton = """
<div>
    <h3>
    The stories you have already added to:
    </h3>
    {viewStories_code}
    <form action='/logout' method = "POST">
        <button type="submit">Logout</button>
    </form>
</div>
"""

view_recent = """
    <!DOCTYPE html>
    <html>
    <head>
    <title> {storyid} recent update </title>
    </head>
    <body>
        <h1>STORY ID: {storyid}</h1>
        <h1>TITLE: {title}</h1>
        <h2>{caption}</h2>
        <button><a href="/add">go back</a></button>
    </body>
    </html>
"""

# HTML BUILDING HELPER METHODS ---------------------------------------------------------------------------------

def writeHTML(htmlTemplate, file):
    with open("templates/"+file, 'w') as f:
        f.write(htmlTemplate)
    f.close()

def html_AddToStories(user, addingForm_message, addingMessage2):
    this_html_template = headingTemplate.format(pageName="Add on to a story!", username=user)

    html_string = """
        <table>
            <tr>
                <th>ID</th>
                <th>TITLE</th>
                <th>GENRE</th>
            </tr>
    """
    c.execute(f"SELECT * FROM stories WHERE user!='{user}'")
    ary_stories = c.fetchall()
    print(ary_stories)
    for i in range(len(ary_stories)):
        html_string += "<tr>"
        for y in range(len(ary_stories[i])-2):
            html_string += "<td>" + str(ary_stories[i][y]) + "</td>"
        html_string += "</tr>"
    html_string += "</table>"
    this_html_template += html_string
    this_html_template += addingForm.format(message=addingForm_message, message2=addingMessage2) + endTemplate
    writeHTML(this_html_template, "add.html")

def html_newStory(user, newForm_message):
    this_html_template = headingTemplate.format(pageName="Create a new story!", username=user) + newForm.format(message=newForm_message) + endTemplate
    writeHTML(this_html_template, "new.html")

def html_viewStories(user):
    html_string = """
        <table>
            <tr>
                <th>ID</th>
                <th>TITLE</th>
                <th>ENTRY</th>
                <th>GENRE</th>
            </tr>
    """
    c.execute(f"SELECT * FROM stories WHERE user='{user}'")
    ary_stories = c.fetchall()
    for i in range(len(ary_stories)):
        html_string += "<tr>"
        for y in range(len(ary_stories[i])-1):
            html_string += "<td>" + str(ary_stories[i][y]) + "</td>"
        html_string += "</tr>"
    html_string += "</table>"

    this_html_template = headingTemplate.format(pageName="PROFILE", username=user) + landingPage_skeleton.format(viewStories_code=html_string)
    writeHTML(this_html_template, "landing.html")

def writeToStory(id_input, genre, cap, user_sesh):
    c.execute(f"SELECT title FROM stories WHERE story_id={id_input}")
    title_get = c.fetchone()
    c.execute(f"""
        INSERT INTO stories VALUES (
            {id_input},
            \"{title_get[0]}\",
            \"{genre}\",
            \"{cap}\",
            '{user_sesh}'
        );
    """)
    db.commit()

def writeNewStory(title_input, genre, cap, user_sesh):
    global global_storyid
    c.execute(f"""
        INSERT INTO stories VALUES (
            {global_storyid},
            \"{title_input}\",
            \"{genre}\",
            \"{cap}\",
            '{user_sesh}'
        )
    """)
    db.commit()
    global_storyid+=1

def html_viewRecent(id):
    c.execute(f"SELECT * FROM stories WHERE story_id={id}")
    store = c.fetchall()
    recent = store[len(store)-1]
    this_html_template = view_recent.format(storyid=id, title=recent[1], caption=recent[3])
    writeHTML(this_html_template, "viewRecent.html")

# FLASK APP ROUTING --------------------------------------------------------------------------------------

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        html_viewStories(session['username'])
        return render_template('landing.html', user=session['username'])
    return render_template('login.html')

# LOGIN PAGE
# has login section, which will say bad user or pass accordingly
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        loginResult = authenticate(request.form['usernameLog'], request.form['passwordLog'])
        if loginResult==2:
            session['username'] = request.form['usernameLog']
            return render_template('landing.html', user=session['username'])
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
        if request.form['storyid_query']=="" or request.form['caption_query']=="" or request.form['genre_query']=="":
            html_AddToStories(session['username'], "please fill in all queries", "")
        elif story_unadded_to(session['username'], request.form['storyid_query'])==0:
            html_AddToStories(session['username'], "this story id does not exist", "")
        elif story_unadded_to(session['username'], request.form['storyid_query'])==1:
            html_AddToStories(session['username'], "you have already added to this story and cannot add again", "")
        else:
            writeToStory(request.form['storyid_query'], request.form['genre_query'], request.form['cap_query'], session['username'])
            return render_template('landing.html', user=session['username'])
    else:
        html_AddToStories(session['username'], "", "")
    return render_template('add.html')

@app.route('/viewRecent', methods=['GET', 'POST'])
def story_profile():
    if request.method == "POST":
        if request.form['storyid_query2']!="":
            c.execute(f"SELECT * FROM stories WHERE story_id={request.form['storyid_query2']}")
            store = c.fetchall()
            if len(store)!=0:
                html_viewRecent(request.form['storyid_query2'])
                return render_template("viewRecent.html")
            html_AddToStories(session['username'], "", "Please insert a valid story id")
    return render_template('add.html')

@app.route('/new', methods=['GET', 'POST'])
def new_story():
    if request.method == "POST":
        if request.form['title_query']=="" or request.form['caption_query']=="" or request.form['genre_query']=="":
            html_newStory(session['username'], "Please fill in all queries")
        else:
            writeNewStory(request.form['title_query'], request.form['genre_query'], request.form['caption_query'], session['username'])
            return render_template('landing.html', user=session['username'])
    else:
        html_newStory(session['username'], "")
    return render_template('new.html')

# RUNNING THIS! -------------------------------------------------------------------------------------------------

if __name__ == "__init__":
    app.debug = True
    app.run()
