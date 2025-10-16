#!/usr/bin/env python
# This script inserts the entire cleaned DataFrame into the SQLite database

import sqlite3
from config import DB_PATH
from cleaning_checkpoint import clean_data  # clean_data is already a DataFrame

def insert_data():
    """
    Inserts the full cleaned DataFrame into the SQLite database.
    """
    try:
        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)

        # Use the cleaned DataFrame directly
        df = clean_data

        # Insert all rows at once
        df.to_sql(
            name="trips",
            con=conn,
            if_exists="append",
            index=False
        )

        conn.close()
        print(f"Successfully inserted {len(df)} rows into SQLite database!")

    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    insert_data()
