def get_all_tickets(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM it_tickets ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(r) for r in rows]


def insert_ticket(conn, title, priority, status, created_date):
    cur = conn.cursor()
    cur.execute("INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
                (title, priority, status, created_date))
    conn.commit()


def delete_ticket(conn, ticket_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
