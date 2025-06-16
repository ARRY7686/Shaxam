from collections import defaultdict
from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.db_connection import get_connection  # used directly instead of get_all_fingerprints

@dataclass
class Match:
    song_id: int
    score: float
    timestamp: int
    points: List[Tuple[int, int]]  # For chart visualization

def match_fingerprint(sample_fingerprint: Dict[int, int]) -> List[Match]:
    """
    Efficiently match the sample fingerprint against the database using a single SQL query.
    """
    if not sample_fingerprint:
        return []

    addresses = tuple(sample_fingerprint.keys())

    # Prepare SQL query
    placeholders = ",".join("?" for _ in addresses)
    query = f"""
        SELECT songID, address, anchorTimeMs
        FROM fingerprints
        WHERE address IN ({placeholders})
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, addresses)

    matches_by_song = defaultdict(list)
    earliest_time = {}

    for song_id, address, db_time in cursor.fetchall():
        sample_time = sample_fingerprint[address]
        if hasattr(sample_time, "anchor_time_ms"):
            sample_time = sample_time.anchor_time_ms

        matches_by_song[song_id].append((sample_time, db_time))

        if song_id not in earliest_time or db_time < earliest_time[song_id]:
            earliest_time[song_id] = db_time

    cursor.close()
    conn.close()

    results = [
        Match(
            song_id=sid,
            score=compute_alignment_score(pairs),
            timestamp=earliest_time[sid],
            points=pairs
        )
        for sid, pairs in matches_by_song.items()
    ]

    return sorted(results, key=lambda m: m.score, reverse=True)

def compute_alignment_score(pairs: List[Tuple[int, int]]) -> float:
    score = 0
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            try:
                sample_diff = abs(pairs[i][0] - pairs[j][0])
                db_diff = abs(pairs[i][1] - pairs[j][1])
                if abs(sample_diff - db_diff) < 100:
                    score += 1
            except Exception as e:
                print(f"Error computing score between {pairs[i]} and {pairs[j]}: {e}")
    return float(score)
