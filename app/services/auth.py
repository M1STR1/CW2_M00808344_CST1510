from app.data.db import connect_database
from app.data.users import create_user, verify_user, get_user_role


# High-level helpers used by Streamlit pages


def register_user(username, password, role='user', db_path=None):
    conn = connect_database(db_path)
    return create_user(conn, username, password, role)


def login_user(username, password, db_path=None):
    conn = connect_database(db_path)
    ok, role = verify_user(conn, username, password)
    return ok, role


def user_role(username, db_path=None):
    conn = connect_database(db_path)
    return get_user_role(conn, username)
