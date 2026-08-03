#!/usr/bin/env python3
"""Build the BD Landscape Universe dataset + single-file interactive web app."""
import json, html

# ------------------------------------------------------------------ #
#  STANDARDIZED DATA MODEL                                            #
#  Node types: company, division, project, player, person            #
# ------------------------------------------------------------------ #

COMPANY = "Paramount"

# division_group -> hue color (category bands, universe theme)
DIVISIONS = {
    "Paramount Pictures":   "#e0564a",
    "Paramount+ / DTC":     "#4a9fe0",
    "MTV / Brand Studio":   "#c05ad0",
    "Pluto TV":             "#e0a24a",
    "Paramount Advertising":"#5ad0a8",
    "CBS":                  "#7d8fe0",
    "Nickelodeon":          "#e0d24a",
    "BET":                  "#8a6bd0",
    "Paramount Sports":     "#5ad0d0",
    "Other":                "#8a8f9a",
}

# projects: (name, division, [type_tags], confidence, [contacts], [players])
PROJECTS = [
    ("Pluto TV fall brand campaign", "Pluto TV", ["Brand Campaign","Creative Development","Production"], "High", ["Katherine Kelly"], ["Versus"]),
    ("Paramount+ UFC opener", "Paramount+ / DTC", ["Title & Launch","Motion & VFX","Trailer & Spot"], "High", [], ["Versus"]),
    ("Mountain of Entertainment – rich 3D environment", "Paramount+ / DTC", ["Design & Identity","Motion & VFX","Digital & UX"], "High", [], ["Versus","Droga5"]),
    ("Monsta – Times Square", "Pluto TV", ["OOH & Print","Motion & VFX","Design & Identity"], "High", [], ["Versus"]),
    ("SpongeBob on the Sphere – Super Bowl LVIII", "Nickelodeon", ["Experiential & Events","Motion & VFX","Social & Creator"], "High", ["Sabrina Caluori"], ["Versus"]),
    ("You Can Count on Sundays", "Paramount Sports", ["360 / Integrated","Sports","Film & Branded Content"], "High", ["Kelly Dunne","Michael Benson","Terry Minogue"], []),
    ("The Naked Gun – AV & digital campaign", "Paramount Pictures", ["Trailer & Spot","Social & Creator"], "High", ["Josh Goldstine"], ["Workshop Creative"]),
    ("The Naked Gun – OOH", "Paramount Pictures", ["OOH & Print","Design & Identity"], "High", [], ["Midnight Oil (Imagine Group)"]),
    ("The Naked Gun x ESPN", "Paramount Pictures", ["Media & Sponsorship","Film & Branded Content","Sports"], "Medium", [], ["ESPN"]),
    ("The Running Man x Liquid Death", "Paramount Pictures", ["Brand Integration","Social & Creator"], "High", [], ["Liquid Death"]),
    ("The Running Man – Reddit interactive pilot", "Paramount Pictures", ["Interactive & Gaming"], "High", [], ["Spark Foundry / Publicis","Reddit"]),
    ("SpongeBob Movie: Search for SquarePants – intl social", "Paramount Pictures", ["Social & Creator","Design & Identity","Motion & VFX"], "High", [], ["Once Upon a Time LA"]),
    ("SpongeBob Movie x Burger King", "Paramount Pictures", ["Consumer & Retail"], "Medium", [], ["Burger King"]),
    ("Scream 7 – Discord playable experience", "Paramount Pictures", ["Interactive & Gaming","Performance & Commerce"], "High", [], ["Spark Foundry / Publicis","Discord","Those Beyond"]),
    ("Scream 7 – Flighthouse social", "Paramount Pictures", ["Social & Creator"], "Medium", [], ["Flighthouse Media"]),
    ("Scream 7 – Big Game spot", "Paramount Pictures", ["Trailer & Spot","Media & Sponsorship"], "Medium", [], []),
    ("Tracker stays – AutoCamp & Hilton Honors", "CBS", ["Experiential & Events","Media & Sponsorship"], "High", ["Michael Benson"], ["AutoCamp","Hilton Honors"]),
    ("NCIS Tuesdays of Honor: A Salute to Service", "CBS", ["Brand Campaign","Title & Launch"], "High", [], []),
    ("BET Media House", "BET", ["Film & Branded Content","Live & Tentpole"], "High", ["Tiyale Hayes"], ["P&G"]),
    ("Black + Iconic Soiree", "BET", ["Experiential & Events","Film & Branded Content"], "High", ["Tiyale Hayes"], ["Gilead","P&G"]),
    ("BET Awards 2026", "BET", ["Live & Tentpole","Brand Integration","Trailer & Spot"], "High", ["Connie Orlando","Tiyale Hayes"], ["Jesse Collins Entertainment"]),
    ("Nickelodeon Fun-ergy Factory – Comic-Con", "Nickelodeon", ["Experiential & Events","Interactive & Gaming","Social & Creator"], "High", [], ["New Children's Museum"]),
    ("2025 MTV VMAs – partner platform", "MTV / Brand Studio", ["Live & Tentpole","Film & Branded Content","Brand Integration"], "High", ["Dario Spina","Matthew Newcomb"], []),
    ("Dunkin x VMAs – Megan Stalter stunt", "MTV / Brand Studio", ["Film & Branded Content","Social & Creator"], "High", [], ["Dunkin","Gravy Films","Artists Equity"]),
    ("Bacardi x VMAs", "MTV / Brand Studio", ["Media & Sponsorship","Live & Tentpole"], "High", ["Matthew Newcomb"], ["Bacardi"]),
    ("Burger King x VMAs", "MTV / Brand Studio", ["Trailer & Spot","Design & Identity","Editorial & Post"], "High", [], ["Bark Bark","Burger King"]),
    ("Red Bull x VMAs / MrBeast activation", "MTV / Brand Studio", ["Experiential & Events","Social & Creator","Film & Branded Content"], "Medium", ["Dario Spina"], ["Red Bull"]),
    ("Paramount Ads Manager Agency Partner Program", "Paramount Advertising", ["Performance & Commerce","Creative Development"], "High", [], ["AllCreativeMedia","New Path Digital"]),
    ("Performance Multiplier with Taboola", "Paramount Advertising", ["Performance & Commerce"], "High", [], ["Taboola"]),
    ("Dynamic fixed ad units with Omnicom Media", "Paramount Advertising", ["Performance & Commerce","Media & Sponsorship"], "High", [], ["Omnicom Media"]),
    ("Find Your Mountain", "Paramount+ / DTC", ["Brand Campaign","Film & Branded Content"], "High", [], ["Droga5","Stink Films / Traktor","Arcade Edit"]),
    ("Nobody Watches Like U.S.", "Paramount Sports", ["Film & Branded Content","Sports","Brand Campaign"], "High", ["Rob Stecklow"], ["72andSunny","Smuggler","Trafik","Iconic","Barking Owl","Soundtree"]),
    ("Yellowjackets FYC", "Paramount+ / DTC", ["Editorial & Post","Design & Identity"], "High", ["Liza Burnett Fefferman","Rene Ridinger","Katherine Allen"], ["TCO London"]),
    ("A Mountain of Entertainment – extended platform", "Paramount+ / DTC", ["Brand Campaign","Motion & VFX","Film & Branded Content","Social & Creator"], "High", ["Domenic DiMeglio","Terry Minogue","Matt Hernandez","Emmanuelle Leboeuf"], ["Droga5","O Positive","Arcade Edit","Human","Parliament","Titmouse","Heard City","Rare Medium"]),
    ("Killer Classics – Halloween stunt", "Other", ["Motion & VFX","Trailer & Spot","Audio"], "High", [], []),
    ("Star Trek: Strange New Worlds – Worlds Collide", "Paramount+ / DTC", ["Title & Launch","360 / Integrated"], "High", [], []),
    ("Team Moms", "Paramount Sports", ["Film & Branded Content","Sports","Media & Sponsorship"], "Medium", ["Jesse Sisgold"], ["ITV America","Kim Kardashian Productions"]),
    ("Feel the Free", "Pluto TV", ["Brand Campaign","Film & Branded Content"], "Medium", [], ["O Positive"]),
    ("Dutton Ranch at SXSW", "Paramount+ / DTC", ["Experiential & Events","Media & Sponsorship"], "High", ["Shawn Silverman"], ["Fairmont Austin"]),
]

