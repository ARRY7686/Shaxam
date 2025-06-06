# 🎧 Shaxam

**Shaxam** is an Advance music recognition desktop application that allows users to identify songs through audio fingerprinting. It offers a sleek UI, real-time audio recording, Alogrithmn-based song matching, and visualization of audio fingerprint alignment.

This project combines:

- 🖥 **Electron** — For building cross-platform desktop applications.
- ⚛️ **React + Tailwind CSS** — For a responsive and animated frontend UI.
- 🐍 **Flask** — For a lightweight Python backend API.
- 📊 **Matplotlib + Seaborn** — For generating visualizations of fingerprint matches.
- 📈 **Sqlite** - A file based database which is lightweight.


---

## 🌟 Features

- 🎵 **Song Recognition**: Click a button to start listening and identifying songs in real-time.
- ⚡ **Advance Fingerprinting**: Fingerprints with the help of librosa by converting the audio file in a spectogram and finding the peaks and hashing it.
- 📈 **Fingerprint Visualization**: See a plotted graph showing how your input aligns with known tracks.
- ⚡ **Responsive & Dark-Themed UI**: Built with Tailwind for elegant, modern interfaces.
- 🔀 **Electron Integration**: Desktop-friendly, packaged React app.
- 🔊 **Microphone Input**: Captures 5 seconds of audio on recognition request.
- 🔄 **Cross-Origin Support**: CORS enabled for React ↔ Flask communication.
- 📈 **SHA-1 Hashing**: Uses SHA-1 Hashing to hash the peaks which ensure minimal hash collisions.
- 🆕 **Add Songs**: Add Songs from Spotify Links.

---

## 📦 Tech Stack

### Frontend
- **React 19**
- **Tailwind CSS 3**
- **Electron** (via `electron.js`)
- **@shadcn/ui** (UI primitives)
- **Concurrently & Wait-on** for syncing React and Electron during dev

### Backend
- **Flask** as the Python web server (`py_server.py`)
- **Flask-CORS** for cross-origin requests
- **Custom Modules**:
  - `mic_record.py` – records audio input
  - `generate_fingerprint.py` – creates audio fingerprints
  - `match.py` – performs fingerprint matching
  - `plot.py` – generates visual match alignment as base64 image
  - `spotify_handler.py` - fetches the song metadata from the spotify link using spotify Web API
  - `youtube_handler.py` - downloads the audio from web usng yt_dlp

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** ≥ v16
- **Python** ≥ 3.8
- Python dependencies (use a virtual environment):

```bash
pip install -r requirements.txt
```
Or if using ```pyproject.toml```:

```bash
    pip install .
```

### Install Frontend

```bash
cd electron-app
npm install
```
---

## ▶️ Running the App

## Get the environmental variables from spotify
```bash
  SPOTIFY_CLIENT_ID="your_client_ID"
  SPOTIFY_CLIENT_SECRET="your_client_secret"
```

### Start the Flask backend:
```bash
python py_server.py
```

### Start the Electron + React frontend:
```bash
cd electron-app
npm run electron
```

This launches:
- Flask server on **http://localhost:5000**
- React app in Electron pointing to **http://localhost:3000**

---

## 🧠 How It Works

### 🎧 Recognize Song (Real-Time)

1. User clicks **Recognize Song**.
2. React sends a `GET` request to `/recognize` on the Flask backend.
3. Flask backend:
   - Records 5 seconds of audio from the user's microphone.
   - Generates a fingerprint using audio processing.
   - Matches the fingerprint against stored fingerprints in the database.
   - Returns:
     - A list of match results (title + confidence score).
     - A base64-encoded image showing alignment of matched fingerprint points.
4. React displays the match results and renders the plot visually in the UI.

### ➕ Add Song via Spotify Link

1. User pastes a **Spotify track link** into the input field and clicks **Add Song**.
2. React sends a `POST` request to `/add` with the `spotify_url` in the request body.
3. Flask backend:
   - Extracts the track ID from the Spotify link.
   - Fetches track metadata (title, artist, album) using the Spotify API.
   - Searches YouTube for an official audio version of the track.
   - Downloads the audio using `yt-dlp`.
   - Generates a fingerprint of the audio.
   - Stores the fingerprint in the SQLite database.
   - Deletes the temporary downloaded audio file.
4. User is notified of success or failure through UI alerts.

---

## 📁 Project Structure

```plaintext
.
├── electron-app/
│   ├── public/
│   │   └── electron.js          # Main Electron process
│   ├── src/
│   │   ├── App.js               # React component with UI and logic
│   │   ├── App.css              # Tailwind styles
│   │   └── index.js             # App entry point
│   └── tailwind.config.js       # Tailwind customization
├── py_server.py                 # Flask backend
└── src/
    ├── mic_record.py            # Audio recording
    ├── generate_fingerprint.py  # Generate audio fingerprints
    ├── match.py                 # Match fingerprints
    └── plot.py                  # Plot match alignment as base64 image
    └── spotify_handler.py       # fetches the song metadata from the spotify link using spotify Web API
    └── youtube_handler.py       # downloads the audio from web usng yt_dl      
```

---

## ⚙️ Scripts

In `electron-app/`:

```bash
npm start         # Starts React only
npm run electron  # Starts both React and Electron in parallel
```

---

## 🖼 Fingerprint Plot Example

- Visualizes matching points between input and stored tracks.
- Rendered using `matplotlib`, sent as base64 string to frontend and shown in `<img />`.

---

## 🛡 CORS Support

Flask backend has CORS enabled for smooth communication between Electron (localhost:3000) and Flask (localhost:5000).

---
## Future Plans

also Let the user get the audio from the device they are using

## 📌 Notes

- Fingerprint generation and matching logic assumed to be implemented in custom modules under `src/`.
- App supports hot-reloading for React changes.
- Uses Tailwind dark mode via `class="dark"` in HTML.