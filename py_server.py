from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import traceback
import json
import numpy as np
import sys
from src.generate_fingerprint import generate_fingerprint
from src.match import match_fingerprint
from src.spotify_handler import get_track_details_from_link
from src.youtube_handler import download_audio_from_youtube
from src.database import add_song, get_song_metadata
from src.plot import get_alignment_data, get_spectrogram_with_alignments

# Conditionally import mic recording (works locally only)
try:
    from src.mic_record import record_audio
except ImportError:
    record_audio = None

app = Flask(__name__)
CORS(app)

# Global state for spectrogram access
last_audio_path = None
last_alignments = {}

@app.route("/recognize", methods=["POST"])
def recognize():
    global last_audio_path, last_alignments
    try:
        audio_path = "mic_input.wav"

        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                return jsonify({"error": "Uploaded file has no name"}), 400
            audio_path = "uploaded_input.wav"
            uploaded_file.save(audio_path)
        else:
            if record_audio is not None:
                record_audio(duration=10, filename=audio_path)
            else:
                return jsonify({"error": "Microphone input is not supported on this server."}), 400

        fingerprints = generate_fingerprint(audio_path)
        results = match_fingerprint(fingerprints)

        matches = []
        alignments = {}
        for match in results:
            title, artist = get_song_metadata(match.song_id)
            matches.append({
                "song_id": match.song_id,
                "title": title,
                "artist": artist,
                "confidence": round(match.score, 2)
            })
            if match.points:
                alignments[f"{title}"] = match.points

        last_audio_path = audio_path
        last_alignments = alignments

        return jsonify({
            "matches": matches,
            "plot_data": get_alignment_data(alignments)
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/spectrogram", methods=["GET"])
def spectrogram():
    global last_audio_path, last_alignments
    try:
        if not last_audio_path or not last_alignments:
            return jsonify({"error": "No recognition data available"}), 400

        result = get_spectrogram_with_alignments(last_audio_path, last_alignments)

        # 🔧 Fix: Ensure all NumPy types are converted to JSON-serializable Python types
        def convert(o):
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(o, (np.float32, np.float64)):
                return float(o)
            if isinstance(o, (np.int32, np.int64)):
                return int(o)
            return o

        serializable_result = json.loads(json.dumps(result, default=convert))
        print("Spectrogram response size (bytes):", sys.getsizeof(json.dumps(serializable_result)))
        return jsonify(serializable_result)

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

        fingerprints = generate_fingerprint(downloaded_file_path)
        add_song(song_name, artist_name, "", fingerprints)

        os.remove(downloaded_file_path)

        return jsonify({"message": f"Song '{song_name}' by {artist_name} added successfully!"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(port=5000, debug=True)
