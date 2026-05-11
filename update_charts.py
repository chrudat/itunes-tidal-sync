import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def get_itunes_top_10():
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    lines = []
    entries = data.get('feed', {}).get('entry', [])
    for song in entries:
        title = song.get('im:name', {}).get('label')
        artist = song.get('im:artist', {}).get('label')
        lines.append(f"{title} - {artist}")
    return "\n".join(lines)

def upload_to_drive(content):
    creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(creds_info)
    service = build('drive', 'v3', credentials=creds)

    file_name = "itunes_charts.txt"
    
    # Suche, ob die Datei schon existiert
    results = service.files().list(q=f"name='{file_name}'", fields="files(id)").execute()
    files = results.get('files', [])

    fh = io.BytesIO(content.encode('utf-8'))
    media = MediaIoBaseUpload(fh, mimetype='text/plain')

    if files:
        # Update bestehende Datei
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"Datei '{file_name}' wurde aktualisiert.")
    else:
        # Erstelle neue Datei
        file_metadata = {'name': file_name}
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Datei '{file_name}' wurde neu erstellt.")

if __name__ == "__main__":
    try:
        charts_text = get_itunes_top_10()
        upload_to_drive(charts_text)
    except Exception as e:
        print(f"Fehler: {e}")
