import psycopg2
from config import load_config


def connect():
    config = load_config()
    return psycopg2.connect(**config)


def create_table():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                surname VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            ALTER TABLE phonebook
            ADD COLUMN IF NOT EXISTS email VARCHAR(100),
            ADD COLUMN IF NOT EXISTS birthday DATE,
            ADD COLUMN IF NOT EXISTS group_id INTEGER;
        """)

        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.table_constraints
                    WHERE constraint_name = 'phonebook_group_id_fkey'
                ) THEN
                    ALTER TABLE phonebook
                    ADD CONSTRAINT phonebook_group_id_fkey
                    FOREIGN KEY (group_id) REFERENCES groups(id);
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
                phone VARCHAR(20) UNIQUE NOT NULL,
                type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
            );
        """)

        cur.execute("""
            INSERT INTO groups(name)
            VALUES
                ('Family'),
                ('Work'),
                ('Friend'),
                ('Other')
            ON CONFLICT (name) DO NOTHING;
        """)

        conn.commit()
    finally:
        cur.close()
        conn.close()