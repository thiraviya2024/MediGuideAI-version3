import sqlite3
import os

# Create data folder automatically
os.makedirs("data", exist_ok=True)

DB_PATH = os.path.join("data", "hospital.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_database()