# player metadata: name -> (type, repeat_bool)
PLAYER_META = {
    "Versus": ("Home team – creative/production/post", True),
    "Droga5": ("Agency – brand platform / lead creative", True),
    "72andSunny": ("Agency – lead creative / sports", False),
    "Workshop Creative": ("Agency – theatrical AV / digital", False),
    "Once Upon a Time LA": ("Agency – entertainment design / social", False),
    "Bark Bark": ("Agency – branded content / integrated studio", False),
    "TCO London": ("Agency – editorial / FYC", False),
    "Spark Foundry / Publicis": ("Agency – media / platform activation", True),
    "AllCreativeMedia": ("Agency – SMB CTV / Ads Manager partner", False),
    "New Path Digital": ("Agency – SMB CTV / Ads Manager partner", False),
    "O Positive": ("Production – live-action", True),
    "Arcade Edit": ("Post / editorial", True),
    "Gravy Films": ("Production – live-action", False),
    "Those Beyond": ("Interactive / games", False),
    "Flighthouse Media": ("Platform-native social", False),
    "Midnight Oil (Imagine Group)": ("OOH / print / design", False),
    "Jesse Collins Entertainment": ("Production – live tentpole", False),
    "Stink Films / Traktor": ("Production company / director collective", False),
    "Smuggler": ("Production company (dir. Tom Hooper)", False),
    "Trafik": ("VFX & color", False),
    "Iconic": ("Post / editorial", False),
    "Barking Owl": ("Music / audio", False),
    "Soundtree": ("Music", False),
    "Human": ("Post / design specialist", True),
    "Parliament": ("Production / post specialist", True),
    "Titmouse": ("Animation", True),
    "Heard City": ("Music / audio / sound", True),
    "Rare Medium": ("Design / production specialist", True),
    "ITV America": ("Production company", False),
    "Kim Kardashian Productions": ("Celebrity production company", False),
    "Artists Equity": ("Production collaborator (verify)", False),
    "New Children's Museum": ("Venue / community partner", False),
    "Fairmont Austin": ("Hospitality / experiential partner", False),
    "AutoCamp": ("Hospitality / experiential partner", False),
    "Hilton Honors": ("Loyalty partner", False),
    "Reddit": ("Platform / interactive media", False),
    "Discord": ("Platform", False),
    "Taboola": ("Ad-tech partner", False),
    "Omnicom Media": ("Agency / media product partner", False),
    "ESPN": ("Media partner", False),
    "Liquid Death": ("Brand / creative engine", False),
    "Dunkin": ("Advertiser brand", False),
    "Bacardi": ("Advertiser brand", False),
    "Burger King": ("Advertiser brand / retail partner", True),
    "Red Bull": ("Advertiser brand", False),
    "P&G": ("Sponsor", True),
    "Gilead": ("Sponsor", False),
}

