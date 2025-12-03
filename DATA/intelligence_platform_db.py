# intelligence_platform_db.py
import sqlite3
from sqlite3 import Connection
from typing import List, Dict, Any

DB_NAME = "intelligence_platform.db"

def create_connection(db_name: str = DB_NAME) -> Connection:
    """
    Create a database connection to the SQLite database.
    """
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    return conn

def create_tables(conn: Connection):
    """
    Create the main tables for the intelligence platform.
    """
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Intelligence reports table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        author_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(author_id) REFERENCES users(id)
    )
    """)
    
    # Threat alerts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT NOT NULL,
        description TEXT,
        severity TEXT,
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()

# ---------------- CRUD FUNCTIONS ---------------- #

def insert_user(conn: Connection, username: str, email: str, role: str) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email, role) VALUES (?, ?, ?)", (username, email, role))
    conn.commit()
    return cur.lastrowid

def get_all_users(conn: Connection) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def insert_report(conn: Connection, title: str, description: str, author_id: int) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO reports (title, description, author_id) VALUES (?, ?, ?)",
                (title, description, author_id))
    conn.commit()
    return cur.lastrowid

def get_all_reports(conn: Connection) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

def insert_alert(conn: Connection, alert_type: str, description: str, severity: str) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO alerts (alert_type, description, severity) VALUES (?, ?, ?)",
                (alert_type, description, severity))
    conn.commit()
    return cur.lastrowid

def get_all_alerts(conn: Connection) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(row) for row in rows]

# ---------------- UTILITY ---------------- #

def close_connection(conn: Connection):
    if conn:
        conn.close()

# ---------------- TESTING ---------------- #
if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    
    # Example inserts
    user_id = insert_user(conn, "agent007", "james.bond@mi6.co.uk", "Analyst")
    report_id = insert_report(conn, "Suspicious Activity", "Observed unusual network traffic.", user_id)
    alert_id = insert_alert(conn, "Phishing", "Multiple phishing emails detected.", "High")
    
    print("Users:", get_all_users(conn))
    print("Reports:", get_all_reports(conn))
    print("Alerts:", get_all_alerts(conn))
    
    close_connection(conn)
