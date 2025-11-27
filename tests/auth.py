import bcrypt
import getpass
from app.Application import hash_password, validate_hash

def main():
    # hidden prompt for a test password
    test_password = getpass.getpass("Enter test password (input hidden): ")

    hashed = hash_password(test_password)
    print(f"Original password: {'*' * len(test_password)} (length: {len(test_password)})")
    print(f"Hashed password: {hashed}")
    print(f"Hash length: {len(hashed)} characters")

    # Test verification with correct password
    is_valid = validate_hash(test_password, hashed)
    print(f"\nVerification with correct password: {is_valid}")

    # Test verification with incorrect password
    is_invalid = validate_hash("WrongPassword", hashed)
    print(f"Verification with incorrect password: {is_invalid}")

if __name__ == "__main__":
    main()
