import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user'):
    """Register a new user with hased password."""
    # hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # verify password
    stored_hash = user[2] # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'),
stored_hash.encode('utf-8')):
        return True, f"Login successful for user '{username}'."
    else:
        return False, "Incorrect password."

def migrate_users_from_file(file_path='DATA/users.txt'):
    """Migrate users from a text file to the database."""
    # ... migration logic ...