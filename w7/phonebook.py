import csv
from connect import connect, create_table


def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            username, phone = row[0], row[1]

            cur.execute("""
                INSERT INTO phonebook (username, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (username, phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Data imported from CSV.")


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO phonebook (username, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING
    """, (username, phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


def update_user():
    current_phone = input("Enter current phone of user to update: ")
    new_username = input("Enter new username: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        UPDATE phonebook
        SET username = %s, phone = %s
        WHERE phone = %s
    """, (new_username, new_phone, current_phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")


def query_data():
    print("1 - Show all")
    print("2 - Search by username")
    print("3 - Search by phone")
    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        username = input("Enter username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))
    elif choice == "3":
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_data():
    print("1 - Delete by username")
    print("2 - Delete by phone")
    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        username = input("Enter username: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        cur.close()
        conn.close()
        return

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")


def menu():
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert data from CSV")
        print("2. Insert data from console")
        print("3. Update user data")
        print("4. Query data")
        print("5. Delete data")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_user()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()