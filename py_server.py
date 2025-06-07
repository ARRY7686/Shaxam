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
from src.database import get_song_metadata

app = Flask(__name__)
CORS(app) 

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        audio_path = "mic_input.wav"

        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                return jsonify({"error": "Uploaded file has no name"}), 400
            audio_path = "uploaded_input.wav"
            uploaded_file.save(audio_path)
        else:
            record_audio(duration=5, filename=audio_path)

        fingerprints = generate_fingerprint(audio_path)
        results = match_fingerprint(fingerprints)  # returns List[Match]

        matches = []
        for match in results:
            title, artist = get_song_metadata(match.song_id)
            matches.append({
                "song_id": match.song_id,
                "title": title,
                "artist": artist,
                "confidence": round(match.score, 2)
            })

        # If you have no alignment points, skip plotting
        img_base64 = None

        if os.path.exists(audio_path):
            os.remove(audio_path)

        return jsonify({
            "matches": matches,
            "plot": img_base64
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/add", methods=["POST"])
def add_song_route():
    try:
        data = request.get_json()
        spotify_link = data.get("spotify_url")
        if not spotify_link:
            return jsonify({"error": "Spotify URL is missing"}), 400

        track_details = get_track_details_from_link(spotify_link)
        if not track_details:
            return jsonify({"error": "Invalid Spotify link or could not fetch details"}), 400

        song_name = track_details[0]
        artist_name = track_details[1][0] if track_details[1] else "Unknown Artist"
        album_name = track_details[2]

        downloaded_file_path = "downloaded_audio.mp3"

        checkBool = download_audio_from_youtube(song_name, [artist_name], output_path="downloaded_audio")
        if not checkBool or not os.path.exists(downloaded_file_path):
            return jsonify({"error": "Failed to download audio"}), 500

        # Generate fingerprints from downloaded file
        fingerprints = generate_fingerprint(downloaded_file_path)

        # Add song with fingerprints
        add_song(song_name, artist_name, "", fingerprints)

        # Clean up file
        os.remove(downloaded_file_path)

        return jsonify({"message": f"Song '{song_name}' by {artist_name} added successfully!"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(port=5000, debug=True) 