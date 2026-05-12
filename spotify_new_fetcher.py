import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Die IDs der "New" Playlists
NEW_PLAYLISTS = {
    "New Releases 1": "63oguNCuwz51He8oxXdP58",
    "New Releases 2": "15IEm4WquzW48cFgtb7Ym7",
    "New Releases 3": "4JcT11QpxN0GoOsRmAvJLm",
    "New Releases 4": "2Ohyls4WAtQSitMMhtBgkd",
    "New Releases 5": "0HoiaN3OGkIZLJc7OhcCaG"
}

def fetch_spotify_group(playlists):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID', '').strip()
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET', '').strip()

    if not client_id or not client_secret:
        return "Spotify Fehler: Client ID oder Secret fehlt."

    try:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        output = ["\n=== 3. SPOTIFY NEW (ÖFFENTLICH) ==="]
        
        for name, p_id in playlists.items():
            output.append(f"\n--- NEW: {name} ---")
            try:
                results = sp.playlist_tracks(
                    p_id, 
                    fields='items(track(name,artists(name)))',
                    limit=10
                )
                
                for item in results.get('items', []):
                    track = item.get('track')
                    if track:
                        artist = track['artists'][0]['name']
                        title = track['name']
                        output.append(f"{artist} - {title}")
            except Exception as e:
                output.append(f"Zugriff nicht möglich: {str(e)}")
                
        return "\n".join(output)

    except Exception as e:
        return f"\nKritischer Auth-Fehler (New): {str(e)}"

if __name__ == "__main__":
    content = fetch_spotify_group(NEW_PLAYLISTS)
    with open("part_spotify_new.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
