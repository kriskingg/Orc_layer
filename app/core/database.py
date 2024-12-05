import sqlite3
from typing import Generator
import os

# Load database file path from environment variable
DB_FILE = os.getenv("DB_FILE_PATH", "metadata.db")

def init_db():
    """
    Initialize SQLite database.
    Creates the database file and the necessary tables if they don't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create secrets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            path TEXT PRIMARY KEY,
            backend TEXT
        )
    """)

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def store_metadata(path: str, backend: str):
    """
    Store metadata in the database.
    Maps the path of the secret to the backend (e.g., HashiCorp or Azure).
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO secrets (path, backend) VALUES (?, ?)", (path, backend))
    conn.commit()
    conn.close()

def get_backend(path: str) -> str:
    """
    Retrieve the backend for a given secret path.
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT backend FROM secrets WHERE path = ?", (path,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Provide a database connection for dependency injection in FastAPI.
    Ensures the connection is closed after use.
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()
