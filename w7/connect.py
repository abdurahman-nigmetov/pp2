import psycopg2
from config import load_config


def connect():
    config = load_config()
    return psycopg2.connect(**config)


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()