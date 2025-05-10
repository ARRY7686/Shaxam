# Shaxam

**Shaxam** is a Python-based audio fingerprinting and matching tool inspired by the Shazam algorithm. It enables you to add songs to a MySQL-backed fingerprint database and match unknown audio clips against it.

## 🎧 Features

- Generate audio fingerprints using frequency peaks and SHA-1 hashing.
- Store and manage fingerprints in a **MySQL database**.
- Match audio clips against stored songs and return confidence scores.
- Visualize alignment between input and matched songs.
- Record audio clips directly from your microphone for matching.

## 📦 Installation

Ensure you have Python 3.12+ installed.

```bash
pip install -r requirements.txt
```

Or if using `pyproject.toml`:

```bash
pip install .
```

### Database Setup

Create a MySQL database and provide the connection details using a `.env` file in the project root:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=shaxam
```

Run the initial SQL setup script (if provided) or create the necessary `songs` and `fingerprints` tables.

## 🚀 Usage

### Add a song to the database:
```bash
python main.py add path/to/song.mp3
```
You’ll be prompted to enter the song name, which will be stored with its fingerprint in MySQL.

### Match a clip against the database:
```bash
python main.py match path/to/clip.mp3
```

### Record from microphone and match:
```bash
python main.py mic {duration}
```
This command records a short audio clip via your microphone and attempts to match it against the database.

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
├── .env                     # Environment variables for DB connection
├── src/
│   ├── database.py              # Handles DB insert/query logic
│   ├── db_connection.py         # Manages MySQL connection via dotenv
│   ├── generate_fingerprint.py # Audio loading, STFT, peak detection, hashing
│   ├── match.py                 # Matching algorithm and scoring
│   ├── mic_record.py           # Microphone audio recording
│   └── plot.py                  # Visualization of alignment
├── audio/                   # Sample audio files
```

## 📚 Dependencies

- `librosa` – audio processing
- `numpy` – array operations
- `scipy` – peak filtering
- `matplotlib` – plotting match alignment
- `mysql-connector-python` – MySQL database driver
- `python-dotenv` – load DB config from `.env` file
- `sounddevice` – microphone audio capture
- `soundfile` – save recorded audio as .wav

## 🛠 Todo

- Improve fingerprint robustness
- Optimize matching for large databases
- Add GUI or web interface
