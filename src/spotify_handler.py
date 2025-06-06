import requests
import base64
import os
import dotenv

dotenv.load_dotenv(override=True)

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
    exit()

def get_spotify_access_token(client_id, client_secret):
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status() # Raise an exception for bad status codes
    token_info = response.json()
    return token_info["access_token"]

def get_track_id_from_link(spotify_link):
    # Example: https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6?si=...
    parts = spotify_link.split('/')
    if 'track' in parts:
        track_index = parts.index('track')
        if len(parts) > track_index + 1:
            track_id_with_params = parts[track_index + 1]
            track_id = track_id_with_params.split('?')[0]
            return track_id
    return None
def get_track_details(track_id, access_token):
    track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(track_url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return(
        [response_data["name"],  # Track name
        [artist["name"] for artist in response_data["artists"]],  # List of artist names
        response_data["album"]["name"]]  # Album name
    )


def get_track_details_from_link(spotify_link):
    track_id = get_track_id_from_link(spotify_link)
    if not track_id:
        raise ValueError("Invalid Spotify track link")

    access_token = get_spotify_access_token(CLIENT_ID, CLIENT_SECRET)
    return get_track_details(track_id, access_token)