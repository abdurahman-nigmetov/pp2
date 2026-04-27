from pathlib import Path

import psycopg2

from config import load_config


def connect(base_dir: Path):
    config = load_config(filename=str(base_dir / "database.ini"))
    return psycopg2.connect(**config)


def create_tables(base_dir: Path):
    conn = connect(base_dir)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
            """
        )

        conn.commit()
    finally:
        cur.close()
        conn.close()