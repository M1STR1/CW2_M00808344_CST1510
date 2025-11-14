import bcrypt

def hash_password(password):
    binary_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(binary_password, salt)
    return hash_password.decode('utf-8')

def validate_hash(password, hash):
    hash_password = hash.encode('utf-8')
    bin_password = password.encode('utf-8')
    return bcrypt.checkpw(bin_password, hash_password)

def register_user():
    name = input("Enter your name: ")
    psw = input("Enter your password: ")
    hash = hash_password(psw)
    with open("users.txt", "a") as f:
        f.write(f"{name},{hash}\n")
    print("User registered.")

def login_user():
    name = input("Enter your name: ")
    psw = input("Enter your password: ")

    with open("users.txt", "r") as f:
        users = f.readlines()
    
    for user in users:
        name_, hash = user.strip().split(",")
        if name_ == name:
            return validate_hash(psw, hash)
    return False