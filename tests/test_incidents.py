from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident

def test_incidents_crud(tmp_path):
    db_file = tmp_path / "incidents.db"
    conn = connect_database(db_file)
    create_all_tables(conn)
    conn.close()

    incident_id = insert_incident("2024-11-01", "Test", "Low", "Open", "desc", "bob", db_file)
    assert isinstance(incident_id, int)

    df = get_all_incidents(db_file)
    assert df.shape[0] >= 1

    changed = update_incident_status(incident_id, "Resolved", db_file)
    assert changed == 1

    deleted = delete_incident(incident_id, db_file)
    assert deleted == 1