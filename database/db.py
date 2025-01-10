import sqlite3

def init_db():
    conn = sqlite3.connect("marketplace.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT
                      )''')
    conn.commit()
    return conn