import requests

def get_itunes_charts():
    try:
        url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Sektion 1: Lesbare Übersicht
        display_lines = ["=== iTUNES TOP 10 (ÜBERSICHT) ==="]
        
        # Sektion 2: Reiner Text für Copy-Paste (Künstler - Titel)
        import_lines = ["\n=== KOPIER-BLOCK FÜR TIDAL-IMPORT ==="]
        
        entries = data.get('feed', {}).get('entry', [])
        for i, song in enumerate(entries, 1):
            artist = song.get('im:artist', {}).get('label')
            title = song.get('im:name', {}).get('label')
            
            display_lines.append(f"{i:2d}. {artist} - {title}")
            import_lines.append(f"{artist} - {title}")
        
        # Zusammenführen der E-Mail
        full_content = "\n".join(display_lines) + "\n" + "\n".join(import_lines)
        
        with open("final_mail.txt", "w", encoding="utf-8") as f:
            f.write(full_content + "\n")
            
        return True
    except Exception as e:
        with open("final_mail.txt", "w", encoding="utf-8") as f:
            f.write(f"Fehler: {e}")
        return False

if __name__ == "__main__":
    get_itunes_charts()
