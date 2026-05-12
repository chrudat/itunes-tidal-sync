import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Deine 5 "New" Playlists (IDs hier eintragen)
NEW_PLAYLISTS = {
    "New Releases 1": "63oguNCuwz51He8oxXdP58",
    "New Releases 2": "15IEm4WquzW48cFgtb7Ym7",
    "New Releases 3": "4JcT11QpxN0GoOsRmAvJLm",
    "New Releases 4": "2Ohyls4WAtQSitMMhtBgkd",
    "New Releases 5": "0HoiaN3OGkIZLJc7OhcCaG"
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
        
        output = ["\n=== 3. SPOTIFY NEW (TOP 10 JE PLAYLIST) ==="]
        
        for name, p_id in playlists.items():
            output.append(f"\n--- NEW: {name} ---")
            try:
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
        return f"\nKritischer Spotify Fehler (New): {str(e)}"

if __name__ == "__main__":
    content = fetch_spotify_group(NEW_PLAYLISTS)
    with open("part_spotify_new.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
