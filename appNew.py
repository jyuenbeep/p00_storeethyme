from flask import Flask
from flask import render_template
from flask import request
from flask import session
import sqlite3

DB_FILE="database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("CREATE TABLE if not exists users (username STRING, password STRING);")

app = Flask(__name__)

app.secret_key = "23bd2dcea35c795e204d397157f3d55bf1afda7db6519a46f9d1e5a5f02ed45b"

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