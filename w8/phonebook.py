import csv
from connect import connect, create_table


def execute_sql_file(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        print(f"{filename} executed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error executing {filename}: {e}")
    finally:
        cur.close()
        conn.close()


def setup_database_objects():
    create_table()
    execute_sql_file("functions.sql")
    execute_sql_file("procedures.sql")


def insert_from_console():
    name = input("Enter name: ").strip()
    surname = input("Enter surname: ").strip()
    phone = input("Enter phone: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s, %s)", (name, surname, phone))
        conn.commit()
        print("Contact inserted or updated.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_csv():
    names = []
    surnames = []
    phones = []

    try:
        with open("contacts.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) < 3:
                    continue
                names.append(row[0].strip())
                surnames.append(row[1].strip())
                phones.append(row[2].strip())

    except FileNotFoundError:
        print("contacts.csv not found.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_contacts(%s, %s, %s, %s)",
            (names, surnames, phones, [])
        )
        conn.commit()
        print("Bulk insert completed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

    # локально покажем некорректные данные
    show_invalid_contacts(names, surnames, phones)


def show_invalid_contacts(names, surnames, phones):
    invalid = []

    for n, s, p in zip(names, surnames, phones):
        if n == "" or s == "" or p == "":
            invalid.append((n, s, p))
            continue

        allowed = set("0123456789+-() ")
        if not (5 <= len(p) <= 20 and all(ch in allowed for ch in p)):
            invalid.append((n, s, p))

    if invalid:
        print("\nIncorrect data:")
        for item in invalid:
            print(item)
    else:
        print("\nNo incorrect data found.")


def search_by_pattern():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No matches found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def query_with_pagination():
    try:
        limit_count = int(input("LIMIT: "))
        offset_count = int(input("OFFSET: "))
    except ValueError:
        print("Must be integers.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM get_phonebook_page(%s, %s)",
            (limit_count, offset_count)
        )
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No data.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_data():
    value = input("Enter name/surname/phone to delete: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Deleted if existed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM phonebook ORDER BY id")
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("Empty.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    setup_database_objects()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert one contact")
        print("2. Insert from CSV")
        print("3. Search (pattern)")
        print("4. Pagination")
        print("5. Delete")
        print("6. Show all")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            query_with_pagination()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            show_all_contacts()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()