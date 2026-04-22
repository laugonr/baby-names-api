import sqlite3

DB_NAME = "babynames.db"

def load_data(file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        with open(file_path, "r") as file:
            for line in file:
                name, gender, count = line.strip().split(",")
                year = int(file_path[-8:-4])

                cursor.execute("""
                    INSERT INTO baby_names (name, year, gender, count)
                    VALUES (?, ?, ?, ?)
                """, (name, year, gender, int(count)))

        conn.commit()
        print("Data loaded successfully!")

    except FileNotFoundError:
        print("File not found. Check the file path.")

    finally:
        conn.close()