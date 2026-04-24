import requests, json
from datetime import datetime

SERIES_IDS = {
    "cle-tor": ("1610612739", "1610612761"),
    "bos-phi": ("1610612738", "1610612755"),
    "atl-nyk": ("1610612737", "1610612752"),
    "det-orl": ("1610612765", "1610612753"),
    "okc-phx": ("1610612760", "1610612756"),
    "lal-hou": ("1610612747", "1610612745"),
    "min-den": ("1610612750", "1610612743"),
    "por-sas": ("1610612757", "1610612759"),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept": "application/json",
}

def get_series_scores():
    url = "https://stats.nba.com/stats/commonplayoffseries?LeagueID=00&Season=2025-26&SeriesID="
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    data = r.json()
    rows = data["resultSets"][0]["rowSet"]
    headers = data["resultSets"][0]["headers"]

    # Index colonnes
    i_home = headers.index("HOME_TEAM_ID")
    i_away = headers.index("VISITOR_TEAM_ID")
    i_home_w = headers.index("HOME_TEAM_WINS")
    i_away_w = headers.index("VISITOR_TEAM_WINS")

    scores = {}
    for row in rows:
        home_id = str(row[i_home])
        away_id = str(row[i_away])
        home_w  = row[i_home_w]
        away_w  = row[i_away_w]
        for sid, (t1, t2) in SERIES_IDS.items():
            if (home_id == t1 and away_id == t2) or (home_id == t2 and away_id == t1):
                if home_id == t1:
                    scores[sid] = f"{home_w}-{away_w}"
                else:
                    scores[sid] = f"{away_w}-{home_w}"
    return scores

scores = get_series_scores()

series = []
for sid in SERIES_IDS:
    series.append({"id": sid, "score": scores.get(sid, "0-0")})

output = {
    "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "series": series
}

with open("bracket.json", "w") as f:
    json.dump(output, f, indent=2)

print("bracket.json mis à jour")
print(json.dumps(output, indent=2))
