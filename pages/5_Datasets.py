def get_all_datasets(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM datasets_metadata ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(r) for r in rows]


def insert_dataset(conn, name, source, category, size):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
        (name, source, category, size)
    )
    conn.commit()


def delete_dataset(conn, dataset_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
