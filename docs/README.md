# Week 7: Secure Authentication System
Student Name: Lee-Brandon Lindsey
Student ID: M00808344
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters

## Project: Week 8 Worksheet — DB + Auth Demo

### Setup:
1. Create Python venv and install dependencies:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Run the DB demo
   python main.py

3. Run tests:
   pytest -q

### Notes:
- DB file by default is DATA/intelligence_platform.db
- The migration reads DATA/users.txt if present
- CLI demo uses Application.register_user and Application.login_user for interactive flows