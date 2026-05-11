import requests

def get_itunes_top_10():
    try:
        url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        lines = []
        entries = data.get('feed', {}).get('entry', [])
        for i, song in enumerate(entries, 1):
            title = song.get('im:name', {}).get('label')
            artist = song.get('im:artist', {}).get('label')
            lines.append(f"{i}. {artist} - {title}")
        
        return "\n".join(lines)
    except Exception as e:
        return f"Fehler beim Abrufen der Charts: {e}"

if __name__ == "__main__":
    charts = get_itunes_top_10()
    # Erstellt die Datei, die später als E-Mail-Body dient
    with open("charts.txt", "w", encoding="utf-8") as f:
        f.write("Hier sind die aktuellen iTunes Charts für diese Woche.\n")
        f.write("Kopiere die Liste einfach für TuneMyMusic:\n\n")
        f.write(charts)
        f.write("\n\nViel Spaß beim Synchronisieren!")
    print("charts.txt wurde erfolgreich erstellt.")
