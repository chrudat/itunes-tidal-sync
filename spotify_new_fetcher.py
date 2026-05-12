import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Hier deine 5 "New" Spotify Playlists eintragen (z.B. Release Radar, New Music Friday)
NEW_PLAYLISTS = {
    "New Releases 1": "ID_HIER_EINTRAGEN",
    "New Releases 2": "ID_HIER_EINTRAGEN",
    "New Releases 3": "ID_HIER_EINTRAGEN",
    "New Releases 4": "ID_HIER_EINTRAGEN",
    "New Releases 5": "ID_HIER_EINTRAGEN"
}

def fetch_spotify_group(playlists):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    if not client_id or not client_secret: return "Spotify Credentials fehlen."

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    output = ["\n=== 3. SPOTIFY NEW (TOP 10 JE PLAYLIST) ==="]
    for name, p_id in playlists.items():
        output.append(f"\n--- NEW: {name} ---")
        try:
            results = sp.playlist_items(p_id, limit=10, fields='items(track(name,artists(name)))')
            for item in results['items']:
                track = item['track']
                output.append(f"{track['artists'][0]['name']} - {track['name']}")
        except Exception as e:
            output.append(f"Fehler bei {name}: {e}")
    return "\n".join(output)

if __name__ == "__main__":
    content = fetch_spotify_group(NEW_PLAYLISTS)
    with open("part_spotify_new.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
