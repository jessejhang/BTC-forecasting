# src/database.py
import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_name="data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ", ".join([f"{col} TEXT" for col in columns])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        self.conn.commit()

    def store_data(self, data: pd.DataFrame, table_name="bitcoin_data"):
        columns = list(data.columns)
        self.create_table(table_name, columns)
        for _, row in data.iterrows():
            self.cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(row))})", tuple(row))
        self.conn.commit()

    def fetch_data(self, table_name="bitcoin_data"):
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.conn)

    def close(self):
        self.conn.close()
