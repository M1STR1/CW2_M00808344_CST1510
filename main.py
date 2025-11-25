from Application import (
    register_user as interactive_register,
    login_user as interactive_login,
    get_session_user,
)
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import (
    register_user as svc_register,
    login_user as svc_login,
    migrate_users_from_file,
)
from app.data.incidents import insert_incident, get_all_incidents

def show_menu():
    print()
    print("Welcome! Choose an option:")
    print("1. Register (interactive)")
    print("2. Login (interactive)")
    print("3. Run DB demo (migrate + CRUD tests)")
    print("4. Exit")

def run_cli():
    while True:
        show_menu()
        choice = input("Enter choice (1, 2, 3, or 4): ").strip()
        if choice == "1":
            interactive_register()
        elif choice == "2":
            token = interactive_login()
            if token and token not in ("locked","notfound","invalid"):
                user, role = get_session_user(token)
                print(f"Logged in as: {user} (role: {role})")
            else:
                print("Login failed or other status:", token)
        elif choice == "3":
            run_db_demo()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")

def run_db_demo():
    print("=" * 60)
    print("DB demo: setup, migrate users, test svc register/login, CRUD incidents")
    print("=" * 60)

    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # migrate users from file (must exist)
    migrate_users_from_file("app/data/users.txt")
    print("User migration completed.")

    # Test service-based registration and login (non-interactive)
    success, msg = svc_register("alice", "password123", "analyst")
    print("Register:", success, msg)
    success, msg = svc_login("alice", "password123")
    print("Login:", success, msg)

    # Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing Attack",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")

    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

if __name__ == "__main__":
    run_cli()
