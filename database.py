import sqlite3

DB_NAME = "babynames.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS baby_names (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        gender TEXT NOT NULL,
        count INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()