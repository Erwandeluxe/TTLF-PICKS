import requests
import json
import os
import unicodedata
from datetime import datetime

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

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
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "tank01-fantasy-stats.p.rapidapi.com"
}

def fetch_injuries():
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBAInjuryList"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def main():
    print("Fetching injury list...")
    data = fetch_injuries()
    body = data.get("body", [])
    print(f"Total blessés dans l'API : {len(body)}")

    injuries = []
    for entry in body:
        raw_name = entry.get("longName", "")
        key = normalize(raw_name)
        if key not in NAMES_NORMALIZED:
            continue
        original_name = NAMES_NORMALIZED[key]
        ret = entry.get("injReturnDate", "")
        if ret and len(ret) == 8:
            ret = f"{ret[6:8]}/{ret[4:6]}/{ret[0:4]}"
        injuries.append({
            "name": original_name,
            "team": entry.get("team", ""),
            "status": entry.get("designation", "?"),
            "description": entry.get("description", ""),
            "return_date": ret,
        })
        print(f"  → Trouvé : {original_name} ({entry.get('designation','?')})")

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