# signature colors for recurring players (Rob's "purple = Anomaly" convention).
# Versus gets the reserved home-team gold.
SIGNATURE_COLORS = {
    "Versus": "#ffd24a",
    "Droga5": "#b06bff",           # purple family = anchor agency (Rob's convention)
    "Spark Foundry / Publicis": "#ff7ab0",
    "O Positive": "#5ad0ff",
    "Arcade Edit": "#7affc0",
    "Burger King": "#ff9d4a",
    "Human": "#a0e060",
    "Parliament": "#e0a0ff",
    "Titmouse": "#ff6b6b",
    "Heard City": "#6bd0ff",
    "Rare Medium": "#d0ff6b",
    "P&G": "#8fd0e0",
}

# people: name -> (division, title, role_label, confidence, route, score|None)
PEOPLE = {
    "David Ellison":       ("Enterprise", "Chairman & CEO", "Executive sponsor / likely DM", "High", "No route identified", None),
    "Jay Askinasi":        ("Paramount Advertising", "Chief Revenue Officer", "Exec sponsor (Brand Studio/Ads) / likely DM", "High", "No direct route", None),
    "Cindy Holland":       ("Paramount+ / DTC", "Chair, Direct-to-Consumer", "Executive sponsor / likely DM", "High", "No direct route", None),
    "Domenic DiMeglio":    ("Paramount+ / DTC", "EVP, CMO & Chief Data Officer, Streaming", "Senior budget owner / likely DM", "Medium", "Senior route; no warm evidence", 74),
    "Michelle Garcia":     ("Paramount+ / DTC", "EVP, Consumer Marketing, DTC", "Budget owner / likely DM", "High", "No internal contact evidence", 81),
    "Shawn Silverman":     ("Paramount+ / DTC", "SVP, Global Head of Title Marketing, P+", "Title budget owner / confirmed commissioner", "High", "No internal contact evidence", 81),
    "Becca Schader":       ("Paramount+ / DTC", "SVP, Creative Marketing, Paramount+", "Creative budget owner / likely DM", "High", "No internal contact evidence", 81),
    "Matt Hernandez":      ("Paramount+ / DTC", "SVP, Head of Design, Paramount Streaming", "Senior creative buyer / likely DM", "High", "Named in Versus contact list", 93),
    "Emmanuelle Leboeuf":  ("Paramount+ / DTC", "Creative Director, Paramount+", "Day-to-day creative buyer / confirmed stakeholder", "High", "Named in Versus contact list", 91),
    "Laura Kane":          ("Paramount+ / DTC", "Senior Creative Director, Paramount+", "Day-to-day creative buyer / likely DM", "Medium", "Named in Versus contact list", 91),
    "Katherine Kelly":     ("Pluto TV", "Senior Director, Campaign Management, Pluto TV", "Active-account route / likely DM", "Medium", "Current Versus work in same team", 96),
    "Eve Seiter":          ("Paramount+ / DTC", "Senior Campaign Manager, Paramount", "Operational recommender / confirmed stakeholder", "Medium", "Named in Versus contact list", 85),
    "Dara Driscoll":       ("Paramount+ / DTC", "Campaign Project Manager, Paramount+", "Scoping / vendor coordination", "Medium", "Named in Versus contact list", 85),
    "Ariana Ringstrom":    ("Paramount+ / DTC", "Manager, Production Project Management, P+", "Scoping / vendor coordination", "Medium", "Named in Versus contact list", 85),
    "George Cheeks":       ("CBS", "Chair, TV Media", "Executive sponsor / likely DM", "High", "No route identified", None),
    "Michael Benson":      ("CBS", "President & CMO, TV Media", "Portfolio budget owner / confirmed commissioner", "High", "No direct warm evidence", 76),
    "Kelly Dunne":         ("Paramount Sports", "EVP, CBS Sports Marketing", "Sports budget owner / confirmed stakeholder", "High", "Campaign route; no warm evidence", 81),
    "Sabrina Caluori":     ("Nickelodeon", "Senior creative executive, Nickelodeon", "Prior Versus stakeholder / confirmed stakeholder", "Medium", "Public prior Versus collaboration", 86),
    "Tiyale Hayes":        ("BET", "EVP, Marketing & Audience Development", "Portfolio budget owner / confirmed commissioner", "High", "No direct warm evidence", 75),
    "Dario Spina":         ("MTV / Brand Studio", "CMO, Paramount Brand Studio", "Senior sponsor / likely DM", "Medium", "No direct warm evidence", 76),
    "Matthew Newcomb":     ("MTV / Brand Studio", "SVP, Integrated Marketing & Activation", "Brief owner / confirmed stakeholder", "High", "No direct warm evidence", 81),
    "Josh Goldstine":      ("Paramount Pictures", "President, Global Marketing & Distribution", "Executive budget owner / likely DM", "Medium", "No direct route", 69),
    "Josh Silverman":      ("Other", "President, Global Products & Experiences", "Executive sponsor / likely DM", "High", "No direct route", 67),
    "Jesse Sisgold":       ("Paramount Sports", "Leader, Paramount Sports Entertainment", "Emerging budget owner / likely DM", "Medium", "No direct route", 73),
    "Terry Minogue":       ("Paramount+ / DTC", "Paramount+ marketing leader (as credited)", "Named stakeholder from project evidence", "Medium", "Named in public project credits", None),
    "Rob Stecklow":        ("Paramount Sports", "Senior sports/news marketing stakeholder, P+", "Confirmed stakeholder", "Medium", "Named in public project credits", None),
    "Connie Orlando":      ("BET", "Internal executive producer, BET", "Confirmed stakeholder", "High", "Named in public project credits", None),
    # project-credit contacts not on the DM tab, added so edges resolve
    "Liza Burnett Fefferman": ("Paramount+ / DTC", "Awards/comms marketing (Yellowjackets FYC)", "Confirmed stakeholder", "Medium", "Public project credit", None),
    "Rene Ridinger":       ("Paramount+ / DTC", "Awards marketing (Yellowjackets FYC)", "Confirmed stakeholder", "Medium", "Public project credit", None),
    "Katherine Allen":     ("Paramount+ / DTC", "Awards marketing (Yellowjackets FYC)", "Confirmed stakeholder", "Medium", "Public project credit", None),
}

