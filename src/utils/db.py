import sqlite3
from pathlib import Path

# Resolve project root regardless of where script is run from
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "output" / "asana_simulation.sqlite"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn
