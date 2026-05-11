import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    try:
        # API Setup
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if 'GOOGLE_CREDENTIALS' not in os.environ:
            print("FEHLER: Secret GOOGLE_CREDENTIALS wurde nicht gefunden!")
            return

        creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)

        # Öffne das Sheet
        sheet_name = "iTunes_Tidal_Sync"
        print(f"Versuche Sheet '{sheet_name}' zu öffnen...")
        spreadsheet = client.open(sheet_name)
        sheet = spreadsheet.worksheet("Charts")

        # iTunes Daten holen
        print("Hole Daten von Apple...")
        url = "https://rss.marketingtools.apple.com/api/v2/de/music/most-played/10/songs.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        rows = []
        for song in data['feed']['results']:
            rows.append([song['name'], song['artistName']])
        
        # Daten schreiben
        print("Schreibe Daten in das Sheet...")
        # Wir schreiben ab Zelle A1
        sheet.update('A1:B10', rows)
        
        print("Erfolg! Google Sheet wurde aktualisiert.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"FEHLER: Das Sheet '{sheet_name}' wurde nicht gefunden. Namen prüfen!")
    except gspread.exceptions.WorksheetNotFound:
        print("FEHLER: Das Tabellenblatt 'Charts' wurde nicht gefunden!")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    update_sheet()
