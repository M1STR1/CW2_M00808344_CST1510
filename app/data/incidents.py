import pandas as pd
from app.data.db import connect_database

def insert_incident(date, incident_type, severity, status, description, reported_by=None, db_path=None):
    """Insert new incident"""
    conn = connect_database(db_path) if db_path else connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents(db_path=None):
    """Retrieve all incidents"""
    conn = connect_database(db_path) if db_path else connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    conn.close()
    return df

def update_incident_status(incident_id, new_status, db_path=None):
    """Update the status of an incident"""
    conn = connect_database(db_path) if db_path else connect_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    changed = cursor.rowcount
    conn.close()
    return changed

def delete_incident(incident_id, db_path=None):
    """Delete an incident"""
    conn = connect_database(db_path) if db_path else connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted
