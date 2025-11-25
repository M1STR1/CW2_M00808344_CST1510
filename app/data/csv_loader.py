import pandas as pd

def load_csv_to_table(conn, csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    return len(df)

def load_all_csv_data(conn, base_path="DATA"):
    total = 0
    total += load_csv_to_table(conn, f"{base_path}/cyber_incidents.csv", "cyber_incidents")
    total += load_csv_to_table(conn, f"{base_path}/datasets_metadata.csv", "datasets_metadata")
    total += load_csv_to_table(conn, f"{base_path}/it_tickets.csv", "it_tickets")
    return total
