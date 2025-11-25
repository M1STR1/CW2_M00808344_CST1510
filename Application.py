import bcrypt
import re
import getpass
import json
import time
import os
import secrets
from typing import Optional, Tuple

# default files under DATA for testability
DATA_DIR = os.path.join(os.getcwd(), "DATA")
os.makedirs(DATA_DIR, exist_ok=True)
LOCKOUT_FILE = os.path.join(DATA_DIR, "lockouts.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")

MAX_FAILED = 5
LOCKOUT_SECONDS = 300        # default lockout seconds (5 minutes)
SESSION_SECONDS = 3600       # default session lifetime (1 hour)


def _load_json(path: str):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_json(path: str, data):
    # atomic save using temp file + rename
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, path)


def _get_lockout(username: str, lockout_file: str = LOCKOUT_FILE):
    data = _load_json(lockout_file)
    return data.get(username, {"failed": 0, "locked_until": 0})


def _set_lockout(username: str, record: dict, lockout_file: str = LOCKOUT_FILE):
    data = _load_json(lockout_file)
    data[username] = record
    _save_json(lockout_file, data)


def _reset_lockout(username: str, lockout_file: str = LOCKOUT_FILE):
    data = _load_json(lockout_file)
    if username in data:
        data.pop(username, None)
        _save_json(lockout_file, data)


def _create_session(username: str, role: str = "user", sessions_file: str = SESSIONS_FILE, session_seconds: int = SESSION_SECONDS):
    sessions = _load_json(sessions_file)
    token = secrets.token_hex(16)
    now = int(time.time())
    sessions[token] = {
        "username": username,
        "role": role,
        "created_at": now,
        "expires_at": now + session_seconds,
    }
    _save_json(sessions_file, sessions)
    return token


def validate_session(token: str, sessions_file: str = SESSIONS_FILE):
    sessions = _load_json(sessions_file)
    record = sessions.get(token)
    if not record:
        return False
    if int(time.time()) > record.get("expires_at", 0):
        sessions.pop(token, None)
        _save_json(sessions_file, sessions)
        return False
    return True


def get_session_user(token: str, sessions_file: str = SESSIONS_FILE) -> Tuple[Optional[str], Optional[str]]:
    sessions = _load_json(sessions_file)
    record = sessions.get(token)
    if record and int(time.time()) <= record.get("expires_at", 0):
        return record.get("username"), record.get("role")
    return None, None


def end_session(token: str, sessions_file: str = SESSIONS_FILE):
    sessions = _load_json(sessions_file)
    if token in sessions:
        sessions.pop(token, None)
        _save_json(sessions_file, sessions)
        return True
    return False


def hash_password(password: str) -> str:
    """Return bcrypt hash string for provided password."""
    binary_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(binary_password, salt)
    return hashed.decode('utf-8')


def validate_hash(password: str, hash_str: str) -> bool:
    """Validate password against bcrypt hash string."""
    hashed_bytes = hash_str.encode('utf-8')
    bin_password = password.encode('utf-8')
    return bcrypt.checkpw(bin_password, hashed_bytes)


def password_strength(password: str) -> Tuple[int, str]:
    if not password:
        return 0, "Very Weak"
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[^\w\s]", password):
        score += 1
    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Strong",
        5: "Very Strong"
    }
    return score, labels.get(score, "Unknown")


def print_strength_bar(score: int):
    total = 5
    filled = "#" * score
    empty = "-" * (total - score)
    print(f"Strength: [{filled}{empty}] ({score}/5)")


def register_user(name: Optional[str] = None, password: Optional[str] = None,
                  role: str = "user", users_file: str = "users.txt"):
    """
    Register a user.
    If name and password are provided, runs non-interactively.
    Else uses interactive prompts.
    Stores users in CSV-friendly users_file as: name,role,hash
    """
    if name is None:
        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return False
    if password is None:
        password = getpass.getpass("Enter your password (input hidden): ")

    score, label = password_strength(password)
    print_strength_bar(score)
    print(f"Rating: {label}")

    if score < 1:
        print("Password too weak.")
        return False

    hashed = hash_password(password)
    with open(users_file, "a", encoding="utf-8") as f:
        f.write(f"{name},{role},{hashed}\n")
    _reset_lockout(name)
    return True


def login_user(username: Optional[str] = None, password: Optional[str] = None,
               users_file: str = "users.txt",
               lockout_file: str = LOCKOUT_FILE,
               sessions_file: str = SESSIONS_FILE,
               max_failed: int = MAX_FAILED,
               lockout_seconds: int = LOCKOUT_SECONDS,
               session_seconds: int = SESSION_SECONDS):
    """
    Login a user.
    - If username and password are not supplied, falls back to interactive prompts.
    - Returns:
        token (str) on success,
        "locked" | "notfound" | "invalid" on failure.
    """
    if username is None:
        username = input("Enter your name: ").strip()
    if password is None:
        password = getpass.getpass("Enter your password: ")

    # check lockout
    lock = _get_lockout(username, lockout_file)
    now = int(time.time())
    if lock.get("locked_until", 0) > now:
        return "locked"

    # read user list
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            users = f.readlines()
    except FileNotFoundError:
        return "notfound"

    found = False
    for user in users:
        parts = user.strip().split(",", 2)
        if len(parts) == 3:
            name_, role, hash_str = parts
        elif len(parts) == 2:
            name_, hash_str = parts
            role = "user"
        else:
            continue

        if name_ == username:
            found = True
            if validate_hash(password, hash_str):
                _reset_lockout(username, lockout_file)
                token = _create_session(username, role, sessions_file, session_seconds)
                return token
            else:
                failed = lock.get("failed", 0) + 1
                locked_until = 0
                if failed >= max_failed:
                    locked_until = int(time.time()) + lockout_seconds
                _set_lockout(username, {"failed": failed, "locked_until": locked_until}, lockout_file)
                return "invalid"

    if not found:
        return "notfound"
