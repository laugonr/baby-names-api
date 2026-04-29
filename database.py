import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "babynames.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    with get_connection() as conn:
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
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_baby_name
        ON baby_names (name, year, gender)
        """)
        conn.commit()
