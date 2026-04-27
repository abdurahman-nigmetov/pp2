import json
from pathlib import Path

from connect import connect, create_tables

DEFAULT_SETTINGS = {
    "snake_color": [0, 0, 255],
    "grid": True,
    "sound": True,
}

SNAKE_COLOR_PRESETS = [
    (0, 0, 255),
    (0, 180, 0),
    (220, 40, 40),
    (255, 140, 0),
    (255, 255, 255),
]


def _load_json(path: Path, fallback):
    if not path.exists():
        return fallback

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return fallback


def _save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def _sanitize_rgb(value, fallback):
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        return list(fallback)

    cleaned = []
    for channel in value:
        try:
            channel_int = int(channel)
        except (TypeError, ValueError):
            return list(fallback)

        cleaned.append(max(0, min(255, channel_int)))

    return cleaned


def load_settings(base_dir: Path):
    settings_path = base_dir / "settings.json"
    raw = _load_json(settings_path, DEFAULT_SETTINGS.copy())

    settings = DEFAULT_SETTINGS.copy()
    settings["snake_color"] = _sanitize_rgb(raw.get("snake_color", settings["snake_color"]), settings["snake_color"])
    settings["grid"] = bool(raw.get("grid", settings["grid"]))
    settings["sound"] = bool(raw.get("sound", settings["sound"]))

    _save_json(settings_path, settings)
    return settings


def save_settings(base_dir: Path, settings):
    settings_path = base_dir / "settings.json"
    clean = DEFAULT_SETTINGS.copy()

    clean["snake_color"] = _sanitize_rgb(settings.get("snake_color", clean["snake_color"]), clean["snake_color"])
    clean["grid"] = bool(settings.get("grid", clean["grid"]))
    clean["sound"] = bool(settings.get("sound", clean["sound"]))

    _save_json(settings_path, clean)
    return clean


def prepare_database(base_dir: Path):
    try:
        create_tables(base_dir)
        return True
    except Exception:
        return False


def get_personal_best(base_dir: Path, username: str):
    safe_name = (username or "").strip() or "Player"

    try:
        conn = connect(base_dir)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE p.username = %s;
            """,
            (safe_name,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return int(row[0]) if row else 0
    except Exception:
        return 0


def save_game_result(base_dir: Path, username: str, score: int, level_reached: int):
    safe_name = (username or "").strip() or "Player"

    try:
        conn = connect(base_dir)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO players (username)
            VALUES (%s)
            ON CONFLICT (username) DO NOTHING;
            """,
            (safe_name,),
        )

        cur.execute("SELECT id FROM players WHERE username = %s;", (safe_name,))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            cur.close()
            conn.close()
            return False

        player_id = int(row[0])

        cur.execute(
            """
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s);
            """,
            (player_id, max(0, int(score)), max(1, int(level_reached))),
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


def load_leaderboard(base_dir: Path, limit: int = 10):
    try:
        conn = connect(base_dir)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at DESC
            LIMIT %s;
            """,
            (max(1, int(limit)),),
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = []
        for row in rows:
            data.append(
                {
                    "username": str(row[0]),
                    "score": int(row[1]),
                    "level": int(row[2]),
                    "played_at": row[3],
                }
            )

        return data
    except Exception:
        return []
