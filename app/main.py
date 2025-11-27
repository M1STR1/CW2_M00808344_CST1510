from app.Application import (
    register_user,
    login_user,
    password_strength,
    print_strength_bar,
    hash_password,
    validate_hash,
    validate_session,
    get_session_user,
    end_session,
)

def show_menu():
    print()
    print("Welcome! Choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice == "1":
            register_user()
            print("User registered successfully.")
        elif choice == "2":
            token = login_user()
            if token:
                print("Login successful.")
                user, role = get_session_user(token)
                if user:
                    print(f"Logged in as: {user} (role: {role})")
            else:
                print("Login failed.")
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.csv_loader import load_all_csv_data

def main():
    print("="*60)
    print("Week 8: Database Demo")
    print("="*60)

    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    migrated = migrate_users_from_file()  # returns number migrated
    print(f"Migrated {migrated} users (if any)")

    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    incident_id = insert_incident("2024-11-05", "Phishing", "High", "Open", "Suspicious email", "alice")
    print(f"Created incident {incident_id}")
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

if __name__ == "__main__":
    main()
