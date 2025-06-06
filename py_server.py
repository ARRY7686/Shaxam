from flask import Flask, jsonify
from src.mic_record import record_audio
from src.generate_fingerprint import generate_fingerprint
from src.match import match_fingerprint
from flask_cors import CORS
from src.plot import plot_alignment_as_base64

app = Flask(__name__)
CORS(app) 

@app.route("/recognize", methods=["GET"])
def recognize():
    try:
        record_audio(duration=5, filename="mic_input.wav")
        fingerprints = generate_fingerprint("mic_input.wav")
        results, alignment_points = match_fingerprint(fingerprints, return_matches=True)


        matches = [
            {"title": r[0], "confidence": round(r[2], 2)}
            for r in results
        ] if results else []

        img_base64 = plot_alignment_as_base64(alignment_points)

        return jsonify({
            "matches": matches,
            "plot": img_base64
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
