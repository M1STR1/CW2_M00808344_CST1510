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