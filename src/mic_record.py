import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os

def record_audio(duration=5, filename="mic_input.wav", samplerate=44100) -> str:
    """
    Records audio from the microphone and saves it as a WAV file.

    Args:
        duration (int): Duration in seconds
        filename (str): Output WAV file name
        samplerate (int): Sample rate in Hz

    Returns:
        str: Path to the saved WAV file
    """
    try:
        print(f"[INFO] Recording for {duration} seconds at {samplerate} Hz...")
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
    except Exception as e:
        print(f"[ERROR] Recording failed: {e}")
        return ""

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    write(filename, samplerate, recording)
    print(f"[INFO] Saved recording to: {filename}")
    return filename
