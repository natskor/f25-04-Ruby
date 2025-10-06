import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent.parent / "auth.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def create_user(username: str, email: str, password_hash: str) -> Optional[str]:
    """Returns None on success, else an error string suitable for UI."""
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?,?,?)",
            (username.strip(), email.strip().lower(), password_hash),
        )
        conn.commit()
        return None
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if "username" in msg:
            return "That username is already taken."
        if "email" in msg:
            return "That email is already registered."
        return "Account already exists."
    finally:
        conn.close()

def find_user_by_email(email: str):
    conn = get_db()
    try:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
        return cur.fetchone()
    finally:
        conn.close()
