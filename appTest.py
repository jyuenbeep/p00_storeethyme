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

# CREATING TABLE <USERS> IN DATABASE.DB (IF IT DOESN'T ALREADY EXIST)

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

def writeNewStory(title_input, img_link, genre, cap, user_sesh):
    global global_storyid
    c.execute(f"""
        INSERT INTO stories VALUES (
            1,
            '{title_input}',
            '{img_link}',
            '{genre}',
            '{cap}',
            '{user_sesh}'
        );
    """)
    db.commit()

writeNewStory("title", "image", "genre", "caption", "risson")

c.execute("SELECT * FROM stories")
print(c.fetchall())

