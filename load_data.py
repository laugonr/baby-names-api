import re

from database import create_table, get_connection
from validation import validate_count, validate_gender, validate_name


def extract_year(file_path):
    """Extract the 4-digit year from an SSA filename like yob2024.txt."""
    match = re.search(r"yob(\d{4})\.txt$", file_path)
    if not match:
        raise ValueError("File name must end with 'yobYYYY.txt'")
    return int(match.group(1))


def load_data(file_path):
    create_table()
    year = extract_year(file_path)
    imported_rows = 0

    with get_connection() as conn:
        cursor = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                name, gender, count = line.strip().split(",")
                cursor.execute("""
                    INSERT OR IGNORE INTO baby_names (name, year, gender, count)
                    VALUES (?, ?, ?, ?)
                """, (
                    validate_name(name),
                    year,
                    validate_gender(gender),
                    validate_count(count)
                ))
                imported_rows += cursor.rowcount

        conn.commit()
    return imported_rows
