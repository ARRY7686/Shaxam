import matplotlib.pyplot as plt

def plot_alignment(alignments):
    if not alignments:
        print("No alignment points to plot.")
        return

    plt.figure(figsize=(10, 8))

    for i, (song_name, points) in enumerate(alignments.items()):
        if not points:
            continue
        x_vals, y_vals = zip(*points)
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', alpha=0.7, label=song_name)

    plt.xlabel("Timestamps in Input Clip (s)")
    plt.ylabel("Timestamps in Song(s) (s)")
    plt.title("Fingerprint Match Alignment")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
