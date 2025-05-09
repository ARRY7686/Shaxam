# Shaxam

**Shaxam** is a Python-based audio fingerprinting and matching tool inspired by the Shazam algorithm. It enables you to add songs to a fingerprint database and match unknown audio clips against it.

## 🎧 Features

- Generate audio fingerprints using frequency peaks and SHA-1 hashing.
- Store and manage a fingerprint database in JSON format.
- Match audio clips against stored songs and return confidence scores.
- Visualize alignment between input and matched songs.

## 📦 Installation

Ensure you have Python 3.12+ installed.

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Add a song to the database:
```bash
python main.py add path/to/song.mp3
```
You’ll be prompted to enter the song name, which will be stored with its fingerprint.

### Match a clip against the database:
```bash
python main.py match path/to/clip.mp3
```

### Example Output
```
Matched: Rick Astley - Never Gonna Give You Up (Confidence: 87.5%)
```

A match alignment plot will also be displayed showing the timestamp correlation between the input clip and matched songs.

## 🗂 Project Structure

```
.
├── main.py                  # CLI entry point
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── database.py              # Handles JSON DB of fingerprints
│   ├── generate_fingerprint.py # Audio loading, STFT, peak detection, hashing
│   ├── match.py                 # Matching algorithm and scoring
│   └── plot.py                  # Visualization of alignment
├── audio/                   # Sample audio files
└── fingerprints/db.json     # Stored fingerprints
```

## 📚 Dependencies

- `librosa` – audio processing
- `numpy` – array operations
- `scipy` – peak filtering
- `matplotlib` – plotting match alignment

## 🛠 Todo

- Improve fingerprint robustness
- Optimize matching for large databases
- Add GUI or web interface


