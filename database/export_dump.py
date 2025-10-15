#!/usr/bin/env python
# This script exports your MySQL database as a SQL dump file using Python

import mysql.connector
from pathlib import Path
import os

# Import the existing variables from config.py
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Build a DB_CONFIG dictionary
DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "database": DB_NAME
}

def export_database():
    try:
        # Ensure data/ folder exists
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "database_dump.sql"

        print(" Connecting to database...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(f" Connected to: {DB_CONFIG['database']}")

        # Get all tables
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"-- SQL Dump of {DB_CONFIG['database']}\n\n")

            for table in tables:
                print(f" Exporting table: {table}")

                # Structure
                cursor.execute(f"SHOW CREATE TABLE `{table}`;")
                create_stmt = cursor.fetchone()[1]
                f.write(f"\n-- Structure for table `{table}`\n")
                f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                f.write(f"{create_stmt};\n\n")

                # Data
                cursor.execute(f"SELECT * FROM `{table}`;")
                rows = cursor.fetchall()
                if rows:
                    columns = [desc[0] for desc in cursor.description]
                    f.write(f"-- Data for table `{table}`\n")
                    for row in rows:
                        values = []
                        for val in row:
                            if val is None:
                                values.append("NULL")
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            else:
                                escaped = str(val).replace("'", "''")
                                values.append(f"'{escaped}'")
                        f.write(
                            f"INSERT INTO `{table}` ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                        )
                    f.write("\n")

        cursor.close()
        conn.close()

        print(f"\n Dump completed successfully!")
        print(f" File saved to: {output_file.resolve()}")

    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    export_database()
