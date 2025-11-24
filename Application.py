import bcrypt
import re
import getpass
import json
import time
import os
import secrets

LOCKOUT_FILE = "lockouts.json"
SESSIONS_FILE = "sessions.json"
MAX_FAILED = 5
LOCKOUT_SECONDS = 300        # 5 minutes
SESSION_SECONDS = 3600      # 1 hour

def _load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def _get_lockout(username):
    data = _load_json(LOCKOUT_FILE)
    return data.get(username, {"failed": 0, "locked_until": 0})

def _set_lockout(username, record):
    data = _load_json(LOCKOUT_FILE)
    data[username] = record
    _save_json(LOCKOUT_FILE, data)

def _reset_lockout(username):
    data = _load_json(LOCKOUT_FILE)
    if username in data:
        data.pop(username, None)
        _save_json(LOCKOUT_FILE, data)

def _create_session(username, role):
    sessions = _load_json(SESSIONS_FILE)
    token = secrets.token_hex(16)
    now = int(time.time())
    sessions[token] = {"username": username, "role": role, "created_at": now, "expires_at": now + SESSION_SECONDS}
    _save_json(SESSIONS_FILE, sessions)
    return token

def validate_session(token):
    sessions = _load_json(SESSIONS_FILE)
    record = sessions.get(token)
    if not record:
        return False
    if int(time.time()) > record.get("expires_at", 0):
        # expired -> remove
        sessions.pop(token, None)
        _save_json(SESSIONS_FILE, sessions)
        return False
    return True

def get_session_user(token):
    sessions = _load_json(SESSIONS_FILE)
    record = sessions.get(token)
    if record and int(time.time()) <= record.get("expires_at", 0):
        return record.get("username"), record.get("role")
    return None, None

def end_session(token):
    sessions = _load_json(SESSIONS_FILE)
    if token in sessions:
        sessions.pop(token, None)
        _save_json(SESSIONS_FILE, sessions)
        return True
    return False

def hash_password(password):
    binary_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(binary_password, salt)
    return hash_password.decode('utf-8')

def validate_hash(password, hash):
    hash_password = hash.encode('utf-8')
    bin_password = password.encode('utf-8')
    return bcrypt.checkpw(bin_password, hash_password)

def password_strength(password: str) -> tuple[int, str]:
    """Return a score (0-5) and a label for the given password."""
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

def register_user():
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    # Role selection
    valid_roles = ("user", "admin", "analyst")
    while True:
        role_input = input("Enter role (user/admin/analyst) [user]: ").strip().lower()
        role = role_input or "user"
        if role in valid_roles:
            break
        print("Invalid role. Choose from: user, admin, analyst.")

    while True:
        psw = getpass.getpass("Enter your password (input hidden): ")
        score, label = password_strength(psw)
        print_strength_bar(score)
        print(f"Rating: {label}")
        if score >= 3:
            choice = input("Use this password? [Y/n]: ").strip().lower()
            if choice in ("", "y", "yes"):
                break
            elif choice == "n":
                continue
            else:
                continue
        else:
            choice = input("Password is weak. Options: [r]etry, [a]ccept anyway, [c]ancel registration: ").strip().lower()
            if choice == "r":
                continue
            if choice == "a":
                break
            if choice == "c":
                print("Registration cancelled.")
                return

    hashed = hash_password(psw)
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{role},{hashed}\n")
    # Reset any lockout info on new registration
    _reset_lockout(name)
    print(f"User registered with role: {role}")

def login_user():
    """
    Attempt login.
    Returns:
      - session token (str) on success
      - "locked" if account currently locked
      - "notfound" if username not found
      - "invalid" if username found but password incorrect
    """
    name = input("Enter your name: ").strip()
    psw = getpass.getpass("Enter your password: ")

    # Check lockout
    lock = _get_lockout(name)
    now = int(time.time())
    if lock.get("locked_until", 0) > now:
        return "locked"

    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            users = f.readlines()
    except FileNotFoundError:
        return "notfound"

    found = False
    for user in users:
        parts = user.strip().split(",", 2)
        if len(parts) == 3:
            name_, role, hash = parts
        elif len(parts) == 2:
            name_, hash = parts
            role = "user"
        else:
            continue

        if name_ == name:
            found = True
            if validate_hash(psw, hash):
                # success -> reset lockout and create session
                _reset_lockout(name)
                token = _create_session(name, role)
                print(f"Welcome {name} (role: {role}). Session token: {token}")
                return token
            else:
                # failure -> increment
                lock = _get_lockout(name)
                failed = lock.get("failed", 0) + 1
                locked_until = 0
                if failed >= MAX_FAILED:
                    locked_until = int(time.time()) + LOCKOUT_SECONDS
                    print(f"Too many failed attempts. Account locked for {LOCKOUT_SECONDS} seconds.")
                else:
                    print(f"Invalid credentials. {MAX_FAILED - failed} attempts left before lockout.")
                _set_lockout(name, {"failed": failed, "locked_until": locked_until})
                return "invalid"

    if not found:
        return "notfound"
