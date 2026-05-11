import os
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# 1. TRAGE HIER DEINE YOUTUBE PLAYLIST ID EIN:
PLAYLIST_ID = "PLUBEOViZYl4UfC1vA486sGy98MlWx_VIX"

def get_itunes_top_10():
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    data = requests.get(url).json()
    return [f"{s['im:artist']['label']} {s['im:name']['label']}" for s in data['feed']['entry']]

def update_youtube():
    # API Setup
    creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/youtube"])
    youtube = build('youtube', 'v3', credentials=creds)

    # 1. Alte Videos aus der Playlist entfernen
    res = youtube.playlistItems().list(part="id", playlistId=PLAYLIST_ID, maxResults=50).execute()
    for item in res.get('items', []):
        youtube.playlistItems().delete(id=item['id']).execute()

    # 2. Neue Songs suchen und hinzufügen
    for query in get_itunes_top_10():
        search_res = youtube.search().list(q=query, part="id", maxResults=1, type="video").execute()
        if search_res['items']:
            video_id = search_res['items'][0]['id']['videoId']
            youtube.playlistItems().insert(
                part="snippet",
                body={"snippet": {"playlistId": PLAYLIST_ID, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}
            ).execute()
            print(f"Hinzugefügt: {query}")

if __name__ == "__main__":
    update_youtube()
