import librosa
import numpy as np
from scipy.ndimage import maximum_filter
import hashlib

def generate_fingerprint(filepath):
    y, sr = librosa.load(filepath, sr=None)
    print(f"[INFO] Loaded {filepath} | Duration: {len(y)/sr:.2f}s | Sample Rate: {sr}")

    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    peaks = get_peaks(S_db)
    print(f"[DEBUG] Found {len(peaks)} peaks")

    fingerprints = create_hashes(peaks)
    print(f"[DEBUG] Created {len(fingerprints)} hashes")

    return fingerprints


def get_peaks(S_db, threshold=-40):
    local_max = maximum_filter(S_db, size=20)
    peaks = np.argwhere(S_db == local_max)
    peaks = [tuple(p) for p in peaks if S_db[p[0], p[1]] > threshold]
    return peaks

def create_hashes(peaks, fan_value=15):
    fingerprints = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if i + j < len(peaks):
                freq1, time1 = peaks[i]
                freq2, time2 = peaks[i + j]
                delta_t = time2 - time1
                if 0 < delta_t <= 200:
                    h = hashlib.sha1(f"{freq1}|{freq2}|{delta_t}".encode()).hexdigest()[:10]
                    fingerprints.append((h, time1))
    return fingerprints