from pathlib import Path
import sqlite3

DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def connect_database(db_path: Path | str = DB_PATH):
    """Open and return sqlite3 connection. db_path may be a Path or string; default DB lives under DATA/."""
    return sqlite3.connect(str(db_path))