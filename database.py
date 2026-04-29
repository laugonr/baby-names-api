import sqlite3
from pathlib import Path

# Shared SQLite helpers for the API and data loader.

# Keep the database next to the app files.
DB_NAME = Path(__file__).resolve().parent / "babynames.db"


def get_connection():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the baby_names table and unique index if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # One record per name, year, gender, and birth count.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS baby_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            gender TEXT NOT NULL,
            count INTEGER NOT NULL
        )
        """)

        # Running the loader twice should not create duplicate records.
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_baby_name
        ON baby_names (name, year, gender)
        """)
        conn.commit()
