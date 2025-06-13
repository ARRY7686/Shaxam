def get_alignment_data(alignments: dict) -> dict:
    """
    Prepare alignment data for Chart.js scatter plot.

    Args:
        alignments (dict): { "Song Name": [(x_ms, y_ms), ...] }

    Returns:
        dict: { "Song Name": [{ "x": float, "y": float }, ...] }
    """
    formatted = {}
    for song, points in alignments.items():
        formatted[song] = [{"x": x / 1000.0, "y": y / 1000.0} for x, y in points]
    return formatted
