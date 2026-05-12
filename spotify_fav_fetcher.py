import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Die IDs fremder, öffentlicher Playlists
FAV_PLAYLISTS = {
    "Favoriten 1": "2wfH0TtehyBpTV5M4xkDRd",
    "Favoriten 2": "1iClTzJkt8IrUN82hqAMrF",
    "Favoriten 3": "1NCSSZD24g2MYEaV1eZ8x4",
    "Favoriten 4": "1Ek02NSuK1YAgctMwBnXAF",
    "Favoriten 5": "4FHKFYziOZF75AkT3aR7QP"
}

def fetch_spotify_group(playlists):
    # .strip() entfernt versehentliche Leerzeichen aus den GitHub Secrets
    client_id = os.environ.get('SPOTIPY_CLIENT_ID', '').strip()
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET', '').strip()

    if not client_id or not client_secret:
        return "Spotify Fehler: Client ID oder Secret fehlt in den GitHub Secrets."

    try:
        # App-only Auth: Ideal für öffentliche, fremde Daten
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        output = ["\n=== 2. SPOTIFY FAVORITEN (ÖFFENTLICH) ==="]
        
        for name, p_id in playlists.items():
            output.append(f"\n--- {name} ---")
            try:
                # playlist_tracks ist die robusteste Methode für fremde Listen
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
                
                if not results.get('items'):
                    output.append("Keine Tracks gefunden oder Playlist ist leer.")
                    
            except Exception as e:
                output.append(f"Zugriff nicht möglich: {str(e)}")
                
        return "\n".join(output)

    except Exception as e:
        return f"\nKritischer Auth-Fehler (Fav): {str(e)}"

if __name__ == "__main__":
    content = fetch_spotify_group(FAV_PLAYLISTS)
    with open("part_spotify_fav.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
