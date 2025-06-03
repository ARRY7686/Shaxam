import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_alignment(alignments):
    if not alignments:
        print("No alignment points to plot.")
        return

    sns.set(style="whitegrid", context="talk")

    plt.figure(figsize=(12, 8))

    palette = sns.color_palette("husl", len(alignments))
    for i, (song_name, points) in enumerate(alignments.items()):
        if not points:
            continue
        x_vals, y_vals = zip(*points)
        plt.scatter(x_vals, y_vals, s=60, alpha=0.8, color=palette[i], label=song_name, edgecolors='k')

        if len(x_vals) > 1:
            z = np.polyfit(x_vals, y_vals, 1)
            p = np.poly1d(z)
            plt.plot(x_vals, p(x_vals), "--", color=palette[i], alpha=0.6)

    plt.xlabel("Timestamps in Input Clip (s)", fontsize=14)
    plt.ylabel("Timestamps in Song(s) (s)", fontsize=14)
    plt.title("Fingerprint Match Alignment", fontsize=16)
    plt.legend(title="Matched Song", fontsize=12)
    plt.tight_layout()
    plt.show()
