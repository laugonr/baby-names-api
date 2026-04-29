from database import create_table, get_connection
from load_data import load_data
from validation import validate_count, validate_gender, validate_name, validate_year
import sqlite3


def prompt_record(include_count=False):
    """Ask the user for name, year, gender, and optionally count."""
    record = [
        validate_name(input("Enter name: ")),
        validate_year(input("Enter year: ")),
        validate_gender(input("Enter gender (M/F): "))
    ]
    if include_count:
        record.append(validate_count(input("Enter count: ")))
    return record


def add_name():
    """Add a new name to the database."""
    try:
        # Collect and validate the fields before inserting.
        name, year, gender, count = prompt_record(include_count=True)
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO baby_names (name, year, gender, count)
                VALUES (?, ?, ?, ?)
            """, (name, year, gender, count))
        print(f"SUCCESS: Added {name} ({gender}, {year}) with count {count}")
    except ValueError as e:
        print(f"ERROR: {e}")
    except sqlite3.IntegrityError:
        print("ERROR: That name, year, and gender already exists")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def search_name():
    """Search for names in the database."""
    try:
        # Search by name and show every matching year/gender record.
        name = validate_name(input("Enter name to search: "))

        with get_connection() as conn:
            results = conn.execute("""
                SELECT id, name, year, gender, count
                FROM baby_names
                WHERE name = ?
                ORDER BY year, gender
            """, (name,)).fetchall()

        if not results:
            print(f"No records found for '{name}'")
            return

        print(f"\nRecords for '{name}':")
        print("-" * 50)
        for row in results:
            print(f"ID: {row[0]}, Year: {row[2]}, Gender: {row[3]}, Count: {row[4]}")

    except ValueError as e:
        print(f"ERROR: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def update_name():
    """Update a name's count in the database."""
    try:
        # The name/year/gender combination finds exactly one record.
        name, year, gender = prompt_record()
        new_count = validate_count(input("Enter new count: "))

        with get_connection() as conn:
            cursor = conn.execute("""
                UPDATE baby_names
                SET count = ?
                WHERE name = ? AND year = ? AND gender = ?
            """, (new_count, name, year, gender))

            if cursor.rowcount == 0:
                print(f"ERROR: No record found for '{name}' ({gender}, {year})")
            else:
                conn.commit()
                print(f"SUCCESS: Updated '{name}' ({gender}, {year}) to count {new_count}")

    except ValueError as e:
        print(f"ERROR: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def delete_name():
    """Delete a name from the database."""
    try:
        # Ask for the exact record, then confirm before deleting it.
        name, year, gender = prompt_record()

        confirm = input(f"Are you sure you want to delete '{name}' ({gender}, {year})? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled")
            return

        with get_connection() as conn:
            cursor = conn.execute("""
                DELETE FROM baby_names
                WHERE name = ? AND year = ? AND gender = ?
            """, (name, year, gender))
            deleted_count = cursor.rowcount

        if deleted_count == 0:
            print(f"ERROR: No record found for '{name}' ({gender}, {year})")
        else:
            print(f"SUCCESS: Deleted '{name}' ({gender}, {year})")

    except ValueError as e:
        print(f"ERROR: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")


def load_ssa_data():
    """Load SSA data from file"""
    try:
        # Example file name: names/yob2024.txt
        file_path = input("Enter SSA file path: ").strip()
        if not file_path:
            print("ERROR: File path cannot be empty")
            return

        imported_rows = load_data(file_path)
        print(f"SUCCESS: Loaded {imported_rows} records from {file_path}")

    except FileNotFoundError:
        print("ERROR: File not found. Check the file path.")
    except ValueError as e:
        print(f"ERROR: {e}")
    except OSError as e:
        print(f"ERROR: File error: {e}")
    except sqlite3.Error as e:
        print(f"ERROR: Database error: {e}")
    except Exception as e:
        print(f"ERROR: Error loading data: {e}")


def display_menu():
    """Display the main menu"""
    # This is the text menu users see in the terminal.
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
    # Create the table once before the user starts choosing actions.
    create_table()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        # Route the user's menu choice to the correct function.
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
