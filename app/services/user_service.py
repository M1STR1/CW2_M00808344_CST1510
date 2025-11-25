import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user', db_path=None):
    conn = connect_database(db_path) if db_path else connect_database()
    create_users_table(conn)
    if get_user_by_username(username, db_path):
        conn.close()
        return False, f"Username '{username}' already exists."
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    insert_user(username, pw_hash, role, db_path)
    conn.close()
    return True, f"User '{username}' registered successfully."

def login_user(username, password, db_path=None):
    user = get_user_by_username(username, db_path)
    if not user:
        return False, "User not found."
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful."
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt', db_path=None):
    path = Path(filepath)
    conn = connect_database(db_path) if db_path else connect_database()
    create_users_table(conn)
    if not path.exists():
        conn.close()
        return 0
    migrated = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 2:
                username = parts[0].strip()
                password_hash = parts[1].strip()
                role = parts[2].strip() if len(parts) > 2 else 'user'
                try:
                    cursor = conn.cursor()
                    cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                   (username, password_hash, role))
                    if cursor.rowcount > 0:
                        migrated += 1
                except sqlite3.Error:
                    pass
    conn.commit()
    conn.close()
    return migrated