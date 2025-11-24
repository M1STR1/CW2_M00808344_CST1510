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
    name = input("Enter your name: ")
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
    with open("users.txt", "a") as f:
        f.write(f"{name},{hashed}\n")
    print("User registered.")

def login_user():
    name = input("Enter your name: ")
    psw = getpass.getpass("Enter your password: ")

    try:
        with open("users.txt", "r") as f:
            users = f.readlines()
    except FileNotFoundError:
        return False

    for user in users:
        name_, hash = user.strip().split(",", 1)
        if name_ == name:
            return validate_hash(psw, hash)
    return False