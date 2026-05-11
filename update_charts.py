import requests

def get_itunes_top_10():
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    lines = []
    entries = data.get('feed', {}).get('entry', [])
    for i, song in enumerate(entries, 1):
        title = song.get('im:name', {}).get('label')
        artist = song.get('im:artist', {}).get('label')
        lines.append(f"{artist} - {title}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    charts = get_itunes_top_10()
    with open("charts.txt", "w", encoding="utf-8") as f:
        f.write(charts)
    print("Charts in Datei gespeichert.")
