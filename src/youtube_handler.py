import requests
import base64
import os
import yt_dlp
from yt_dlp import YoutubeDL

def download_audio_from_youtube(song_name,artists_names, output_path="downloaded_audio.mp3"):
    search_query = f"{song_name} by {'&'.join(artists_names)} official audio"
    print(f"[INFO] Searching for YouTube for: {search_query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
            ydl.download([info['entries'][0]['url']])
            print(f"[INFO] Downloaded audio for: {song_name} by {', '.join(artists_names)}")
            return True
    except yt_dlp.utils.DownloadError as e:
        print(f"[ERROR] Failed to download audio: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False
    