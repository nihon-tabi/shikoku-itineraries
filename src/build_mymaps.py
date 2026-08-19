"""Generate the Google My Maps import file for the whole trip.

One map covering all four options, so the traveller has a single thing to open
regardless of which itinerary they end up on. Every pin's description is built
to stand ALONE — someone who has never seen the itinerary should be able to use
it — so there are no dates and no "on day 4".

Sources, in the order they are trusted:
  * operator-sourced prices, hours and closing days from refs.costs (the same
    figures the workbooks and dashboard quote, so nothing can drift)
  * refs.blurbs for what the place actually is
  * refs.trails for walks, with YAMAP/AllTrails
  * Google Places for address, phone and website ONLY -- its hours are a
    cross-check, never the citation, because they go stale and say nothing
    about seasonal closing or last entry.

Map codes are deliberately absent: every option is car-free. See the
`japan-map-codes` skill -- adding them where nobody drives dilutes the fields
that matter.

    python -m src.build_mymaps
"""
import json
import os
import re

from .refs.geo import PLACES, _geo
from .refs.blurbs import BLURBS
from .refs.trails import TRAILHEADS
from .refs.costs import ATTRACTIONS, DWELL, BOOKINGS, TIDES
from .refs import mapcat
from .build_map import TRANSIT, LODGING, DROP, ALIAS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
DETAILS = os.path.join(HERE, "refs", "places_details.json")

RULE = "_" * 40
EMOJI = {
    "Attractions": "🏯", "Nature views & Hikes": "🌿",
    "Shrines and Temples": "⛩️", "Food and Markets": "🍜",
    "Accommodation": "🛏️", "Stations, Ports and Stops": "🚉",
}


def _details():
    return json.load(open(DETAILS)) if os.path.exists(DETAILS) else {}


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _match(label, rows, key=0):
    """Find the costs rows for a place.

    Names differ between files -- the row may be 'Matsuyama Castle keep' for the
    place 'Matsuyama Castle' -- so this matches on whole-phrase containment, and
    returns ALL matches because a place can legitimately have several priced
    parts (a castle keep and its ropeway).

    Containment must be on a WORD BOUNDARY and the shared phrase must carry more
    than one word. An earlier version fell back to comparing first words, which
    made every 'Mt …' match every other: Mt Misen's pin carried Mt Tsurugi's
    chairlift fare. A wrong price that looks right is worse than none, so this
    errs toward matching nothing.
    """
    want = _norm(label)
    if not want:
        return []
    hits = []
    for r in rows:
        n = _norm(r[key])
        if not n:
            continue
        short, long_ = (want, n) if len(want) <= len(n) else (n, want)
        # A single shared word is only evidence if it is distinctive. "Yashima"
        # identifies a place; "mt" identifies three different mountains.
        if len(short.split()) < 2 and short != long_ and len(short) < 6:
            continue
        if re.search(rf"(?:^|\s){re.escape(short)}(?:\s|$)", long_):
            hits.append(r)
    return hits


def section(title, lines):
    body = "<br>".join(f"•\t{l}" for l in lines if l)
    return f"{RULE}<br>{title}<br>{body}" if body else ""


JA = re.compile(r"[぀-ヿ一-鿿][぀-ヿ一-鿿・ヶ]*")


def japanese_name(query):
    """Pull the Japanese name out of a geocoding query like '姫路城 Himeji Castle'.

    Worth carrying into the entry: it is what the traveller shows a station
    attendant or types into a Japanese site when the English name gets them
    nowhere."""
    hits = JA.findall(query or "")
    best = max(hits, key=len) if hits else ""
    return best if len(best) > 1 else ""


