from src.database import get_all_fingerprints
from collections import defaultdict

def match_fingerprint(fingerprint, return_matches=False):
    db = get_all_fingerprints()
    matches = []
    alignments = {}

    input_length = len(fingerprint)
    if input_length == 0:
        return []

    for song, song_fingerprints in db.items():
        direct_matches = 0
        offset_counts = defaultdict(int)
        alignment_points = []

        for h_input, t_input in fingerprint:
            for h_db, t_db in song_fingerprints:
                if h_input == h_db:
                    direct_matches += 1
                    offset = t_db - t_input
                    offset_counts[offset] += 1
                    alignment_points.append((t_input, t_db))

        if direct_matches == 0:
            continue

        best_alignment = max(offset_counts.values(), default=0)
        hybrid_score = best_alignment * 2 + direct_matches
        max_possible = input_length * 3 
        confidence = hybrid_score / max_possible

        matches.append((song, hybrid_score, confidence))
        alignments[song] = alignment_points

    matches.sort(key=lambda x: x[2], reverse=True)
    return (matches, alignments) if return_matches else matches
