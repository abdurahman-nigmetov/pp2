import csv
import json
from datetime import datetime
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


def parse_birthday(value):
    value = value.strip()
    if value == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None


def get_group_id_by_choice(choice):
    mapping = {
        "1": 1,  # Family
        "2": 2,  # Work
        "3": 3,  # Friend
        "4": 4,  # Other
    }
    return mapping.get(choice, 4)


def insert_contact():
    name = input("Enter name: ").strip()
    surname = input("Enter surname: ").strip()
    email = input("Enter email: ").strip()
    birthday = parse_birthday(input("Enter birthday (YYYY-MM-DD or empty): "))
    group_choice = input(
        "Enter group number:\n"
        "1. Family\n"
        "2. Work\n"
        "3. Friend\n"
        "4. Other\n"
        "Choose: "
    ).strip()

    group_id = get_group_id_by_choice(group_choice)

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL upsert_contact(%s, %s, %s, %s, %s)",
            (name, surname, email or None, birthday, group_id)
        )
        conn.commit()
        print("Contact inserted or updated.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def add_phone():
    contact_name = input("Enter contact name: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter phone type (home/work/mobile): ").strip().lower()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def move_to_group():
    contact_name = input("Enter contact name: ").strip()
    group_name = input("Enter new group name: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        conn.commit()
        print("Contact moved to group.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_csv():
    names = []
    surnames = []
    emails = []
    birthdays = []
    group_ids = []

    try:
        with open("contacts.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = (row.get("name") or "").strip()
                surname = (row.get("surname") or "").strip()
                email = (row.get("email") or "").strip()
                birthday_raw = (row.get("birthday") or "").strip()
                group_name = (row.get("group") or "Other").strip().lower()

                if group_name == "family":
                    group_id = 1
                elif group_name == "work":
                    group_id = 2
                elif group_name == "friend":
                    group_id = 3
                else:
                    group_id = 4

                birthday = parse_birthday(birthday_raw) if birthday_raw else None

                names.append(name)
                surnames.append(surname)
                emails.append(email)
                birthdays.append(birthday)
                group_ids.append(group_id)

    except FileNotFoundError:
        print("contacts.csv not found.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_contacts(%s, %s, %s, %s, %s, %s)",
            (names, surnames, emails, birthdays, group_ids, [])
        )
        conn.commit()
        print("Bulk insert completed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()

    # add phones from CSV one by one
    try:
        with open("contacts.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            conn = connect()
            cur = conn.cursor()
            try:
                for row in reader:
                    name = (row.get("name") or "").strip()
                    phone = (row.get("phone") or "").strip()
                    phone_type = (row.get("type") or "mobile").strip().lower()

                    if phone:
                        try:
                            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
                        except Exception:
                            conn.rollback()
                            conn = connect()
                            cur = conn.cursor()
                conn.commit()
            finally:
                cur.close()
                conn.close()
    except FileNotFoundError:
        pass


def search_by_pattern():
    pattern = input("Enter search pattern: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
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


def filter_by_group():
    group_name = input("Enter group name: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                p.id,
                p.name,
                p.surname,
                p.email,
                p.birthday,
                g.name AS group_name,
                COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
            LEFT JOIN phones ph ON p.id = ph.contact_id
            WHERE g.name ILIKE %s
            GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name
            ORDER BY p.id
        """, (group_name,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No contacts in this group.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def sort_contacts():
    sort_field = input("Sort by (name/birthday/date): ").strip().lower()

    if sort_field not in ("name", "birthday", "date"):
        print("Invalid sort field.")
        return

    if sort_field == "name":
        order_sql = "ORDER BY p.name, p.surname"
    elif sort_field == "birthday":
        order_sql = "ORDER BY p.birthday NULLS LAST, p.name"
    else:
        order_sql = "ORDER BY p.created_at DESC"

    conn = connect()
    cur = conn.cursor()
    try:
        query = f"""
            SELECT
                p.id,
                p.name,
                p.surname,
                p.email,
                p.birthday,
                g.name AS group_name,
                p.created_at,
                COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
            LEFT JOIN phones ph ON p.id = ph.contact_id
            GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name, p.created_at
            {order_sql}
        """
        cur.execute(query)
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


def query_with_pagination():
    try:
        limit_count = int(input("Page size: "))
    except ValueError:
        print("Must be integers.")
        return

    offset_count = 0

    conn = connect()
    cur = conn.cursor()
    try:
        while True:
            cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit_count, offset_count))
            rows = cur.fetchall()

            if rows:
                print(f"\n--- PAGE (OFFSET {offset_count}) ---")
                for row in rows:
                    print(row)
            else:
                print("No data.")

            command = input("Command (next/prev/quit): ").strip().lower()
            if command == "next":
                offset_count += limit_count
            elif command == "prev":
                offset_count = max(0, offset_count - limit_count)
            elif command == "quit":
                break
            else:
                print("Invalid command.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_data():
    value = input("Enter name/surname/email to delete: ").strip()

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
        cur.execute("""
            SELECT
                p.id,
                p.name,
                p.surname,
                p.email,
                p.birthday,
                g.name AS group_name,
                p.created_at,
                COALESCE(string_agg(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.id), '')
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
            LEFT JOIN phones ph ON p.id = ph.contact_id
            GROUP BY p.id, p.name, p.surname, p.email, p.birthday, g.name, p.created_at
            ORDER BY p.id
        """)
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


def export_to_json():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                p.id,
                p.name,
                p.surname,
                p.email,
                p.birthday,
                g.name AS group_name,
                p.created_at
            FROM phonebook p
            LEFT JOIN groups g ON p.group_id = g.id
            ORDER BY p.id
        """)
        contacts = cur.fetchall()

        result = []
        for contact in contacts:
            contact_id = contact[0]
            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
                ORDER BY id
            """, (contact_id,))
            phones = [{"phone": row[0], "type": row[1]} for row in cur.fetchall()]

            result.append({
                "id": contact[0],
                "name": contact[1],
                "surname": contact[2],
                "email": contact[3],
                "birthday": str(contact[4]) if contact[4] else None,
                "group": contact[5],
                "created_at": str(contact[6]) if contact[6] else None,
                "phones": phones
            })

        with open("contacts_export.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        print("Exported to contacts_export.json")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def import_from_json():
    try:
        with open("contacts_export.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("contacts_export.json not found.")
        return

    conn = connect()
    cur = conn.cursor()
    try:
        for item in data:
            name = item.get("name")
            surname = item.get("surname")
            email = item.get("email")
            birthday = item.get("birthday")
            group_name = item.get("group") or "Other"
            phones = item.get("phones", [])

            cur.execute("""
                SELECT id
                FROM phonebook
                WHERE name = %s AND surname = %s
                ORDER BY id
                LIMIT 1
            """, (name, surname))
            existing = cur.fetchone()

            if existing:
                action = input(f'Contact "{name} {surname}" exists. skip or overwrite? ').strip().lower()
                if action == "skip":
                    continue
                elif action == "overwrite":
                    cur.execute("DELETE FROM phonebook WHERE id = %s", (existing[0],))
                else:
                    print("Skipped.")
                    continue

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group_name,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute(
                "CALL upsert_contact(%s, %s, %s, %s, %s)",
                (name, surname, email, birthday, group_id)
            )

            for phone_item in phones:
                try:
                    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone_item["phone"], phone_item["type"]))
                except Exception:
                    conn.rollback()
                    conn = connect()
                    cur = conn.cursor()

        conn.commit()
        print("Imported from contacts_export.json")
    except Exception as e:
        conn.rollback()
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
        print("3. Search")
        print("4. Pagination")
        print("5. Delete")
        print("6. Show all")
        print("7. Add phone")
        print("8. Move to group")
        print("9. Filter by group")
        print("10. Sort contacts")
        print("11. Export to JSON")
        print("12. Import from JSON")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            insert_contact()
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
        elif choice == "7":
            add_phone()
        elif choice == "8":
            move_to_group()
        elif choice == "9":
            filter_by_group()
        elif choice == "10":
            sort_contacts()
        elif choice == "11":
            export_to_json()
        elif choice == "12":
            import_from_json()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()