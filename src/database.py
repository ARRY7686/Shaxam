from src.db_connection import get_connection

def add_song(song_name, fingerprints):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO songs (name) VALUES (?)", (song_name,))
    conn.commit()

    
    cursor.execute("SELECT id FROM songs WHERE name = ?", (song_name,))
    song_id = cursor.fetchone()[0]

    data = [(int(song_id), str(h), int(t)) for h, t in fingerprints]
    cursor.executemany(
        "INSERT INTO fingerprints (song_id, hash, offset) VALUES (?, ?, ?)", data
    )
    conn.commit()

    cursor.close()
    conn.close()


def get_all_fingerprints():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.name, f.hash, f.offset
        FROM songs s
        JOIN fingerprints f ON s.id = f.song_id
    """)
    rows = cursor.fetchall()

    db = {}
    for name, h, t in rows:
        db.setdefault(name, []).append((h, t))

    cursor.close()
    conn.close()
    return db
