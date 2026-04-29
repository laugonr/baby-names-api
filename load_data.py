import re
import os

from database import create_table, get_connection
from validation import validate_count, validate_gender, validate_name

# Imports Social Security baby-name files into SQLite.
# Run this when babynames.db needs to be created or refreshed.


def extract_year(file_path):
    """Extract the 4-digit year from an SSA filename like yob2024.txt."""
    match = re.search(r"yob(\d{4})\.txt$", file_path)
    if not match:
        raise ValueError("File name must end with 'yobYYYY.txt'")
    return int(match.group(1))


def load_data(file_path):
    """Load one SSA baby-name file into the database."""
    create_table()

    year = extract_year(file_path)
    imported_rows = 0

    with get_connection() as conn:
        cursor = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                # SSA rows are stored as name, gender, and birth count.
                name, gender, count = line.strip().split(",")

                # Skip rows already imported from a previous run.
                cursor.execute("""
                    INSERT OR IGNORE INTO baby_names (name, year, gender, count)
                    VALUES (?, ?, ?, ?)
                """, (
                    validate_name(name),
                    year,
                    validate_gender(gender),
                    validate_count(count)
                ))

                # rowcount is 0 when INSERT OR IGNORE skips a duplicate.
                imported_rows += cursor.rowcount

        conn.commit()
    return imported_rows


def load_all_data(folder="names"):
    """Load every SSA file from a folder such as names/."""
    total = 0

    for file in os.listdir(folder):
        # Only import the official yobYYYY.txt files.
        if file.startswith("yob") and file.endswith(".txt"):
            path = os.path.join(folder, file)

            try:
                rows = load_data(path)
                total += rows
                print(f"Loaded {file}: {rows}")
            except Exception as e:
                print(f"Error loading {file}: {e}")

    print(f"\nTOTAL LOADED: {total}")


if __name__ == "__main__":
    load_all_data("names")
