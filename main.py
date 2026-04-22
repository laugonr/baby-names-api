from database import create_table
from load_data import load_data
import sqlite3

DB_NAME = "babynames.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def add_name():
    name = input("Enter name: ")
    year = int(input("Enter year: "))
    gender = input("Enter gender (M/F): ")
    count = int(input("Enter count: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO baby_names (name, year, gender, count)
        VALUES (?, ?, ?, ?)
    """, (name, year, gender, count))

    conn.commit()
    conn.close()

    print("Name added!")


def search_name():
    name = input("Enter name to search: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM baby_names WHERE name = ?", (name,))
    results = cursor.fetchall()

    conn.close()

    for row in results:
        print(row)


def update_name():
    name = input("Enter name to update: ")
    new_count = int(input("Enter new count: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE baby_names
        SET count = ?
        WHERE name = ?
    """, (new_count, name))

    conn.commit()
    conn.close()

    print("Updated!")


def delete_name():
    name = input("Enter name to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM baby_names WHERE name = ?", (name,))

    conn.commit()
    conn.close()

    print("Deleted!")


def menu():
    create_table()

    while True:
        print("\n=== Baby Name Database ===")
        print("1. Load SSA data")
        print("2. Add a new name")
        print("3. Search for a name")
        print("4. Update a name record")
        print("5. Delete a name record")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            file_path = input("Enter SSA file path: ")
            load_data(file_path)

        elif choice == "2":
            add_name()

        elif choice == "3":
            search_name()

        elif choice == "4":
            update_name()

        elif choice == "5":
            delete_name()

        elif choice == "6":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()