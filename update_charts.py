import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    try:
        # API Setup
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # Öffne das Sheet (Name muss exakt passen)
        spreadsheet_name = "iTunes_Tidal_Sync"
        print(f"Öffne Sheet '{spreadsheet_name}'...")
        sheet = client.open(spreadsheet_name).worksheet("Charts")

        # iTunes Daten holen
        print("Hole Daten von Apple...")
        url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
        response = requests.get(url)
        data = response.json()
        
        rows = []
        for song in data['feed']['entry']:
            title = song['im:name']['label']
            artist = song['im:artist']['label']
            # Wir formatieren es direkt als eine Zeile für TuneMyMusic
            rows.append([f"{title} - {artist}"])
        
        # Sheet leeren und neu befüllen
        sheet.clear()
        sheet.update('A1', rows)
        print("Erfolg! Google Sheet wurde aktualisiert.")

    except Exception as e:
        print(f"Fehler: {e}")
        raise e

if __name__ == "__main__":
    update_sheet()