def describe(label, folder, det, trail=None, query=""):
    """Compose one entry in the house format."""
    parts = []
    ja = japanese_name(query)
    head = f"{EMOJI[folder]} {label}" + (f" ({ja})" if ja else "")
    blurb = BLURBS.get(label, "")
    parts.append(head + (f"<br>{blurb}" if blurb else ""))

    # -- Location & Access
    access = []
    if det.get("address"):
        access.append(f"Address: {det['address']}")
    if trail:
        access.append(f"Trailhead: {trail[2]}")
    parts.append(section("📍 Location & Access", access))

    # -- Hours & Admission, from the operator-sourced rows
    rows = _match(label, ATTRACTIONS)
    ha = []
    for r in rows:
        name, _area, price, hours, closed = r[0], r[1], r[2], r[3], r[4]
        bit = name if len(rows) > 1 else "Admission"
        ha.append(f"{bit}: {price}")
        if hours and hours != "—":
            ha.append(f"Hours: {hours}")
        if closed and closed != "—":
            ha.append(f"Closing days / notes: {closed}")
    if det.get("website"):
        ha.append(f"Website: {det['website']}")
    parts.append(section("🕒 Hours & Admission", ha))

    # -- Trail detail
    if trail:
        _n, _region, _co, yamap, alltrails, dist, time_, verdict, note, _tag = trail
        parts.append(section("🛤️ Trail Overview", [
            f"{dist} · {time_}", f"Verdict: {verdict}", note]))
        parts.append(section("🔗 More Info & Reviews", [
            f"YAMAP: {yamap}" if yamap else "",
            f"AllTrails: {alltrails}" if alltrails else ""]))

    # -- How long people spend
    dw = _match(label, DWELL)
    if dw:
        parts.append(section("⏳ How Much Time to Budget?",
                             [f"{d[1]} — {d[3]}" for d in dw[:1]]))

    # -- Booking, and tide, where they gate the visit
    bk = _match(label, BOOKINGS)
    if bk:
        parts.append(section("⚠️ Booking", [f"{b[1]}. {b[2]}" for b in bk[:1]]))
    td = _match(label, TIDES)
    if td:
        parts.append(section("🌊 Tides", [t[2] for t in td[:1]]))

    # -- The invariant footer
    phone = det.get("phone") or "not stated"
    link = det.get("maps_url") or ""
    foot = f"{RULE}<br>Phone number: {phone}"
    parts.append(foot)
    if link:
        parts.append(link)
    return "<br><br>".join(p for p in parts if p)


def build():
    geo, det_all = _geo(), _details()
    trail_by_key = {}
    for t in TRAILHEADS:
        trail_by_key[_norm(t[0].split("—")[0])] = t

    folders, seen, unmapped = {}, set(), []
    for name, q in PLACES.items():
        g = geo.get(q)
        if not g or name in DROP:
            continue
        key = (round(g["lat"], 5), round(g["lng"], 5))
        if key in seen:
            continue
        seen.add(key)
        label = ALIAS.get(name, name)
        det = det_all.get(g.get("place_id"), {})

        if label in mapcat.SIGHTS:
            folder, glyph = mapcat.SIGHTS[label]
        elif TRANSIT.search(name + q):
            folder, glyph = "Stations, Ports and Stops", mapcat.transit_glyph(name, q)
        elif LODGING.search(name + q):
            folder, glyph = "Accommodation", "1602"
        else:
            unmapped.append(label)
            continue

        trail = trail_by_key.get(_norm(label))
        folders.setdefault(folder, []).append({
            "name": label, "lat": g["lat"], "lon": g["lng"],
            "icon": mapcat.icon_for(folder, glyph),
            "description": describe(label, folder, det, trail, q),
        })

    # Trailheads that are not already a sight pin get their own entry, in the
    # nature folder -- the traveller asked for them merged, not separate.
    for t in TRAILHEADS:
        base = _norm(t[0].split("—")[0])
        if any(_norm(p["name"]) == base for p in folders.get("Nature views & Hikes", [])):
            continue
        lat, lon = [float(x) for x in t[2].split(",")]
        glyph = mapcat.TRAIL_GLYPH.get(t[7].split("—")[0].strip(), "1596")
        folders.setdefault("Nature views & Hikes", []).append({
            "name": t[0], "lat": lat, "lon": lon,
            "icon": mapcat.icon_for("Nature views & Hikes", glyph),
            "description": describe(t[0], "Nature views & Hikes", {}, t, t[1]),
        })

    spec = {
        "name": "Shikoku, Setouchi and Hiroshima — October 2026",
        "description": ("Every place across all four itinerary options. Prices are "
                        "PER PERSON. Figures are quoted from the operator that "
                        "charges them; anything unpublished says so."),
        "folders": [{"name": f, "places": sorted(folders[f], key=lambda p: p["name"])}
                    for f in sorted(folders, key=lambda f: mapcat.FOLDERS[f][0])],
    }
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, "shikoku-mymaps.json")
    json.dump(spec, open(dest, "w"), ensure_ascii=False, indent=1)

    total = sum(len(f["places"]) for f in spec["folders"])
    print(f"{total} pins in {len(spec['folders'])} folders -> {dest}")
    for f in spec["folders"]:
        print(f"   {f['name']:30} {len(f['places']):3}")
    if unmapped:
        print(f"\n{len(unmapped)} place(s) with no category — add to mapcat.SIGHTS:")
        for u in unmapped:
            print(f"   {u}")
    return spec


if __name__ == "__main__":
    build()
