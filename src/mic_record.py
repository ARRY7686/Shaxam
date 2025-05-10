import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(duration=5, filename="mic_input.wav", samplerate=44100):
    print(f"[INFO] Recording from mic for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    write(filename, samplerate, recording)
    print(f"[INFO] Saved recording to {filename}")
    return filename
