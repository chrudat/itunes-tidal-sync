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
        return "Spotify Fehler: Secrets fehlen."

    try:
        # 1. Authentifizierung vorbereiten
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            redirect_uri="https://www.google.com/"
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # 2. Die Liste vorbereiten (DAS MUSS HIER STEHEN)
        output = ["\n=== SPOTIFY ABFRAGE AKTIVIERT ==="]
        
        # 3. Playlisten abrufen
        for name, p_id in playlists.items():
            output.append(f"\n--- {name} ---")
            results = sp.playlist_items(p_id, limit=10, fields='items(track(name,artists(name)))')
            for item in results['items']:
                track = item['track']
                if track:
                    artist = track['artists'][0]['name']
                    title = track['name']
                    output.append(f"{artist} - {title}")
        return "\n".join(output)

    except Exception as e:
        return f"\nSpotify Fehler: {str(e)}"

if __name__ == "__main__":
    content = fetch_spotify_group(FAV_PLAYLISTS)
    with open("part_spotify_fav.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
