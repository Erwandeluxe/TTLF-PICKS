import requests, json
from datetime import datetime
from collections import defaultdict

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

SERIES_PAIRS = {
    "det-orl": ("DET", "ORL"),
    "bos-phi": ("BOS", "PHI"),
    "nyk-atl": ("NY",  "ATL"),
    "cle-tor": ("CLE", "TOR"),
    "okc-phx": ("OKC", "PHX"),
    "sas-por": ("SA",  "POR"),
    "den-min": ("DEN", "MIN"),
    "lal-hou": ("LAL", "HOU"),
}

def get_wins():
    r = requests.get(
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
        "?seasontype=3&limit=100&dates=20260418-20260530",
        headers=HEADERS, timeout=15
    )
    r.raise_for_status()
    events = r.json().get("events", [])

    wins = defaultdict(int)
    for e in events:
        comp = e["competitions"][0]
        if not comp.get("status", {}).get("type", {}).get("completed", False):
            continue
        for t in comp["competitors"]:
            if t.get("winner"):
                wins[t["team"]["abbreviation"]] += 1
    return wins

wins = get_wins()

series = []
for sid, (t1, t2) in SERIES_PAIRS.items():
    w1 = wins.get(t1, 0)
    w2 = wins.get(t2, 0)
    if w1 > w2:
        score = f"{t1} {w1}-{w2}"
    elif w2 > w1:
        score = f"{t2} {w2}-{w1}"
    else:
        score = f"{w1}-{w2}"
    series.append({"id": sid, "score": score})

output = {
    "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "series": series
}

with open("bracket.json", "w") as f:
    json.dump(output, f, indent=2)

print("OK")
print(json.dumps(output, indent=2))
