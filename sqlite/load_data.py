import sqlite3
import pandas as pd
from pathlib import Path
import math
from datetime import datetime

# File paths
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "data.db"
CSV_PATH = BASE_DIR.parent / "data" / "train.csv"
SCHEMA_PATH = BASE_DIR / "schema.sql"
REMOVED_LOG = BASE_DIR / "removed_records.csv"

def create_database():
    """Create the database and apply schema."""
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
    print(" Database and schema created successfully.")

def load_data():
    """Load, clean, and insert data into the database."""
    def get_distance(lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def get_duration(pickup, dropoff):
        try:
            start = datetime.strptime(pickup, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(dropoff, '%Y-%m-%d %H:%M:%S')
            return (end - start).total_seconds() / 60
        except:
            return None

    print(" Loading CSV...")
    df = pd.read_csv(CSV_PATH)

    print(" Calculating derived features...")
    df["duration_min"] = df.apply(lambda row: get_duration(row["pickup_datetime"], row["dropoff_datetime"]), axis=1)
    df["distance_km"] = df.apply(lambda row: get_distance(
        row["pickup_latitude"], row["pickup_longitude"],
        row["dropoff_latitude"], row["dropoff_longitude"]
    ), axis=1)
    df["avg_speed_kmh"] = df.apply(lambda row: row["distance_km"] / (row["duration_min"] / 60) if row["duration_min"] else None, axis=1)

    # Normalize column names
    df["pickup_lat"] = df["pickup_latitude"]
    df["pickup_lng"] = df["pickup_longitude"]
    df["dropoff_lat"] = df["dropoff_latitude"]
    df["dropoff_lng"] = df["dropoff_longitude"]

    # Set placeholders if not in original dataset
    df["fare_amount"] = df.get("fare_amount", None)
    df["tip_amount"] = df.get("tip_amount", None)

    # Clean data
    print(" Cleaning data...")
    original_count = len(df)
    df_cleaned = df[
        (df["duration_min"].notnull()) &
        (df["duration_min"] > 0) & (df["duration_min"] < 180) &
        (df["distance_km"] > 0) & (df["distance_km"] < 100) &
        (df["avg_speed_kmh"] > 1) & (df["avg_speed_kmh"] < 150)
    ]
    removed_count = original_count - len(df_cleaned)

    print(f" Removed {removed_count} invalid records.")
    df_removed = df[~df.index.isin(df_cleaned.index)]
    df_removed.to_csv(REMOVED_LOG, index=False)
    print(f" Removed records saved to: {REMOVED_LOG.name}")

    # Insert cleaned data
    print(" Inserting cleaned data into the database...")
    with sqlite3.connect(DB_PATH) as conn:
        # Prepare trips table
        trips_cols = [
            "id", "vendor_id", "pickup_datetime", "dropoff_datetime",
            "passenger_count", "pickup_lat", "pickup_lng",
            "dropoff_lat", "dropoff_lng", "store_and_fwd_flag",
            "distance_km", "duration_min", "fare_amount", "tip_amount", "avg_speed_kmh"
        ]
        trips_df = df_cleaned[trips_cols].copy()
        trips_df = trips_df.rename(columns={"id": "trip_id"})
        trips_df.to_sql("trips", conn, if_exists="replace", index=False)

        # Insert passengers as a separate table (if still needed)
        passengers = pd.DataFrame(df_cleaned["passenger_count"].unique(), columns=["passenger_count"])
        passengers.to_sql("passengers", conn, if_exists="replace", index=False)

        print("Cleaned data inserted successfully.")

        # Print 3 sample rows
        print("\n Sample inserted records:")
        sample = pd.read_sql("SELECT * FROM trips LIMIT 3", conn)
        print(sample.to_markdown(index=False))

if __name__ == "__main__":
    create_database()
    load_data()
