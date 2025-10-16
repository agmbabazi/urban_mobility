#!/usr/bin/env python
# This script inserts data into the SQLite database

import sqlite3
from config import DB_PATH
import pandas as pd
from cleaning_checkpoint import clean_data  # Ensure clean_data returns a cleaned DataFrame

def insert_data():
    """
    Inserts cleaned trip data into the SQLite database in batches.
    """
    try:
        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Load cleaned data (ensure clean_data is a pandas DataFrame)
        df = clean_data()

        batch_size = 100000
        total_rows = len(df)

        for start in range(0, total_rows, batch_size):
            end = start + batch_size
            batch_df = df.iloc[start:end]

            # Insert rows into trips table
            batch_df.to_sql(
                name="trips",
                con=conn,
                if_exists="append",
                index=False
            )

            print(f"✅ Inserted rows {start} to {min(end, total_rows)}")

        conn.close()
        print("🎉 Data successfully inserted into SQLite database!")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    insert_data()
