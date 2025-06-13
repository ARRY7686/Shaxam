from collections import defaultdict
from typing import Dict, List, Tuple
from dataclasses import dataclass
from src.database import get_all_fingerprints  # Returns { song_id: [(address, anchor_time_ms)] }

@dataclass
class Match:
    song_id: int
    score: float
    timestamp: int
    points: List[Tuple[int, int]]  # For chart visualization


def match_fingerprint(sample_fingerprint: Dict[int, int]) -> List[Match]:
    """
    Matches the sample fingerprint against the database and returns ranked matches.
    Input: sample_fingerprint = {address: anchor_time_ms or Couple}
    """

    db = get_all_fingerprints()  # { song_id: [(address, anchor_time_ms)] }
    matches_by_song: Dict[int, List[Tuple[int, int]]] = defaultdict(list)  # song_id -> [(sample_time, db_time)]
    earliest_time: Dict[int, int] = {}

    for song_id, entries in db.items():
        for address_db, db_time in entries:
            if address_db in sample_fingerprint:
                value = sample_fingerprint[address_db]
                sample_time = value.anchor_time_ms if hasattr(value, "anchor_time_ms") else value

                matches_by_song[song_id].append((sample_time, db_time))

                if song_id not in earliest_time or db_time < earliest_time[song_id]:
                    earliest_time[song_id] = db_time

    results = []
    for song_id, time_pairs in matches_by_song.items():
        score = compute_alignment_score(time_pairs)
        results.append(Match(
            song_id=song_id,
            score=score,
            timestamp=earliest_time[song_id],
            points=time_pairs
        ))

    results.sort(key=lambda m: m.score, reverse=True)
    return results


def compute_alignment_score(pairs: List[Tuple[int, int]]) -> float:
    score = 0
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            try:
                sample_diff = abs(pairs[i][0] - pairs[j][0])
                db_diff = abs(pairs[i][1] - pairs[j][1])
                if abs(sample_diff - db_diff) < 100:  # ≤100ms offset
                    score += 1
            except Exception as e:
                print(f"Error computing score between {pairs[i]} and {pairs[j]}: {e}")
    return float(score)
