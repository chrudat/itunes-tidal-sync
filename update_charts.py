import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_itunes_top_10():
    """Holt die echten iTunes Verkaufscharts (Top 10 Songs Deutschland)."""
    print("Hole Daten von den iTunes Verkaufscharts...")
    # Klassischer RSS Feed für den iTunes Store Deutschland
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    rows = []
    # Navigation durch die JSON-Struktur des klassischen Feeds
    entries = data.get('feed', {}).get('entry', [])
    
    for song in entries:
        title = song.get('im:name', {}).get('label', 'Unbekannter Titel')
        artist = song.get('im:artist', {}).get('label', 'Unbekannter Interpret')
        rows.append([title, artist])
    
    return rows

def update_sheet():
    try:
        # 1. API Setup & Authentifizierung
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        if 'GOOGLE_CREDENTIALS' not in os.environ:
            print("FEHLER: GitHub Secret 'GOOGLE_CREDENTIALS' nicht gefunden!")
            return

        creds_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
        client = gspread.authorize(creds)

        # 2. Sheet öffnen
        # WICHTIG: Name der Datei und des Tabellenblatts müssen exakt stimmen
        spreadsheet_name = "iTunes_Tidal_Sync"
        worksheet_name = "Charts"
        
        print(f"Öffne Google Sheet '{spreadsheet_name}'...")
        spreadsheet = client.open(spreadsheet_name)
        sheet = spreadsheet.worksheet(worksheet_name)

        # 3. Daten abrufen
        new_tracks = get_itunes_top_10()
        
        if not new_tracks:
            print("Keine Daten gefunden. Abbruch.")
            return

        # 4. Sheet aktualisieren
        print(f"Schreibe {len(new_tracks)} Titel in das Sheet...")
        
        # Wir leeren zuerst den Bereich A1:B10, um Platz für neue Daten zu schaffen
        # Dann schreiben wir die neuen 10 Zeilen hinein
        sheet.update('A1:B10', new_tracks)
        
        print("---")
        for i, track in enumerate(new_tracks, 1):
            print(f"{i}. {track[0]} - {track[1]}")
        print("---")
        print("Erfolg! Google Sheet wurde aktualisiert.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"FEHLER: Die Datei '{spreadsheet_name}' wurde nicht gefunden.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"FEHLER: Das Tabellenblatt '{worksheet_name}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    update_sheet()
