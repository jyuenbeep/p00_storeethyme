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
import sqlite3

app = Flask(__name__)
app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

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

c.execute("""
CREATE TABLE if not exists users (
    username STRING, 
    password STRING,
);
""")
# use sql join tables to make tables within tables
# this table within the row will capture already added to stories
c.execute("""
CREATE TABLE if not exists stories (
    id INTEGER, 
    title STRING, 
    thumbnail STRING, 
    genres STRING[], 
    caption STRING
    userUpdate STRING
);
""")

def writeToStory(storyID, imageLink, caption, genres, user):
# will go through the UPDATES column of the specified story in table stories in database.db
# INSERT INTO UPDATES WHERE STORIES.ID = STORYID
    c.execute(f"""
        INSERT INTO stories VALUES (
            {storyID},
            SELECT title FROM stories WHERE id={storyID},
            {imageLink},
            {genres},
            {caption},
            {userUpdate}
        );
    """)

def writeAddToStories(user):
    this_html_template = headingTemplate.format(
        pageName="adding to story",
        username=user
    ) + addingForm + endTemplate
    writeHTML(this_html_template, add.html)

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
"""

def writeNewStory(title, genres, thumbnail, caption, user):
# INSERT INTO STORIES [all the information]
# INSERT INTO UPDATES WHERE STORIES.ID = STORYID
    c.execute(f"""
        INSERT INTO stories VALUES (
            {storyid},
            {title},
            {thumbnail},
            {genres},
            {caption},
            {user}
        );
    """)
    db.commit()
    storyid+=1