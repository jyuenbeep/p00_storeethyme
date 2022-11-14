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
