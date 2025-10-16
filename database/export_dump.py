#!/usr/bin/env python
# This script exports the SQLite database into a single SQL dump file, overwriting if content is the same

import sqlite3
from pathlib import Path
from datetime import datetime
from config import DB_PATH
import filecmp

def export_database():
    """
    Exports the entire SQLite database into a single SQL dump file.
    Overwrites the existing dump if the content is the same.
    """
    try:
        # Create an output directory for the dump if it doesn't exist
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)

        # Set the dump file path (no timestamp, just a fixed file)
        dump_file = output_dir / "database_dump.sql"

        # Connect to SQLite
        conn = sqlite3.connect(DB_PATH)

        # Generate the SQL dump as a string
        new_dump_lines = []
        for line in conn.iterdump():
            new_dump_lines.append(f"{line}\n")
        conn.close()

        # Check if the dump file already exists
        if dump_file.exists():
            with open(dump_file, "r", encoding="utf-8") as f:
                old_lines = f.readlines()

            # Only overwrite if the content is different
            if old_lines == new_dump_lines:
                print("Database dump is identical. No changes made.")
                return

        # Write the new dump to the file
        with open(dump_file, "w", encoding="utf-8") as f:
            f.writelines(new_dump_lines)

        print(f"Database exported successfully to: {dump_file.resolve()}")

    except Exception as e:
        print(f"Error exporting database: {e}")

if __name__ == "__main__":
    export_database()
