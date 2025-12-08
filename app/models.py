import sqlite3
DB = 'app.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, user TEXT, task TEXT)''')
    conn.commit()
    conn.close()

# VULNERABLE: weak create (SQL concatenation + plain password)
def create_user_vuln(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    c.execute(query)
    conn.commit()
    conn.close()

def get_user_vuln(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # VULN: concatenated query -> SQLi
    query = f"SELECT * FROM users WHERE username = '{username}'"
    c.execute(query)
    row = c.fetchone()
    conn.close()
    return row

# VULN: create todo without parameterization
def add_todo_vuln(user, task):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    q = f"INSERT INTO todos (user, task) VALUES ('{user}', '{task}')"
    c.execute(q)
    conn.commit()
    conn.close()

def list_todos(user):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todos WHERE user = ?", (user,))
    rows = c.fetchall()
    conn.close()
    return rows
