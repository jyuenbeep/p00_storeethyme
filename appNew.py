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

def authenticate(user, passw):
    c.execute(f"SELECT username FROM users WHERE EXISTS (SELECT {user} from users WHERE password={passw})")