# ------------------------------------------------------------------ #
#  BUILD NODES + EDGES                                                #
# ------------------------------------------------------------------ #
nodes, links = [], []
def nid(kind, name): return f"{kind}::{name}"

# company
nodes.append({"id": nid("company", COMPANY), "label": COMPANY, "type": "company", "company": COMPANY})

# divisions
for d, color in DIVISIONS.items():
    nodes.append({"id": nid("division", d), "label": d, "type": "division", "company": COMPANY, "color": color})
    links.append({"source": nid("company", COMPANY), "target": nid("division", d), "rel": "hierarchy"})

# projects + edges to players and people
used_players, used_people = set(), set()
for name, div, tags, conf, contacts, players in PROJECTS:
    pid = nid("project", name)
    nodes.append({"id": pid, "label": name, "type": "project", "company": COMPANY,
                  "division": div, "tags": tags, "confidence": conf,
                  "color": DIVISIONS.get(div, "#8a8f9a")})
    links.append({"source": nid("division", div), "target": pid, "rel": "commissions"})
    for pl in players:
        used_players.add(pl)
        links.append({"source": pid, "target": nid("player", pl), "rel": "made-by"})
    for pc in contacts:
        used_people.add(pc)
        links.append({"source": pid, "target": nid("person", pc), "rel": "credited"})

