import requests
from bs4 import BeautifulSoup
import json
import unicodedata
import re
from datetime import datetime

PLAYER_NAMES = [
  "Nickeil Alexander-Walker","Tony Bradley","Dyson Daniels","RayJ Dennis","Mouhamed Gueye","Buddy Hield","Jalen Johnson","Corey Kispert","Christian Koloko","Jonathan Kuminga","Jock Landale","CJ McCollum","Asa Newell","Georges Niang","Onyeka Okongwu","Zaccharie Risacher","Gabe Vincent","Keaton Wallace",
  "Jaylen Brown","Luka Garza","Hugo Gonzalez","Ron Harper Jr.","Sam Hauser","Payton Pritchard","Neemias Queta","Baylor Scheierman","Max Shulga","Jayson Tatum","John Tonje","Nikola Vucevic","Jordan Walsh","Derrick White","Amari Williams",
  "Jarrett Allen","Thomas Bryant","Keon Ellis","James Harden","Sam Merrill","Riley Minix","Donovan Mitchell","Evan Mobley","Larry Nance Jr.","Craig Porter Jr.","Tyrese Proctor","Dennis Schroder","Max Strus","Nae'Qwan Tomlin","Jaylon Tyson","Dean Wade",
  "Christian Braun","Bruce Brown","Aaron Gordon","Tim Hardaway Jr.","DaRon Holmes II","Cameron Johnson","Nikola Jokic","Curtis Jones","Spencer Jones","Tyus Jones","Jamal Murray","Zeke Nnaji","Jalen Pickett","KJ Simpson","Julian Strawther","Jonas Valanciunas","Peyton Watson",
  "Cade Cunningham","Jalen Duren","Javonte Green","Tobias Harris","Ronald Holland II","Kevin Huerter","Daniss Jenkins","Isaac Jones","Chaz Lanier","Caris LeVert","Wendell Moore Jr.","Paul Reed","Duncan Robinson","Marcus Sasser","Tolu Smith","Isaiah Stewart","Ausar Thompson",
  "Steven Adams","Clint Capela","Isaiah Crawford","JD Davison","Kevin Durant","Tari Eason","Dorian Finney-Smith","Jeff Green","Aaron Holiday","Josh Okogie","Alperen Sengun","Reed Sheppard","Jabari Smith Jr.","Jae'Sean Tate","Amen Thompson","Fred VanVleet",
  "Deandre Ayton","Luka Doncic","Rui Hachimura","Jaxson Hayes","Bronny James","LeBron James","Luke Kennard","Maxi Kleber","Dalton Knecht","Jake LaRavia","Chris Manon","Austin Reaves","Marcus Smart","Nick Smith Jr.","Adou Thiero","Jarred Vanderbilt",
  "Kyle Anderson","Joan Beringer","Jaylen Clark","Mike Conley","Donte DiVincenzo","Ayo Dosunmu","Anthony Edwards","Enrique Freeman","Rudy Gobert","Bones Hyland","Joe Ingles","Jaden McDaniels","Julian Phillips","Julius Randle","Naz Reid","Terrence Shannon Jr.","Rocco Zikarsky",
  "Jose Alvarado","OG Anunoby","Mikal Bridges","Jalen Brunson","Jordan Clarkson","Pacome Dadiet","Mohamed Diawara","Josh Hart","Ariel Hukporti","Trey Jemison III","Tyler Kolek","Miles McBride","Kevin McCullar Jr.","Mitchell Robinson","Landry Shamet","Jeremy Sochan","Karl-Anthony Towns",
  "Brooks Barnhizer","Branden Carlson","Alex Caruso","Luguentz Dort","Shai Gilgeous-Alexander","Isaiah Hartenstein","Chet Holmgren","Isaiah Joe","Jared McCain","Ajay Mitchell","Thomas Sorber","Nikola Topic","Cason Wallace","Aaron Wiggins","Jalen Williams","Jaylin Williams","Kenrich Williams",
  "Paolo Banchero","Desmond Bane","Goga Bitadze","Anthony Black","Jamal Cain","Jevon Carter","Wendell Carter Jr.","Colin Castleton","Kevon Harris","Jett Howard","Jonathan Isaac","Noah Penda","Jase Richardson","Jalen Suggs","Franz Wagner","Moritz Wagner","Tristan da Silva",
  "Dominick Barlow","Adem Bona","Johni Broome","Andre Drummond","VJ Edgecombe","Justin Edwards","Joel Embiid","Paul George","Quentin Grimes","Kyle Lowry","Tyrese Martin","Tyrese Maxey","Kelly Oubre Jr.","Dalen Terry","Jabari Walker","Trendon Watford",
  "Grayson Allen","Devin Booker","Koby Brea","Dillon Brooks","Amir Coffey","Ryan Dunn","Rasheer Fleming","Collin Gillespie","Jordan Goodwin","Jalen Green","Haywood Highsmith","CJ Huntley","Oso Ighodaro","Isaiah Livers","Khaman Maluach","Royce O'Neale","Mark Williams",
  "Deni Avdija","Toumani Camara","Sidy Cissoko","Donovan Clingan","Jerami Grant","Scoot Henderson","Jrue Holiday","Vit Krejci","Damian Lillard","Caleb Love","Kris Murray","Shaedon Sharpe","Matisse Thybulle","Blake Wesley","Robert Williams III","Yang Hansen","Chris Youngblood",
  "Harrison Barnes","Bismack Biyombo","Carter Bryant","Stephon Castle","Julian Champagnie","De'Aaron Fox","Dylan Harper","Harrison Ingram","Keldon Johnson","David Jones Garcia","Luke Kornet","Jordan McLaughlin","Emanuel Miller","Kelly Olynyk","Mason Plumlee","Devin Vassell","Lindy Waters III","Victor Wembanyama",
  "Scottie Barnes","RJ Barrett","Jamison Battle","Gradey Dick","Chucky Hepburn","Brandon Ingram","Trayce Jackson-Davis","A.J. Lawson","Sandro Mamukelashvili","Alijah Martin","Jonathan Mogbo","Collin Murray-Boyles","Jakob Poeltl","Immanuel Quickley","Jamal Shead","Garrett Temple","Ja'Kobe Walter"
]

