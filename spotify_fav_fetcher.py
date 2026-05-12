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

def fetch_spotify_group(playlists):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    refresh_token = os.environ.get('SPOTIPY_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        return "Spotify Fehler: Secrets (ID, Secret oder Refresh Token) fehlen."

    try:
        # Auth-Manager Konfiguration
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="https://www.google.com/"
        )
        
        # Token mit dem Refresh-Token erneuern
        token_info = auth_manager.refresh_access_token(refresh_token)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        output = ["\n=== 2. SPOTIFY FAVORITEN (TOP 10 JE PLAYLIST) ==="]
        
        for name, p_id in playlists.items():
            output.append(f"\n--- {name} ---")
            try:
                # playlist_items ist die sicherste Methode für öffentliche Playlists
                results = sp.playlist_items(
                    p_id, 
                    limit=10, 
                    fields='items(track(name,artists(name)))',
                    additional_types=['track']
                )
                
                for item in results.get('items', []):
                    track = item.get('track')
                    if track:
                        artist = track['artists'][0]['name']
                        title = track['name']
                        output.append(f"{artist} - {title}")
            except Exception as playlist_error:
                output.append(f"Fehler bei dieser Playlist: {str(playlist_error)}")
                
        return "\n".join(output)

    except Exception as e:
        return f"\nKritischer Spotify Fehler (Fav): {str(e)}"

if __name__ == "__main__":
    content = fetch_spotify_group(FAV_PLAYLISTS)
    with open("part_spotify_fav.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
