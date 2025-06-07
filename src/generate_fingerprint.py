import librosa
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class Peak:
    time: float          # in seconds
    freq: float          # frequency bin

@dataclass
class Couple:
    anchor_time_ms: int
    song_id: int

TARGET_ZONE_SIZE = 5  # max target points per anchor 


from typing import Optional

def generate_fingerprint(filepath: str, song_id: Optional[int] = None) -> Dict[int, Couple]:
    y, sr = librosa.load(filepath, sr=None)
    print(f"[INFO] Loaded {filepath} | Duration: {len(y)/sr:.2f}s | Sample Rate: {sr}")

    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=512))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    peaks = extract_peaks(S_db, sr, hop_length=512)
    print(f"[DEBUG] Found {len(peaks)} peaks")

    fingerprints = create_fingerprints(peaks, song_id)
    print(f"[DEBUG] Created {len(fingerprints)} fingerprints")

    return fingerprints


def create_fingerprints(peaks: List[Peak], song_id: Optional[int]) -> Dict[int, Couple]:
    fingerprints = {}
    for i, anchor in enumerate(peaks):
        for j in range(i + 1, min(len(peaks), i + 1 + TARGET_ZONE_SIZE)):
            target = peaks[j]
            address = create_address(anchor, target)
            anchor_time_ms = int(anchor.time * 1000)
            # If song_id is None, store placeholder -1 or None
            fingerprints[address] = Couple(anchor_time_ms, song_id if song_id is not None else -1)
    return fingerprints



def extract_peaks(S_db: np.ndarray, sr: int, hop_length: int) -> List[Peak]:
    from scipy.ndimage import maximum_filter

    local_max = maximum_filter(S_db, size=20)
    peaks = np.argwhere(S_db == local_max)

    peak_list = []
    for freq_bin, time_bin in peaks:
        if S_db[freq_bin, time_bin] > -40:  # Threshold (in dB)
            time = time_bin * hop_length / sr
            peak_list.append(Peak(time, freq_bin))
    return peak_list




def create_address(anchor: Peak, target: Peak) -> int:
    anchor_freq = int(anchor.freq)
    target_freq = int(target.freq)
    delta_ms = int((target.time - anchor.time) * 1000)

    address = (anchor_freq << 23) | (target_freq << 14) | delta_ms
    return address
