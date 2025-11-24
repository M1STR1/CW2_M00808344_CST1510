import bcrypt
import re
import getpass

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
    print(f"User registered with role: {role}")

def login_user():
    name = input("Enter your name: ").strip()
    psw = getpass.getpass("Enter your password: ")

    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            users = f.readlines()
    except FileNotFoundError:
        return False

    for user in users:
        parts = user.strip().split(",", 2)
        if len(parts) == 3:
            name_, role, hash = parts
        elif len(parts) == 2:
            # legacy format: name,hash
            name_, hash = parts
            role = "user"
        else:
            continue

        if name_ == name:
            if validate_hash(psw, hash):
                print(f"Welcome {name} (role: {role})")
                return True
            else:
                return False
    return False
