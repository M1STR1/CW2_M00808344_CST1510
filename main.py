from Application import register_user, login_user, password_strength, print_strength_bar, hash_password

def menu():
    print("Welcome! Choose an option:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter choice (1, 2, or 3): ")
    if choice == "1":
        register_user()
        print("User registered successfully.")
    elif choice == "2":
        if login_user():
            print("Login successful.")
        else:
            print("Login failed.")
    elif choice == "3":
        print("Exiting program.")
        return
    else:
        print("Invalid choice.")

def main():
    while True:
        menu()
        choice = input("> ")
        print('Choose an option: 1. Register 2. Login 3. Exit')
        if choice == "1":
            register_user()
            print("User registered successfully.")
        elif choice == "2":
            if login_user():
                print("Login successful.")
            else:
                print("Login failed.")
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()