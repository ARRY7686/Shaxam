import sys
from src.generate_fingerprint import generate_fingerprint
from src.database import add_song
from src.match import match_fingerprint
from src.plot import plot_alignment
from src.mic_record import record_audio  # You defined this in mic_record.py

print("Imports Successful!")

def main():
    mode = sys.argv[1]

    if mode == "add":
        filepath = sys.argv[2]
        song_name = input("Enter song name: ")
        fp = generate_fingerprint(filepath)
        add_song(song_name, fp)
        print(f"{song_name} added.")

    elif mode == "match":
        filepath = sys.argv[2]
        fp = generate_fingerprint(filepath)
        result, alignments = match_fingerprint(fp, return_matches=True)
        print("Matches:")
        for song, score, confidence in result:
            print(f"Matched: {song} (Confidence: {confidence * 100:.1f}%)")
            plot_alignment(alignments)

    elif mode == "mic":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        filepath = record_audio(duration=duration)
        fp = generate_fingerprint(filepath)
        result, alignments = match_fingerprint(fp, return_matches=True)
        print("Matches:")
        for song, score, confidence in result:
            print(f"Matched: {song} (Confidence: {confidence * 100:.1f}%)")
            plot_alignment(alignments)

if __name__ == "__main__":
    main()
