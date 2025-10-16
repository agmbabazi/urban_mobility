#!/usr/bin/env python
# This script initializes a SQLite3 database for the project

import sqlite3
from config import DB_PATH

def create_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"Database created at {DB_PATH}")
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
