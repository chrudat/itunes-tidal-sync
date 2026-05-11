import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    try:
        # 1. API Setup
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # 2. Sheet öffnen
        spreadsheet_name = "iTunes_Tidal_Sync"
        print(f"Öffne Sheet '{spreadsheet_name}'...")
        sheet = client.open(spreadsheet_name).worksheet("Charts")

        # 3. iTunes Daten holen (Verkaufscharts)
        print("Hole Daten von Apple...")
        url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        rows = []
        entries = data.get('feed', {}).get('entry', [])
        
        for song in entries:
            title = song.get('im:name', {}).get('label')
            artist = song.get('im:artist', {}).get('label')
            # Struktur: Interpret in Spalte A, Titel in Spalte B
            rows.append([artist, title])
        
        # 4. Sheet aktualisieren
        # Wir leeren alles und schreiben die 10 neuen Zeilen ab A1
        sheet.clear()
        sheet.update('A1', rows)
        
        print("Erfolg! Google Sheet wurde mit Interpret (A) und Titel (B) aktualisiert.")
        for r in rows:
            print(f"Eingetragen: {r[0]} - {r[1]}")

    except Exception as e:
        print(f"Fehler: {e}")
        raise e

if __name__ == "__main__":
    update_sheet()
