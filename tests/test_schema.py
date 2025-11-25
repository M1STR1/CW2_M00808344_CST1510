import sqlite3
from app.data.db import connect_database
from app.data.schema import create_all_tables

def test_create_tables(tmp_path):
    db_file = tmp_path / "test.db"
    conn = connect_database(db_file)
    create_all_tables(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert "users" in tables
    assert "cyber_incidents" in tables
    assert "datasets_metadata" in tables
    assert "it_tickets" in tables
    conn.close()