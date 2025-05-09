import sys
from src.generate_fingerprint import generate_fingerprint
from src.database import add_song
from src.match import match_fingerprint
from src.plot import plot_alignment

def main():
    mode = sys.argv[1]
    filepath = sys.argv[2]

    if mode == "add":
        song_name = input("Enter song name: ")
        fp = generate_fingerprint(filepath)
        add_song(song_name, fp)
        print(f"{song_name} added.")
    elif mode == "match":
        fp = generate_fingerprint(filepath)
        result, alignments = match_fingerprint(fp, return_matches=True)
        print("Matches:")
        for song, score, confidence in result:
            print(f"Matched: {song} (Confidence: {confidence * 100:.1f}%)")
            plot_alignment(alignments) 

if __name__ == "__main__":
    main()
