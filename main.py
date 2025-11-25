from Application import (
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

def main():
    print("=" * 60)
    print("week 8: database demo")
    print("=" * 60)

    # 1. setup database connection
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. migrate users from file
    migrate_users_from_file("app/data/users.txt")
    print("User migration completed.")
    
    # 3. test authentication
    success, msg = register_user("alice", "password123", "analyst")
    print(msg)

    success, msg = login_user("alice", "password123")
    print(msg)

    # 4. test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing Attack",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    # 5. query data
    df = get_all_incidents()
    print(f'Total incidents: {len(df)}')

if __name__ == "__main__":
    main()
