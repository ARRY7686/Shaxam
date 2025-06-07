import sqlite3
import os

DB_FILENAME = "shaxamv3.sqlite"

def initialize_database(db_file: str):
    if os.path.exists(db_file):
        print(f"Database '{db_file}' already exists.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            ytID TEXT,
            key TEXT NOT NULL UNIQUE
        );
    ''')

    # Create fingerprints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fingerprints (
            address INTEGER NOT NULL,
            anchorTimeMs INTEGER NOT NULL,
            songID INTEGER NOT NULL,
            PRIMARY KEY (address, anchorTimeMs, songID)
        );
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_file}' created with required tables.")

if __name__ == "__main__":
    initialize_database(DB_FILENAME)
