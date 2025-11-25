from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.db import connect_database
from app.data.schema import create_users_table
import tempfile
from pathlib import Path

def test_register_and_login(tmp_path):
    db_file = tmp_path / "users.db"
    conn = connect_database(db_file)
    create_users_table(conn)
    conn.close()

    success, msg = register_user("alice", "S3cureP@ss", "analyst", db_file)
    assert success

    ok, message = login_user("alice", "S3cureP@ss", db_file)
    assert ok

    bad, message = login_user("alice", "wrong", db_file)
    assert not bad
    assert message == "Incorrect password."

def test_migrate_users(tmp_path):
    db_file = tmp_path / "migrate.db"
    conn = connect_database(db_file)
    create_users_table(conn)
    conn.close()

    users_txt = tmp_path / "users.txt"
    users_txt.write_text("bob,$2b$12$invalidhash,analyst\n")
    migrated = migrate_users_from_file(str(users_txt), db_file)
    assert migrated >= 1