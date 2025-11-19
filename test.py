import sqlite3

conn = sqlite3.connect('DATA/intelligence_platform.db')

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

 