import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# 1. TRAGE HIER DEINE ORDNER-ID EIN:
FOLDER_ID = "1kUM9c15HTv6-hbF-pSQ3bZ6NCftcu9u8"

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
    # API Setup
    creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    creds = service_account.Credentials.from_service_account_info(creds_info)
    service = build('drive', 'v3', credentials=creds)

    file_name = "itunes_charts.txt"
    
    # Suche die Datei explizit NUR in deinem Ordner
    query = f"name='{file_name}' and '{FOLDER_ID}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    fh = io.BytesIO(content.encode('utf-8'))
    media = MediaIoBaseUpload(fh, mimetype='text/plain')

    if files:
        # Datei existiert -> Update
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"Datei '{file_name}' wurde im Zielordner aktualisiert.")
    else:
        # Datei existiert nicht -> Neu erstellen MIT PARENT
        # Das 'parents' Attribut ist der Schlüssel, um die Speicher-Quota zu umgehen!
        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID]
        }
        new_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = new_file.get('id')
        print(f"Datei '{file_name}' wurde neu im Zielordner erstellt. ID: {file_id}")

if __name__ == "__main__":
    try:
        charts_text = get_itunes_top_10()
        upload_to_drive(charts_text)
    except Exception as e:
        # Diesmal geben wir den vollen Fehler aus, damit wir genau sehen, was passiert
        print(f"Fehler aufgetreten: {e}")
        raise e
