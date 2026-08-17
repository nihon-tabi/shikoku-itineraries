"""Export the trip's SIGHTS as KML + CSV for Google My Maps.

Google My Maps has no public write API — the Maps Platform APIs cover geocoding,
places and routing, but creating or editing a My Maps layer is not exposed, and
neither is it available through the Maps MCP server. So this does the next best
thing: emits files My Maps imports directly (Create new map → Import layer).

Stations, ports, bus stops and beds are deliberately excluded — the traveller
asked for the places worth going to, not the plumbing.

Run from the project root:  python -m src.build_map
"""
import csv, os, re, html

from .refs import PLACES, DWELL, ATTRACTIONS, TRAILHEADS
from .refs.geo import _geo
from .refs.blurbs import BLURBS
from .itineraries import OPTIONS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")

TRANSIT = re.compile(r"駅|港|バス停|ターミナル|バスストップ|乗り場|渡船|"
                     r"Station|Stn|Port|Terminal|shuttle stop|Bus Centre|Ground")
LODGING = re.compile(r"ホテル|旅館|ゲストハウス|ホステル|民宿|Hostel|Hotel|Ryokan|"
                     r"Guest ?[Hh]ouse|WeBase|4S STAY|WAKKA|I-Link|PAQ|Casablanca|"
                     r"NEST|ぽんぽこ|Yadocurly|Anago no Nedoko|Evergreen|J-Hoppers|"
                     r"Trophy House|Shiokaze")
# Named individually because the regexes cannot know these are transfer points
# rather than destinations.
DROP = {"Mukaishima", "Sunrise Itoyama", "Innoshima Ōhashi", "Minokoshi",
        "Kouuntei", "Ariake Ground", "Kotohiki Park", "Shimanami Kaido",
        "Marukin", "Ochiai village", "Sumoto", "Ryōzen-ji",
        "lower shrine",   # the Takaya trailhead — the shrine itself is already a pin
        "Yasuda",         # a village; Yamaroku and Nakabu-an are the reasons to go
        "Ōshima"}         # an island you ride through, not a destination
# Alias -> the name to keep, so one pin does not appear twice.
ALIAS = {"Ritsurin": "Ritsurin Garden", "Kazurabashi": "Iya Kazurabashi",
         "Gate in the Sky": "Takaya Shrine", "Itsukushima": "Itsukushima Shrine",
         "Honmura": "Art House Project, Honmura", "Momijidani": "Momijidani, Miyajima",
         "Makino": "Makino Botanical Garden", "Kankakei": "Kankakei Gorge",
         "Peace Memorial": "Peace Memorial Museum", "Ninomaru": "Ninomaru Garden",
         "Mt Misen": "Mt Misen", "Shishiiwa": "Mt Misen ropeway top"}

def sights():
    """[(name, lat, lng, description, kind)] — sights AND vetted trailheads.

    Descriptions are written to stand ALONE in Google Maps, with no itinerary
    around them: what the place is, then price/hours/dwell where published. No
    dates, no "on day 4" — a pin has to be useful to someone who never saw the
    plan.
    """
    geo = _geo()
    dwell = {d[0].lower(): d[1] for d in DWELL}
    price = {a[0].lower(): (a[2], a[3]) for a in ATTRACTIONS}
    seen, out = set(), []

    for name, q in PLACES.items():
        if name in DROP or TRANSIT.search(name + q) or LODGING.search(name + q):
            continue
        g = geo.get(q)
        if not g:
            continue
        key = (round(g["lat"], 5), round(g["lng"], 5))
        if key in seen:
            continue
        seen.add(key)
        label = ALIAS.get(name, name)
        bits = [BLURBS.get(label, "")]
        for k, v in dwell.items():
            if label.lower() in k or k.split("(")[0].strip() in label.lower():
                bits.append(f"People spend about {v}.")
                break
        for k, (pr, h) in price.items():
            if label.lower() in k or k.split("(")[0].strip()[:14] in label.lower():
                bits.append(f"{pr} · {h}")
                break
        out.append((label, g["lat"], g["lng"],
                    " ".join(b for b in bits if b), "sight"))

    # Trailheads: the START of each walk, with the GPS apps that cover it. These
    # are the pins that matter most on the ground — a trailhead is exactly the
    # thing that is hard to find and easy to get wrong.
    for tname, region, ll, yamap, alltrails, dist, time, verdict, note, _src in TRAILHEADS:
        lat, lng = (float(x) for x in ll.split(","))
        apps = []
        if alltrails:
            apps.append(f"AllTrails: {alltrails}")
        else:
            apps.append("AllTrails: no matching route.")
        if yamap:
            apps.append(f"YAMAP: {yamap}")
        desc = (f"TRAILHEAD — the walk STARTS here. {dist}, about {time}. {verdict}. "
                f"{note} " + "  ".join(apps))
        out.append((f"⛰ {tname}", lat, lng, desc, "trailhead"))

    return sorted(out, key=lambda t: (t[4] != "sight", t[0]))

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = sights()
    kml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
           '<name>Shikoku &amp; Setouchi — places worth going to</name>',
           '<description>Two layers: places worth going to, and the trailheads where walks start. Stations, ports and hotels are deliberately excluded. Every pin reads on its own.</description>']
    for kind, folder in (("sight", "Places worth going to"),
                         ("trailhead", "Trailheads — where each walk starts")):
        kml.append(f"<Folder><name>{folder}</name>")
        for n, lat, lng, note, k in rows:
            if k != kind:
                continue
            kml.append("<Placemark><name>%s</name><description>%s</description>"
                       "<Point><coordinates>%s,%s,0</coordinates></Point></Placemark>"
                       % (html.escape(n), html.escape(note), lng, lat))
        kml.append("</Folder>")
    kml.append("</Document></kml>")
    with open(os.path.join(OUT, "shikoku-sights.kml"), "w", encoding="utf-8") as f:
        f.write("\n".join(kml))
    with open(os.path.join(OUT, "shikoku-sights.csv"), "w", encoding="utf-8-sig",
              newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["Name", "Latitude", "Longitude", "Notes", "Layer"])
        w.writerows(rows)
    ns = sum(1 for r in rows if r[4] == "sight")
    print(f"{ns} sights + {len(rows)-ns} trailheads "
          f"-> out/shikoku-sights.kml and .csv")

if __name__ == "__main__":
    main()
