import re
import sqlite3

DB_NAME = "babynames.db"


def extract_year(file_path):
    """Extract the 4-digit year from an SSA filename like yob2024.txt."""
    match = re.search(r"yob(\d{4})\.txt$", file_path)
    if not match:
        raise ValueError("File name must end with 'yobYYYY.txt'")
    return int(match.group(1))


def load_data(file_path):
    year = extract_year(file_path)
    imported_rows = 0

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                name, gender, count = line.strip().split(",")
                cursor.execute("""
                    INSERT INTO baby_names (name, year, gender, count)
                    VALUES (?, ?, ?, ?)
                """, (name, year, gender, int(count)))
                imported_rows += 1

        conn.commit()
    return imported_rows
