# connect_db.py
import mysql.connector
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Create connection
conn = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
conn.database = DB_NAME

print(f"Connected to database: {DB_NAME}")
