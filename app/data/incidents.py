import pandas as pd
from typing import List, Dict

# Keep SQL parameterized

def get_all_incidents(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM cyber_incidents ORDER BY id DESC")
    rows = cur.fetchall()
    if not rows:
        return []
    cols = rows[0].keys()
    return [dict(r) for r in rows]


def insert_incident(conn, title, severity, status, date):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
        (title, severity, status, date)
    )
    conn.commit()


def update_incident(conn, incident_id, **fields):
    keys = list(fields.keys())
    values = [fields[k] for k in keys]
    set_clause = ", ".join([f"{k} = ?" for k in keys])
    sql = f"UPDATE cyber_incidents SET {set_clause} WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, (*values, incident_id))
    conn.commit()


def delete_incident(conn, incident_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()


def load_incidents_from_csv(conn, csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        insert_incident(conn, row.get('title', ''), row.get('severity', ''), row.get('status', ''), row.get('date', ''))
