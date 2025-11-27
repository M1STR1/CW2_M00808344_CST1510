# Object-oriented manager for the app
from app.data.db import connect_database
from app.data import incidents, datasets, tickets


class CRUDManager:
    def __init__(self, db_path=None):
        self.conn = connect_database(db_path)


# Incidents
def list_incidents(self):
    return incidents.get_all_incidents(self.conn)


def add_incident(self, title, severity, status, date):
    incidents.insert_incident(self.conn, title, severity, status, date)


def edit_incident(self, id, **fields):
    incidents.update_incident(self.conn, id, **fields)


def remove_incident(self, id):
    incidents.delete_incident(self.conn, id)


# Datasets
def list_datasets(self):
    return datasets.get_all_datasets(self.conn)


def add_dataset(self, name, source, category, size):
    datasets.insert_dataset(self.conn, name, source, category, size)


def remove_dataset(self, id):
    datasets.delete_dataset(self.conn, id)


# Tickets
def list_tickets(self):
    return tickets.get_all_tickets(self.conn)


def add_ticket(self, title, priority, status, created_date):
    tickets.insert_ticket(self.conn, title, priority, status, created_date)


def remove_ticket(self, id):
    tickets.delete_ticket(self.conn, id)
