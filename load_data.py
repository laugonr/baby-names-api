import re
import os

from database import create_table, get_connection
from validation import validate_count, validate_gender, validate_name

# load_data.py imports Social Security baby-name text files into SQLite.
# Run this script when you want to fill or update babynames.db from the
# names/yobYYYY.txt data files.


def extract_year(file_path):
    """Extract the 4-digit year from an SSA filename like yob2024.txt."""
    # The year in the file name becomes the year for every row in that file.
    match = re.search(r"yob(\d{4})\.txt$", file_path)
    if not match:
        raise ValueError("File name must end with 'yobYYYY.txt'")
    return int(match.group(1))


def load_data(file_path):
    """Load one SSA baby-name file into the database."""
    # This function handles one file at a time.

    # Make sure the table exists before inserting data.
    create_table()

    # Example: names/yob2024.txt becomes year 2024.
    year = extract_year(file_path)
    imported_rows = 0

    with get_connection() as conn:
        cursor = conn.cursor()
        with open(file_path, "r") as file:
            for line in file:
                # Each SSA line looks like: Olivia,F,14718
                name, gender, count = line.strip().split(",")

                # INSERT OR IGNORE avoids duplicate rows if the loader is run twice.
                cursor.execute("""
                    INSERT OR IGNORE INTO baby_names (name, year, gender, count)
                    VALUES (?, ?, ?, ?)
                """, (
                    validate_name(name),
                    year,
                    validate_gender(gender),
                    validate_count(count)
                ))

                # rowcount is 1 when a new row was inserted, 0 if ignored.
                imported_rows += cursor.rowcount

        conn.commit()
    return imported_rows

def load_all_data(folder="names"):
    """Load every SSA file from a folder such as names/."""
    # This function loops over the whole data folder and imports each year file.
    total = 0

    for file in os.listdir(folder):
        # Only import files with SSA's yobYYYY.txt naming pattern.
        if file.startswith("yob") and file.endswith(".txt"):
            path = os.path.join(folder, file)

            try:
                # Load one file, then add its inserted row count to the total.
                rows = load_data(path)
                total += rows
                print(f"Loaded {file}: {rows}")
            except Exception as e:
                print(f"Error loading {file}: {e}")

    print(f"\nTOTAL LOADED: {total}")


if __name__ == "__main__":
    # Running this file directly imports all files inside the names folder.
    load_all_data("names")
