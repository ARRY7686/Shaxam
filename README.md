# 🎧 Shaxam

**Shaxam** is an Advance music recognition desktop application that allows users to identify songs through audio fingerprinting. It offers a sleek UI, real-time audio recording, Alogrithmn-based song matching, and visualization of audio fingerprint alignment.

This project combines:

- 🖥 **Electron** — For building cross-platform desktop applications.
- ⚛️ **React + Tailwind CSS** — For a responsive and animated frontend UI.
- 🐍 **Flask** — For a lightweight Python backend API.
- 📊 **Matplotlib + Seaborn** — For generating visualizations of fingerprint matches.

---

## 🌟 Features

- 🎵 **Song Recognition**: Click a button to start listening and identifying songs in real-time.
- ⚡ **Advance Fingerprinting**: Fingerprints with the help of librosa by converting the audio file in a spectogram and finding the peaks and hashing it.
- 📈 **Fingerprint Visualization**: See a plotted graph showing how your input aligns with known tracks.
- ⚡ **Responsive & Dark-Themed UI**: Built with Tailwind for elegant, modern interfaces.
- 🔀 **Electron Integration**: Desktop-friendly, packaged React app.
- 🔊 **Microphone Input**: Captures 5 seconds of audio on recognition request.
- 🔄 **Cross-Origin Support**: CORS enabled for React ↔ Flask communication.
- 📈 **SHA-1 Hashing**: Uses SHA-1 Hashing to hash the peaks which ensure minimal hash collisions

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

1. User clicks **Recognize Song**.
2. React sends a GET request to `/recognize` on the Flask server.
3. Flask:
   - Records 5 seconds of audio.
   - Generates fingerprints.
   - Matches against known fingerprints.
   - Returns:
     - Match results (titles + confidence).
     - A base64-encoded PNG plot of fingerprint alignment.
4. React displays results and renders plot in the UI.

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

Let user add their own songs and help train the database.

## 📌 Notes

- Fingerprint generation and matching logic assumed to be implemented in custom modules under `src/`.
- App supports hot-reloading for React changes.
- Uses Tailwind dark mode via `class="dark"` in HTML.