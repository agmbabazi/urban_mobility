#!/usr/bin/env python
# This script saves (backs up) the current SQLite database to a backup file

import sqlite3
from pathlib import Path
from datetime import datetime
from config import DB_PATH, DB_NAME

def save_database():
    """
    Creates a timestamped backup of the SQLite database.
    """
    try:
        # Create backup directory
        backup_dir = Path(__file__).resolve().parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Create backup file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{DB_NAME}_backup_{timestamp}.db"

        # Connect to source and destination databases
        source_conn = sqlite3.connect(DB_PATH)
        dest_conn = sqlite3.connect(backup_file)

        # Perform the backup
        with dest_conn:
            source_conn.backup(dest_conn)

        source_conn.close()
        dest_conn.close()

        print(f"Database successfully backed up as: {backup_file.resolve()}")

    except Exception as e:
        print(f"Error saving database: {e}")

if __name__ == "__main__":
    save_database()
