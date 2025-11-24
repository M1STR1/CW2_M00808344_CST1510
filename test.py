import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")

conn = sqlite3.connect(DB_PATH)

def add_user(conn, name, hash):
    curr = conn.cursor()
    sql = (""" INSERT INTO users (username, password_hash) VALUES (?, ?) """ )
    param = (name, hash) 
    curr.execute(sql, param) 
    conn.commit()

def get_users(): 
    curr = conn.cursor()
    sql = """ SELECT * FROM users """
    curr.execute(sql) 
    users = curr.fetchall()
    conn.close() 
    return users

with open('DATA/users.txt', 'r') as f: 
    users = f.readlines() 
    
for user in users:
    print(user.strip().split(',')) 

 