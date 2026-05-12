import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Hier deine 5 "New" Spotify Playlists eintragen (z.B. Release Radar, New Music Friday)
NEW_PLAYLISTS = {
    "New Releases 1": "63oguNCuwz51He8oxXdP58",
    "New Releases 2": "15IEm4WquzW48cFgtb7Ym7",
    "New Releases 3": "4JcT11QpxN0GoOsRmAvJLm",
    "New Releases 4": "2Ohyls4WAtQSitMMhtBgkd",
    "New Releases 5": "0HoiaN3OGkIZLJc7OhcCaG"
}

from spotipy.oauth2 import SpotifyClientCredentials

def fetch_spotify_group(playlists):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

    try:
        # Wir verzichten auf den User-Token und gehen den offiziellen Weg für öffentliche Daten
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        output = ["\n=== SPOTIFY DATEN ==="]
        for name, p_id in playlists.items():
            output.append(f"\n--- {name} ---")
            # Wir nutzen hier eine robustere Abfrage
            results = sp.playlist_tracks(p_id, limit=10, fields='items(track(name,artists(name)))')
            for item in results['items']:
                if item['track']:
                    artist = item['track']['artists'][0]['name']
                    title = item['track']['name']
                    output.append(f"{artist} - {title}")
        return "\n".join(output)
    except Exception as e:
        return f"\nSpotify Fehler: {str(e)}"
        
if __name__ == "__main__":
    content = fetch_spotify_group(NEW_PLAYLISTS)
    with open("part_spotify_new.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
