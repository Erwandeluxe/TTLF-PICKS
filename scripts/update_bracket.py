import requests, json
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Mapping ESPN team abbreviation → ID bracket HTML
TEAM_MAP = {
    "DET": "det", "ORL": "orl",
    "BOS": "bos", "PHI": "phi",
    "NYK": "nyk", "ATL": "atl",
    "CLE": "cle", "TOR": "tor",
    "OKC": "okc", "PHX": "phx",
    "SA":  "sas", "POR": "por",
    "DEN": "den", "MIN": "min",
    "LAL": "lal", "HOU": "hou",
}

SERIES_IDS = {
    frozenset(["DET","ORL"]): "det-orl",
    frozenset(["BOS","PHI"]): "bos-phi",
    frozenset(["NYK","ATL"]): "nyk-atl",
    frozenset(["CLE","TOR"]): "cle-tor",
    frozenset(["OKC","PHX"]): "okc-phx",
    frozenset(["SA","POR"]):  "sas-por",
    frozenset(["DEN","MIN"]): "den-min",
    frozenset(["LAL","HOU"]): "lal-hou",
}

def get_series():
    # Récupère tous les matchs playoffs ESPN
    r = requests.get(
        "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?seasontype=3&limit=50",
        headers=HEADERS, timeout=15
    )
    r.raise_for_status()
    events = r.json().get("events", [])

    wins = {}  # serie_id -> {abbr: wins}
    for event in events:
        comp = event["competitions"][0]
        teams = comp["competitors"]
        abbrs = [t["team"]["abbreviation"] for t in teams]
        key = frozenset(abbrs)
        sid = SERIES_IDS.get(key)
        if not sid:
            continue
        if sid not in wins:
            wins[sid] = {a: 0 for a in abbrs}
        # winner
        for t in teams:
            if t.get("winner"):
                wins[sid][t["team"]["abbreviation"]] = wins[sid].get(t["team"]["abbreviation"], 0) + 1

    series = []
    for sid, w in wins.items():
        items = sorted(w.items(), key=lambda x: -x[1])
        if len(items) == 2:
            a1, w1 = items[0]
            a2, w2 = items[1]
            score = f"{a1} {w1}-{w2}" if w1 != w2 else f"{w1}-{w2}"
        else:
            score = "—"
        series.append({"id": sid, "score": score})

    return series

series = get_series()
output = {
    "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "series": series
}

with open("bracket.json", "w") as f:
    json.dump(output, f, indent=2)

print("OK")
print(json.dumps(output, indent=2))
