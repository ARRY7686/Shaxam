import random
from dataclasses import dataclass
from typing import Dict, List, Tuple
from src.db_connection import get_connection

@dataclass
class Couple:
    anchor_time_ms: int
    song_id: int


def generate_unique_id() -> int:
    return random.randint(1, 2**31 - 1)

def get_song_metadata(song_id: int) -> Tuple[str, str]:
    """
    Fetches the title and artist of a song from the DB by its id.
    Returns (title, artist) or ("Unknown", "Unknown") if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, artist FROM songs WHERE id = ?
    """, (song_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0], row[1]
    else:
        return "Unknown", "Unknown"

def add_song(song_title: str, song_artist: str, yt_id: str, fingerprints: Dict[int, Couple]):
    conn = get_connection()
    cursor = conn.cursor()

    song_key = f"{song_title}---{song_artist}"

    # Insert song without id (let SQLite assign it)
    cursor.execute("""
        INSERT OR IGNORE INTO songs (title, artist, ytID, key)
        VALUES (?, ?, ?, ?)
    """, (song_title, song_artist, yt_id, song_key))
    conn.commit()

    # Retrieve song_id - either lastrowid or select by key
    song_id = cursor.lastrowid
    if song_id == 0:  # Insert ignored, so fetch existing ID
        cursor.execute("SELECT id FROM songs WHERE key = ?", (song_key,))
        row = cursor.fetchone()
        if not row:
            print(f"[ERROR] Failed to fetch song_id for '{song_title}'")
            cursor.close()
            conn.close()
            return
        song_id = row[0]

    # Now prepare fingerprint data using the real song_id
    data = [
        (int(address), int(c.anchor_time_ms), int(song_id))
        for address, c in fingerprints.items()
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO fingerprints (address, anchorTimeMs, songID)
        VALUES (?, ?, ?)
    """, data)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"[INFO] Added song '{song_title}' with {len(data)} fingerprints.")



def get_all_fingerprints() -> Dict[int, List[Tuple[int, int]]]:
    """
    Returns all fingerprints in the format:
    { song_id: [(address, anchor_time_ms), ...] }
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT songID, address, anchorTimeMs
        FROM fingerprints
    """)
    rows = cursor.fetchall()

    db = {}
    for song_id, address, anchor_time_ms in rows:
        db.setdefault(song_id, []).append((address, anchor_time_ms))

    cursor.close()
    conn.close()
    return db
