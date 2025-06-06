from flask import Flask, jsonify, request # Make sure to import 'request'
from flask_cors import CORS
import os
import traceback

# Assuming these are in your 'src' directory and handle their respective tasks
from src.mic_record import record_audio
from src.generate_fingerprint import generate_fingerprint
from src.match import match_fingerprint
from src.plot import plot_alignment_as_base64
from src.spotify_handler import get_track_details_from_link
from src.youtube_handler import download_audio_from_youtube
from src.database import add_song 

app = Flask(__name__)
CORS(app) 

@app.route("/recognize", methods=["GET"])
def recognize():
    """Handles the song recognition request."""
    try:

        record_audio(duration=5, filename="mic_input.wav")
        fingerprints = generate_fingerprint("mic_input.wav")
        results, alignment_points = match_fingerprint(fingerprints, return_matches=True)

        matches = []
        if results:
            for r in results:
                matches.append({"title": r[0], "confidence": round(r[2], 2)})

        img_base64 = plot_alignment_as_base64(alignment_points)

        return jsonify({
            "matches": matches,
            "plot": img_base64
        })
    except Exception as e:
        traceback.print_exc() # Print full traceback for debugging
        return jsonify({"error": str(e)}), 500

@app.route("/add", methods=["POST"])
def add_song_route(): # Renamed to avoid confusion with the internal helper function name
    """
    Handles adding a song to the database from a Spotify URL provided in a POST request.
    """
    try:
        data = request.get_json() 
        spotify_link = data.get("spotify_url") 

        if not spotify_link:
            print("[ERROR] Spotify URL is missing from the request.")
            return jsonify({"error": "Spotify URL is missing"}), 400

        print(f"[INFO] Received Spotify link for adding: {spotify_link}")

        track_details = get_track_details_from_link(spotify_link)
        if not track_details:
            print(f"[ERROR] Could not fetch details for Spotify link: {spotify_link}")
            return jsonify({"error": "Invalid Spotify link or could not fetch details"}), 400

        song_name = track_details[0]
        artist_name = track_details[1][0] if track_details[1] else "Unknown Artist"
        album_name = track_details[2] 

        print(f"[INFO] Processing song: '{song_name}' by {artist_name}")

        downloaded_file_path = "downloaded_audio.mp3" 

        checkBool = download_audio_from_youtube(song_name, [artist_name], output_path=downloaded_file_path)
        if not checkBool:
            return jsonify({"error": "Failed to download audio from YouTube"}), 500

        if not os.path.exists(downloaded_file_path):
            # This check might still be useful if yt-dlp reports success but file isn't there for some edge case
            return jsonify({"error": "Downloaded audio file not found despite download attempt"}), 500
        
        fingerprints = generate_fingerprint(downloaded_file_path)
        add_song(song_name, fingerprints)

        os.remove(downloaded_file_path)
        print(f"[INFO] Successfully added '{song_name}' to the database and cleaned up temporary file.")

        return jsonify({"message": f"Song '{song_name}' by {artist_name} added successfully!"}), 200

    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": f"An error occurred while adding the song: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(port=5000, debug=True) 