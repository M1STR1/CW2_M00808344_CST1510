# Multi-Domain Intelligence Platform — Week 7 / Week 8

Student: Lee-Brandon Lindsey  
Student ID: M00808344  
Course: CST1510 — CW2

---

## Project Summary
Small command-line intelligence platform demonstrating secure authentication and a database-backed system for Week 7 & Week 8.  
Includes secure password hashing, role-based users, account lockout, session management, and simple CRUD capabilities.

---

## Features
- Secure password storage using bcrypt (with automatic salting)
- Password strength indicator
- Role-based registration: user / admin / analyst
- Account lockout after repeated failed logins
- Session management (create / validate / end)
- SQLite database schema for users, incidents, datasets, and IT tickets
- Migration from `DATA/users.txt` into the database
- CSV import and CRUD helpers for incidents
- Unit tests (pytest) for core logic and flows

---

## Technical Implementation
- Hash Algorithm: bcrypt
- Database: SQLite (file under `DATA/`)
- Data storage of users (legacy): comma-separated `users.txt`
- Language: Python 3.10+ (recommended)
- Key files:
  - `Application.py` — interactive auth flows, lockout, sessions
  - `main.py` — CLI demo and DB demo
  - `app/data/schema.py` — table creation
  - `app/data/db.py` — DB connection helper
  - `app/services/user_service.py` — service layer for user CRUD
  - `app/data/incidents.py` — incidents CRUD & CSV loader
  - `auth.py` — simple password hashing test script

---

## Requirements
Install dependencies:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
(For PowerShell use: `.venv\Scripts\Activate.ps1`)

---

## Setup and Running
1. Ensure package folders exist:
   - `app/`, `app/data/`, `app/services/`
   - Include `__init__.py` files if needed.

2. Create a `DATA/` directory if you want to store data files locally:
```
mkdir DATA
```

3. Run the demo CLI:
```
python main.py
```

The CLI includes:
- Register
- Login
- A DB demo that creates tables, migrates users, and performs CRUD

---

## Migration format
- The migration script (`migrate_users_from_file`) reads `DATA/users.txt`. Each line must be:
```
username,hashed_password,role
```
- Use `bcrypt`-generated hashes if migrating from legacy data.

---

## Testing
Run all tests:
```
pytest -q
```
Unit tests use temporary DB files to avoid changing your `DATA/` folder.

---

## Git Notes
- `.gitignore` hides `app/data/` and `services/` to avoid committing data or ephemeral files:
```
app/data/
services/
.pytest_cache/
```
- To track these folders, remove the ignore rules and re-add files:
```
git rm -r --cached app/data services
git add app/data services .gitignore
git commit -m "Track app/data and services"
```

---

## Troubleshooting
- ImportError: Ensure `__init__.py` exists in `app`, `app/data`, `app/services`.
- Bcrypt missing: `pip install bcrypt`
- Pandas errors (CSV loader): `pip install pandas`
- Database not creating: Confirm `create_all_tables(conn)` runs before CRUD operations.

---

## Next Steps
- Add role-based CLI actions (admin-only functionality)
- Add more unit tests for migration, CSV loader, and interactive flows
- Add CI to run tests on push (GitHub Actions)
- Improve session persistence (database-backed sessions in production)

---