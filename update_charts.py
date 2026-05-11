import os
import json
import requests
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 1. DEINE YOUTUBE PLAYLIST ID:
PLAYLIST_ID = "PLUBEOViZYl4UfC1vA486sGy98MlWx_VIX"

def get_itunes_top_10():
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [f"{s['im:artist']['label']} {s['im:name']['label']}" for s in data['feed']['entry']]

def update_youtube():
    # API Setup mit Service Account
    creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = Credentials.from_service_account_info(
        creds_info, 
        scopes=["https://www.googleapis.com/auth/youtube"]
    )
    youtube = build('youtube', 'v3', credentials=creds)

    print("Leere alte Playlist-Einträge...")
    # 1. Alte Videos aus der Playlist abrufen
    res = youtube.playlistItems().list(
        part="id", 
        playlistId=PLAYLIST_ID, 
        maxResults=50
    ).execute()
    
    # 2. Alte Einträge löschen
    for item in res.get('items', []):
        youtube.playlistItems().delete(id=item['id']).execute()

    print("Suche neue Songs auf YouTube und füge sie hinzu...")
    # 3. Neue Songs suchen und hinzufügen
    for query in get_itunes_top_10():
        search_res = youtube.search().list(
            q=query, 
            part="id", 
            maxResults=1, 
            type="video"
        ).execute()
        
        if search_res.get('items'):
            video_id = search_res['items'][0]['id']['videoId']
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": PLAYLIST_ID, 
                        "resourceId": {"kind": "youtube#video", "videoId": video_id}
                    }
                }
            ).execute()
            print(f"Hinzugefügt: {query}")

if __name__ == "__main__":
    try:
        update_youtube()
    except Exception as e:
        print(f"Fehler: {e}")
        raise e
