#!/usr/bin/env python
# This script exports your MySQL database as a SQL dump file in smaller chunks

import mysql.connector
from pathlib import Path
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
import os

DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "database": DB_NAME
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

def write_chunk(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def export_database():
    try:
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

        chunk_index = 1
        current_size = 0
        buffer = []

        def new_chunk_path(index):
            return output_dir / f"database_dump.part{index:03d}.sql"

        print("Connecting to database...")

        for table in tables:
            print(f"Exporting table: {table}")

            # Table structure
            cursor.execute(f"SHOW CREATE TABLE `{table}`;")
            create_stmt = cursor.fetchone()[1]
            lines = [
                f"\n-- Structure for table `{table}`\n",
                f"DROP TABLE IF EXISTS `{table}`;\n",
                f"{create_stmt};\n\n"
            ]
            for line in lines:
                buffer.append(line)
                current_size += len(line.encode('utf-8'))
                if current_size >= MAX_FILE_SIZE:
                    write_chunk(new_chunk_path(chunk_index), buffer)
                    chunk_index += 1
                    buffer = []
                    current_size = 0

            # Table data
            cursor.execute(f"SELECT * FROM `{table}`;")
            rows = cursor.fetchall()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                buffer.append(f"-- Data for table `{table}`\n")
                current_size += len(buffer[-1].encode('utf-8'))
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
                    insert_line = f"INSERT INTO `{table}` ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                    buffer.append(insert_line)
                    current_size += len(insert_line.encode('utf-8'))
                    if current_size >= MAX_FILE_SIZE:
                        write_chunk(new_chunk_path(chunk_index), buffer)
                        chunk_index += 1
                        buffer = []
                        current_size = 0

        # Write remaining buffer
        if buffer:
            write_chunk(new_chunk_path(chunk_index), buffer)

        cursor.close()
        conn.close()

        print("\nDump completed successfully!")
        print(f"Files saved in: {output_dir.resolve()}")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    export_database()
