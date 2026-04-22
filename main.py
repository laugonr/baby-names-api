from database import create_table, get_connection
from load_data import load_data
import sqlite3

DB_NAME = "babynames.db"


def validate_name(name):
    """Validate name input"""
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    return name.strip().title()


def validate_year(year_str):
    """Validate year input"""
    try:
        year = int(year_str)
        if year < 1880 or year > 2026:  # SSA data starts around 1880
            raise ValueError("Year must be between 1880 and 2026")
        return year
    except ValueError:
        if year_str.strip().isdigit():
            raise ValueError("Year must be between 1880 and 2026")
        raise ValueError("Year must be a valid number")


def validate_gender(gender):
    """Validate gender input"""
    gender = gender.upper()
    if gender not in ['M', 'F']:
        raise ValueError("Gender must be 'M' or 'F'")
    return gender


def validate_count(count_str):
    """Validate count input"""
    try:
        count = int(count_str)
        if count < 0:
            raise ValueError("Count cannot be negative")
        return count
    except ValueError:
        raise ValueError("Count must be a valid number")


def add_name():
    """Add a new name to the database"""
    try:
        name = validate_name(input("Enter name: "))
        year = validate_year(input("Enter year: "))
        gender = validate_gender(input("Enter gender (M/F): "))
        count = validate_count(input("Enter count: "))

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO baby_names (name, year, gender, count)
                VALUES (?, ?, ?, ?)
            """, (name, year, gender, count))
            conn.commit()

        print(f"SUCCESS: Added {name} ({gender}, {year}) with count {count}")

    except ValueError as e:
        print(f"ERROR: Error: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def search_name():
    """Search for names in the database"""
    try:
        name = validate_name(input("Enter name to search: "))

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM baby_names WHERE name = ?", (name,))
            results = cursor.fetchall()

        if not results:
            print(f"No records found for '{name}'")
            return

        print(f"\nRecords for '{name}':")
        print("-" * 50)
        for row in results:
            print(f"ID: {row[0]}, Year: {row[2]}, Gender: {row[3]}, Count: {row[4]}")

    except ValueError as e:
        print(f"ERROR: Error: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def update_name():
    """Update a name's count in the database"""
    try:
        name = validate_name(input("Enter name to update: "))
        new_count = validate_count(input("Enter new count: "))

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE baby_names
                SET count = ?
                WHERE name = ?
            """, (new_count, name))

            if cursor.rowcount == 0:
                print(f"ERROR: No records found for '{name}'")
            else:
                conn.commit()
                print(f"SUCCESS: Updated {cursor.rowcount} record(s) for '{name}' to count {new_count}")

    except ValueError as e:
        print(f"ERROR: Error: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def delete_name():
    """Delete a name from the database"""
    try:
        name = validate_name(input("Enter name to delete: "))

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete all records for '{name}'? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled")
            return

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM baby_names WHERE name = ?", (name,))
            deleted_count = cursor.rowcount
            conn.commit()

        if deleted_count == 0:
            print(f"ERROR: No records found for '{name}'")
        else:
            print(f"SUCCESS: Deleted {deleted_count} record(s) for '{name}'")

    except ValueError as e:
        print(f"ERROR: Error: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def load_ssa_data():
    """Load SSA data from file"""
    try:
        file_path = input("Enter SSA file path: ").strip()
        if not file_path:
            print("ERROR: File path cannot be empty")
            return

        load_data(file_path)
        print(f"SUCCESS: Data loaded from {file_path}")

    except Exception as e:
        print(f"ERROR: Error loading data: {e}")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*40)
    print("      Baby Name Database Manager")
    print("="*40)
    print("1. Load SSA data")
    print("2. Add a new name")
    print("3. Search for a name")
    print("4. Update a name record")
    print("5. Delete a name record")
    print("6. Exit")
    print("-"*40)


def menu():
    """Main menu loop"""
    create_table()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            load_ssa_data()
        elif choice == "2":
            add_name()
        elif choice == "3":
            search_name()
        elif choice == "4":
            update_name()
        elif choice == "5":
            delete_name()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("ERROR: Invalid choice. Please enter 1-6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()
