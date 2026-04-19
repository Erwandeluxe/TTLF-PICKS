import requests
import json
import os
from datetime import datetime

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tank01-fantasy-stats.p.rapidapi.com"
}

def load_mapping():
    with open("ttlf_tank01_mapping.json", encoding="utf-8") as f:
        return json.load(f)

def fetch_injuries():
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAInjuryList"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json().get("body", [])

def main():
    mapping = load_mapping()
    # Inverser : playerID → nom TTLF
    id_to_name = {info["playerID"]: name for name, info in mapping.items()}

    print("Fetching injury list...")
    body = fetch_injuries()
    print(f"Total blessés dans l'API : {len(body)}")

    injuries = []
    for entry in body:
        pid = entry.get("playerID", "")
        if pid not in id_to_name:
            continue
        ttlf_name = id_to_name[pid]
        ret = entry.get("injReturnDate", "")
        if ret and len(ret) == 8:
            ret = f"{ret[6:8]}/{ret[4:6]}/{ret[0:4]}"
        injuries.append({
            "name": ttlf_name,
            "team": entry.get("team", ""),
            "status": entry.get("designation", "?"),
            "description": entry.get("description", ""),
            "return_date": ret,
        })
        print(f"  → {ttlf_name} ({entry.get('designation','?')})")

    output = {
        "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"),
        "count": len(injuries),
        "injuries": injuries
    }
    with open("injuries.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Done. {len(injuries)} blessé(s) dans notre liste.")

if __name__ == "__main__":
    main()