def normalize(name):
    n = unicodedata.normalize("NFD", name)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return n.strip().lower()

NAMES_NORMALIZED = {normalize(n): n for n in PLAYER_NAMES}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def fetch_rotowire_injuries():
    # Essai 1 : API JSON directe RotoWire
    api_url = "https://www.rotowire.com/basketball/tables/injury-report.php?team=ALL&pos=ALL"
    try:
        r = requests.get(api_url, headers=HEADERS, timeout=20)
        if r.status_code == 200 and r.text.strip().startswith('['):
            data = r.json()
            print(f"API JSON trouvée : {len(data)} entrées")
            results = []
            for p in data:
                results.append({
                    "name":        p.get("player", ""),
                    "team":        p.get("team", ""),
                    "status":      p.get("injury_status", ""),
                    "description": p.get("injury", ""),
                    "return_date": p.get("return_date", ""),
                })
            return results
    except Exception as e:
        print(f"API JSON échouée : {e}")

    # Essai 2 : scraping HTML classique
    r = requests.get("https://www.rotowire.com/basketball/injury-report.php", headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    print(r.text[1000:3000])  # debug portion du milieu
    return []

def main():
    print("Fetching RotoWire injury list...")
    body = fetch_rotowire_injuries()
    print(f"Total lignes trouvées : {len(body)}")

    injuries = []
    for entry in body:
        key = normalize(entry["name"])
        if key not in NAMES_NORMALIZED:
            continue
        original_name = NAMES_NORMALIZED[key]
        injuries.append({
            "name":        original_name,
            "team":        entry["team"],
            "status":      entry["status"],
            "description": entry["description"],
            "return_date": entry["return_date"],
        })
        print(f"  -> {original_name} ({entry['status']})")

    output = {
        "updated_at": datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"),
        "count": len(injuries),
        "injuries": injuries
    }
    with open("injuries_rotowire.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Done. {len(injuries)} blesse(s) dans notre liste.")

if __name__ == "__main__":
    main()
