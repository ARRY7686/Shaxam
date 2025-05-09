import json
import os

DB_PATH = "fingerprints/db.json"

def add_song(song_name, fingerprints):
    db = load_db()
    
    fingerprints_cleaned = [(str(h), int(t)) for h, t in fingerprints]
    db[song_name] = fingerprints_cleaned

    with open(DB_PATH, "w") as f:
        json.dump(db, f)
def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r") as f:
        return json.load(f)
