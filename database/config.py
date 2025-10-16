#!/usr/bin/env python
# This file stores the SQLite database configuration details

from pathlib import Path

# Database configuration

DB_NAME = "new_york_yellow_taxi_august_2025"  # SQLite database name

# Path to the SQLite database file
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / f"{DB_NAME}.db"
