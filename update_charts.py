import requests
import os

def get_itunes_top_10():
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Wir erstellen ein CSV-Format: Interpret, Titel
    lines = []
    entries = data.get('feed', {}).get('entry', [])
    for song in entries:
        title = song.get('im:name', {}).get('label')
        artist = song.get('im:artist', {}).get('label')
        # Kommas in Namen entfernen, um das CSV-Format nicht zu sprengen
        clean_artist = artist.replace(",", "")
        clean_title = title.replace(",", "")
        lines.append(f"{clean_artist},{clean_title}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    content = get_itunes_top_10()
    with open("itunes_charts.csv", "w", encoding="utf-8") as f:
        f.write(content)
    print("CSV-Datei lokal erstellt.")
