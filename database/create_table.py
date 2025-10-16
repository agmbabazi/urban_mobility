#!/usr/bin/env python
# This script creates tables in the SQLite database

import sqlite3
from config import DB_PATH

def create_tables():
    """
    Connects to the SQLite database and creates the required tables if they don't exist.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the trips table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            VendorID INTEGER,
            tpep_pickup_datetime TEXT,
            tpep_dropoff_datetime TEXT,
            passenger_count INTEGER,
            trip_distance REAL,
            RatecodeID INTEGER,
            store_and_fwd_flag TEXT,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            payment_type INTEGER,
            fare_amount REAL,
            extra REAL,
            mta_tax REAL,
            tip_amount REAL,
            tolls_amount REAL,
            improvement_surcharge REAL,
            congestion_surcharge REAL,
            Airport_fee REAL,
            total_amount REAL,
            calculated_total_amount REAL,
            trip_duration_min REAL,
            speed_mph REAL,
            fare_per_mile REAL,
            tip_pct REAL,
            idle_trip_flag INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Commit and close
        conn.commit()
        conn.close()

        print("Tables created successfully.")

    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