# players (only those referenced) + worked-with edges to divisions
player_div = {}
for name, div, tags, conf, contacts, players in PROJECTS:
    for pl in players:
        player_div.setdefault(pl, set()).add(div)
for pl in sorted(used_players):
    meta = PLAYER_META.get(pl, ("Partner", False))
    nodes.append({"id": nid("player", pl), "label": pl, "type": "player", "company": COMPANY,
                  "ptype": meta[0], "repeat": meta[1],
                  "sig": SIGNATURE_COLORS.get(pl),
                  "divisions": sorted(player_div.get(pl, []))})
    for d in player_div.get(pl, []):
        links.append({"source": nid("player", pl), "target": nid("division", d), "rel": "worked-with"})

# people (referenced by projects OR on the DM tab) + belongs-to edges
all_people = set(PEOPLE.keys()) | used_people
for pn in sorted(all_people):
    div, title, role, conf, route, score = PEOPLE.get(pn, ("Other", "", "Confirmed stakeholder", "Medium", "", None))
    nodes.append({"id": nid("person", pn), "label": pn, "type": "person", "company": COMPANY,
                  "division": div, "title": title, "role": role, "confidence": conf,
                  "route": route, "score": score})
    if nid("division", div) in {n["id"] for n in nodes}:
        links.append({"source": nid("division", div), "target": nid("person", pn), "rel": "decision-maker"})
    else:  # enterprise-level exec: attach to company root
        links.append({"source": nid("company", COMPANY), "target": nid("person", pn), "rel": "decision-maker"})

DATA = {"company": COMPANY, "divisions": DIVISIONS, "nodes": nodes, "links": links}

with open("graph_data.json", "w") as f:
    json.dump(DATA, f, indent=1)

