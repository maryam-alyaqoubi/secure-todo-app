# Use these functions to replace vulnerable ones when fixing
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
DB = 'app.db'

def create_user_secure(username, password):
    hashed = generate_password_hash(password)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()

def get_user_secure(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row

def add_todo_secure(user, task):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO todos (user, task) VALUES (?, ?)", (user, task))
    conn.commit()
    conn.close()

