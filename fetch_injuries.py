import requests
import json
import os

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tank01-fantasy-stats.p.rapidapi.com"
}

def main():
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAPlayerList"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    body = data.get("body", [])
    print(f"Total joueurs : {len(body)}")
    with open("players_dump.json", "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
    print("Done. players_dump.json créé.")

if __name__ == "__main__":
    main()
