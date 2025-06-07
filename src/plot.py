import matplotlib
matplotlib.use("Agg")  # Use headless backend for non-GUI environments

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64

def plot_alignment_as_base64(alignments: dict) -> str:
    """
    Generate a base64-encoded PNG plot showing alignment of fingerprint matches.
    
    Args:
        alignments (dict): {
            "Song Name": [(sample_time_ms, db_time_ms), ...],
            ...
        }

    Returns:
        str: base64-encoded image (or None if empty)
    """
    if not alignments:
        return None

    sns.set(style="whitegrid", context="talk")
    plt.figure(figsize=(12, 8))

    palette = sns.color_palette("husl", len(alignments))

    for i, (song_name, points) in enumerate(alignments.items()):
        if not points:
            continue

        # Convert ms to seconds for readability
        x_vals, y_vals = zip(*points)
        x_vals = [x / 1000.0 for x in x_vals]
        y_vals = [y / 1000.0 for y in y_vals]

        plt.scatter(
            x_vals,
            y_vals,
            s=60,
            alpha=0.8,
            color=palette[i],
            label=song_name
        )

        if len(x_vals) > 1:
            z = np.polyfit(x_vals, y_vals, 1)
            p = np.poly1d(z)
            plt.plot(x_vals, p(x_vals), "--", color=palette[i], alpha=0.6)

    plt.xlabel("Input Clip Time (s)", fontsize=14)
    plt.ylabel("Matched Song Time (s)", fontsize=14)
    plt.title("Fingerprint Alignment Plot", fontsize=16)
    plt.legend(title="Songs", fontsize=10)
    plt.tight_layout()

    # Output image to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64
