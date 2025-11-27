import bcrypt
from app.data.db import connect_database

# Basic user helpers using sqlite3 and bcrypt

def create_user(conn, username: str, password: str, role: str = "user"):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, pw_hash, role))
        conn.commit()
        return True
    except Exception:
        return False


def verify_user(conn, username: str, password: str):
    cur = conn.cursor()
    cur.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False, None
    pw_hash = row[0]
    role = row[1]
    try:
        if bcrypt.checkpw(password.encode(), pw_hash):
            return True, role
        return False, None
    except Exception:
        return False, None


def get_user_role(conn, username: str):
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    return row[0] if row else None
