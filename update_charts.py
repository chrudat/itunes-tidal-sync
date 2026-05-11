import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# API Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Öffne das Sheet (Name muss exakt passen)
sheet = client.open("iTunes_Tidal_Sync").worksheet("Charts")

def get_itunes_top_10():
    url = "https://rss.marketingtools.apple.com/api/v2/de/music/most-played/10/songs.json"
    response = requests.get(url)
    data = response.json()
    
    rows = []
    for song in data['feed']['results']:
        title = song['name']
        artist = song['artistName']
        rows.append([title, artist])
    return rows

def update_sheet():
    new_tracks = get_itunes_top_10()
    
    # Bestehende Daten löschen (außer Header, falls vorhanden)
    # Hier überschreiben wir einfach die Zellen A1 bis B10
    cell_list = sheet.range('A1:B10')
    
    flat_list = []
    for row in new_tracks:
        flat_list.extend(row)
        
    for i, val in enumerate(flat_list):
        cell_list[i].value = val
        
    sheet.update_cells(cell_list)
    print("Google Sheet erfolgreich aktualisiert!")

if __name__ == "__main__":
    update_sheet()
