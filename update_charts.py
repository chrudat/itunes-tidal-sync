def get_itunes_top_10():
    # Klassischer iTunes RSS Feed für die Top 10 Verkaufscharts
    url = "https://itunes.apple.com/de/rss/topsongs/limit=10/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    rows = []
    # Das Format ist hier: feed -> entry
    for song in data['feed']['entry']:
        title = song['im:name']['label']
        artist = song['im:artist']['label']
        rows.append([title, artist])
    return rows
