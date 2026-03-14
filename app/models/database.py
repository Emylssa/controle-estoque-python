import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / 'estoque.db'
SQL_PATH = BASE_DIR / 'database.sql'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
