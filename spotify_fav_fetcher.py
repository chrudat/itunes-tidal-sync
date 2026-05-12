import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Hier deine 5 Standard Spotify Playlists eintragen
FAV_PLAYLISTS = {
    "Favoriten 1": "ID_HIER_EINTRAGEN",
    "Favoriten 2": "ID_HIER_EINTRAGEN",
    "Favoriten 3": "ID_HIER_EINTRAGEN",
    "Favoriten 4": "ID_HIER_EINTRAGEN",
    "Favoriten 5": "ID_HIER_EINTRAGEN"
}

def fetch_spotify_group(playlists):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    if not client_id or not client_secret: return "Spotify Credentials fehlen."

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    output = ["\n=== 2. SPOTIFY FAVORITEN (TOP 10 JE PLAYLIST) ==="]
    for name, p_id in playlists.items():
        output.append(f"\n--- {name} ---")
        try:
            results = sp.playlist_items(p_id, limit=10, fields='items(track(name,artists(name)))')
            for item in results['items']:
                track = item['track']
                output.append(f"{track['artists'][0]['name']} - {track['name']}")
        except Exception as e:
            output.append(f"Fehler bei {name}: {e}")
    return "\n".join(output)

if __name__ == "__main__":
    content = fetch_spotify_group(FAV_PLAYLISTS)
    with open("part_spotify_fav.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
