import requests

def get_itunes_charts():
    try:
        url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        lines = ["\n=== 1. iTUNES VERKAUFSCHARTS (TOP 10) ==="]
        entries = data.get('feed', {}).get('entry', [])
        for i, song in enumerate(entries, 1):
            artist = song.get('im:artist', {}).get('label')
            title = song.get('im:name', {}).get('label')
            lines.append(f"{artist} - {title}")
        
        return "\n".join(lines)
    except Exception as e:
        return f"\niTunes Fehler: {e}"

if __name__ == "__main__":
    content = get_itunes_charts()
    with open("part_itunes.txt", "w", encoding="utf-8") as f:
        f.write(content + "\n")
