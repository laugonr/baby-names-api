import sqlite3
from pathlib import Path

# database.py keeps the SQLite setup in one place.
# Other files call these helper functions instead of repeating database code.

# Store the database file in the same folder as the Python files.
DB_NAME = Path(__file__).resolve().parent / "babynames.db"


def get_connection():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the baby_names table and unique index if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Main table for each name, year, gender, and number of births.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS baby_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            gender TEXT NOT NULL,
            count INTEGER NOT NULL
        )
        """)

        # Prevent duplicate records for the same name/year/gender.
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_baby_name
        ON baby_names (name, year, gender)
        """)
        conn.commit()
