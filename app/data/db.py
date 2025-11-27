import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("DATA/intelligence_platform.db")


def connect_database(db_path: Optional[str] = None):
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None):
    conn = connect_database(db_path)
    cur = conn.cursor()


# Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
    )
    """)


# Create incidents table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    severity TEXT,
    status TEXT,
    date TEXT
    )
    """)


# Datasets metadata
    cur.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    source TEXT,
    category TEXT,
    size INTEGER
    )
    """)


# IT tickets
    cur.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    priority TEXT,
    status TEXT,
    created_date TEXT
    )
    """)


    conn.commit()
    return conn