print(f"nodes={len(nodes)} links={len(links)}")
print("  divisions=", sum(1 for n in nodes if n['type']=='division'))
print("  projects =", sum(1 for n in nodes if n['type']=='project'))
print("  players  =", sum(1 for n in nodes if n['type']=='player'))
print("  people   =", sum(1 for n in nodes if n['type']=='person'))

# ------------------------------------------------------------------ #
#  EMIT RAW RECORDS (graph is built in JS so uploads can merge)      #
# ------------------------------------------------------------------ #
# enrich each project with IP / team / cost / sources / notes from the source CSV
import csv as _csv, re as _re
def _norm(s): return _re.sub(r'[^a-z0-9]+','',(s or '').lower())
ENRICH={}
try:
    with open("landscape_map.csv", newline='', encoding='utf-8') as _f:
        for _row in _csv.DictReader(_f):
            _nm=_norm(_row.get("Campaign Name",""))
            if not _nm: continue
            ENRICH[_nm]={
                "brand":(_row.get("Division / Brand") or "").strip(),
                "ip":(_row.get("IP / Franchise") or "").strip(),
                "team":(_row.get("Team / Dept") or "").strip(),
                "cost":(_row.get("Project Size / Cost") or "").strip(),
                "sources":[s.strip() for s in _re.split(r'[;,]', _row.get("Source(s)","")) if s.strip()],
                "notes":(_row.get("Notes") or "").strip(),
            }
except FileNotFoundError:
    print("WARN: landscape_map.csv not found; details will be sparse")
# alias map for names that differ slightly between curated list and CSV
_ALIAS={
    _norm("SpongeBob Movie: Search for SquarePants – intl social"): _norm("The SpongeBob Movie: Search for SquarePants - international social"),
    _norm("SpongeBob on the Sphere – Super Bowl LVIII"): _norm("SpongeBob SquarePants on the Sphere - Super Bowl LVIII"),
    _norm("SpongeBob Movie x Burger King"): _norm("The SpongeBob Movie x Burger King"),
    _norm("The Naked Gun – AV & digital campaign"): _norm("The Naked Gun - AV and digital campaign"),
    _norm("Tracker stays – AutoCamp & Hilton Honors"): _norm("Tracker-themed stays with AutoCamp and Hilton Honors"),
    _norm("2025 MTV VMAs – partner platform"): _norm("2025 MTV Video Music Awards - partner platform"),
}
def _enr(name):
    key=_norm(name)
    e=ENRICH.get(key) or ENRICH.get(_ALIAS.get(key,"")) or {}
    return e
_missed=[name for (name,*_ ) in PROJECTS if not _enr(name)]
if _missed: print("UNMATCHED (no enrichment):", len(_missed)); [print("   -",m) for m in _missed]

RAW = {
    "company": COMPANY,
    "divColors": DIVISIONS,
    "projects": [
        {**{"company": COMPANY, "division": div, "name": name,
            "tags": tags, "confidence": conf, "contacts": contacts, "players": players},
         **_enr(name)}
        for (name, div, tags, conf, contacts, players) in PROJECTS
    ],
    "playerMeta": {k: {"ptype": v[0], "repeat": v[1], "sig": SIGNATURE_COLORS.get(k)}
                   for k, v in PLAYER_META.items()},
    "people": {k: {"division": v[0], "title": v[1], "role": v[2],
                   "confidence": v[3], "route": v[4], "score": v[5]}
               for k, v in PEOPLE.items()},
}

with open("template.html") as f:
    HTML = f.read()
HTML = HTML.replace("__RAW__", json.dumps(RAW))
with open("index.html", "w") as f:
    f.write(HTML)
print("index.html bytes:", len(HTML))

# also drop a re-uploadable CSV template of the Paramount data
import csv
with open("landscape_template.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Client","Division Group","Campaign Name","Project Type","Confidence",
                "Key Contacts / Decision-Makers","Related Agencies / Vendors"])
    for (name, div, tags, conf, contacts, players) in PROJECTS:
        w.writerow([COMPANY, div, name, "; ".join(tags), conf,
                    "; ".join(contacts), "; ".join(players)])
print("wrote landscape_template.csv")
