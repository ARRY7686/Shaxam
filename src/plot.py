import librosa
import numpy as np

def get_alignment_data(alignments: dict) -> dict:
    formatted = {}
    for song, points in alignments.items():
        formatted[song] = [{"x": x / 1000.0, "y": y / 1000.0} for x, y in points]
    return formatted

def get_spectrogram_with_alignments(audio_path: str, alignments: dict, sr=22050) -> dict:
    y, sr = librosa.load(audio_path, sr=sr)
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    freq_downsample =  6  
    time_downsample =  6  

    S_db_ds = S_db[::freq_downsample, ::time_downsample]

    times = librosa.frames_to_time(np.arange(S_db_ds.shape[1]) * time_downsample, sr=sr)
    freqs = librosa.fft_frequencies(sr=sr)[::freq_downsample]

    spectrogram = []
    for t_idx, t in enumerate(times):
        for f_idx, f in enumerate(freqs):
            magnitude = S_db_ds[f_idx, t_idx]
            spectrogram.append({
                "x": round(t, 3),
                "y": round(f, 1),
                "value": round(magnitude, 2)
            })

    return {
        "spectrogram": spectrogram,
        "alignments": get_alignment_data(alignments)
    }
