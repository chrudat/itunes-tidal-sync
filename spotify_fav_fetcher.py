import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Hier deine 5 Standard Spotify Playlists eintragen
FAV_PLAYLISTS = {
    "Favoriten 1": "2wfH0TtehyBpTV5M4xkDRd",
    "Favoriten 2": "1iClTzJkt8IrUN82hqAMrF",
    "Favoriten 3": "1NCSSZD24g2MYEaV1eZ8x4",
    "Favoriten 4": "1Ek02NSuK1YAgctMwBnXAF",
    "Favoriten 5": "4FHKFYziOZF75AkT3aR7QP"
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
    content = fetch_spotify_group(FAV_PLAYLISTS)
    with open("part_spotify_fav.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
