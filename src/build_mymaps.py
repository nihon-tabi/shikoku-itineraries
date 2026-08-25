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

Every pin carries a Denso map code even though all four options are car-free:
a pin outlives the itinerary it was built for, and the code is what a rental
car's nav or a taxi driver can use when a Japanese address will not resolve.

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
MAPCODES = os.path.join(HERE, "refs", "mapcodes.json")

RULE = "_" * 40
EMOJI = {
    "Attractions": "🏯", "Nature views & Hikes": "🌿",
    "Shrines and Temples": "⛩️", "Food and Markets": "🍜",
    "Accommodation": "🛏️", "Stations, Ports and Stops": "🚉",
}


def _details():
    return json.load(open(DETAILS)) if os.path.exists(DETAILS) else {}


def _mapcodes():
    """lat,lon -> Denso map code, from src.fetch_mapcodes.

    Present even though every option is car-free: a pin outlives the itinerary
    it was built for, and the code is what a rental car's nav or a taxi driver
    can actually use. Quoted from the converter, never computed."""
    return json.load(open(MAPCODES)) if os.path.exists(MAPCODES) else {}


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
        # An explicit mapping wins: it is the only way to connect rows and pins
        # that share no words, like "Miyajima ropeway" and "Mt Misen".
        pinned = mapcat.ROW_TO_PIN.get(r[key])
        if pinned is not None:
            if _norm(pinned) == want:
                hits.append(r)
            continue
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


def clean_url(u):
    """Drop the tracking parameters the Places API bolts on.

    A website comes back as ...?utm_source=google_maps&utm_medium=organic and a
    maps link as ...&g_mp=<base64>. Neither is meant for a human to read, and
    both make the entry look machine-generated."""
    if not u:
        return u
    for junk in ("?utm_source=", "&utm_source=", "?g_mp=", "&g_mp="):
        i = u.find(junk)
        if i != -1:
            u = u[:i]
    return u


def section(title, lines):
    body = "<br>".join(f"•\t{l}" for l in lines if l)
    return f"{RULE}<br>{title}<br>{body}" if body else ""


JA = re.compile(r"[぀-ヿ一-鿿][぀-ヿ一-鿿・ヶ]*")


def japanese_name(query):
    """Pull the Japanese name out of a geocoding query like '姫路城 Himeji Castle'.

    Worth carrying into the entry: it is what the traveller shows a station
    attendant or types into a Japanese site when the English name gets them
    nowhere.

    Take the FIRST Japanese run, not the longest. Queries are written name
    first, then disambiguators — '剣山 見ノ越 Mt Tsurugi' is the mountain
    followed by the pass you reach it from. Picking the longest run labelled
    Mt Tsurugi as 見ノ越, and Takaya Shrine as 天空の鳥居.
    """
    hits = JA.findall(query or "")
    first = hits[0] if hits else ""
    return first if len(first) > 1 else ""


def walks_from(label):
    """The walks that start at or near this place.

    A mountain's pin sits on the mountain, which is correct for what the place
    IS and useless for getting there — routing to a 1,955 m summit helps nobody.
    So a sight that has walks names them and gives their trailhead coordinates,
    and each walk also has its own pin. The reader should not have to know the
    walk pins exist to find them.
    """
    want = _norm(label)
    out = []
    for t in TRAILHEADS:
        base = _norm(t[0].split("—")[0].split("→")[0])
        if base and (base == want or want in base or base in want):
            out.append(t)
    return out


def describe(label, folder, det, trail=None, query="", mapcode=None, display=None):
    """Compose one entry in the house format."""
    parts = []
    # An explicit name wins over whatever the geocoding query happened to use.
    ja = mapcat.JA_NAMES.get(display or label, mapcat.JA_NAMES.get(label))
    if ja is None:
        ja = japanese_name(query)
    head = f"{EMOJI[folder]} {display or label}" + (f" ({ja})" if ja else "")
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
        # ALWAYS name what the figure is for. Collapsing a single row to the
        # word "Admission" turned a chairlift fare into the price of entering a
        # mountain, and a poison gas museum's ¥150 into the cost of a free
        # island. What a price buys is part of the price.
        ha.append(f"{name}: {price}")
        if hours and hours != "—":
            ha.append(f"Hours: {hours}")
        if closed and closed != "—":
            ha.append(f"Closing days / notes: {closed}")
    if det.get("website"):
        ha.append(f"Website: {clean_url(det['website'])}")
    parts.append(section("🕒 Hours & Admission", ha))

    # -- Trail detail
    if trail:
        _n, _region, _co, yamap, alltrails, dist, time_, verdict, note, _tag = trail
        parts.append(section("🛤️ Trail Overview", [
            f"{dist} · {time_}", f"Verdict: {verdict}", note]))
        parts.append(section("🔗 More Info & Reviews", [
            f"YAMAP: {yamap}" if yamap else "",
            f"AllTrails: {alltrails}" if alltrails else ""]))

    # -- Walks that start here, for a sight that is not itself a walk
    if not trail:
        w = walks_from(label)
        if w:
            parts.append(section("🥾 Walks from here", [
                f"{t[0]} — {t[5]}, {t[6]} · {t[7]} · trailhead {t[2]}" for t in w]))

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
    phone = det.get("phone")
    if not phone:
        alt = mapcat.CONTACTS.get(label)
        phone = f"{alt[0]} — {alt[1]}" if alt else "not stated"
    link = clean_url(det.get("maps_url") or "")
    foot = f"{RULE}<br>Phone number: {phone}"
    foot += f"<br>Map code: {mapcode or 'not stated'}"
    parts.append(foot)
    if link:
        parts.append(link)
    return "<br><br>".join(p for p in parts if p)


def build():
    geo, det_all, codes = _geo(), _details(), _mapcodes()
    folders, seen, unmapped = {}, set(), []
    # Deliberately NOT merging walks into sight pins. A mountain's pin belongs
    # on the mountain; a walk's pin belongs at the point you start walking, and
    # those are kilometres and hundreds of metres apart. Merging also collapsed
    # every route up one mountain into a single entry, so "Mt Tsurugi" silently
    # carried the Minokoshi trailhead while describing the chairlift route.
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

        # LODGING is tested BEFORE transit: "4S STAY 阿波池田駅前" contains 駅 and
        # was being filed as a station because of where it stands.
        if label in mapcat.SIGHTS:
            folder, glyph = mapcat.SIGHTS[label]
        elif LODGING.search(name + q):
            folder, glyph = "Accommodation", "1602"
        elif TRANSIT.search(name + q):
            folder, glyph = "Stations, Ports and Stops", mapcat.transit_glyph(name, q)
        else:
            unmapped.append(label)
            continue

        mc = codes.get(f"{g['lat']:.6f},{g['lng']:.6f}")
        folders.setdefault(folder, []).append({
            "name": mapcat.PIN_NAMES.get(label, label),
            "lat": g["lat"], "lon": g["lng"],
            "icon": mapcat.icon_for(folder, glyph),
            "description": describe(label, folder, det, None, q, mc,
                                    mapcat.PIN_NAMES.get(label, label)),
        })

    # Every walk gets its own pin, at its own trailhead. Two routes up the same
    # mountain are two pins, because they start in different places and one may
    # be worth doing while the other is not.
    for t in TRAILHEADS:
        lat, lon = [float(x) for x in t[2].split(",")]
        glyph = mapcat.TRAIL_GLYPH.get(t[7].split("—")[0].strip(), "1596")
        folders.setdefault("Nature views & Hikes", []).append({
            "name": t[0], "lat": lat, "lon": lon,
            "icon": mapcat.icon_for("Nature views & Hikes", glyph),
            "description": describe(t[0], "Nature views & Hikes", {}, t, t[1],
                                    codes.get(f"{lat:.6f},{lon:.6f}")),
        })

    # Guard against the geocoder resolving a place to one of its own parts.
    # "ホテル祖谷温泉" returned the hotel's OPEN-AIR BATH, 190 m downhill, because
    # the bath is separately listed and better rated than the hotel. Two tells:
    # a Plus Code address (the geocoder had no street address to give) and a
    # resolved name that reads like a sub-facility.
    PLUS = re.compile(r"\b[23456789CFGHJMPQRVWX]{4}\+[23456789CFGHJMPQRVWX]{2,}")
    PART = ("Open-air", "露天", "足湯", "Foot Bath", "Parking", "駐車", "Bus Stop",
            "Entrance", "入口", "Ticket", "売店", "Gift Shop")
    suspect = []
    for fname, places in folders.items():
        for pl in places:
            d = pl["description"]
            if PLUS.search(d):
                suspect.append((pl["name"], "Plus Code address — weak geocode"))
            for w in PART:
                if f"{w}" in d.split("____")[0]:
                    suspect.append((pl["name"], f"resolved name contains {w!r}"))
                    break
    if suspect:
        print(f"\n⚠ {len(suspect)} pin(s) may point at a sub-facility rather than the place:")
        for nm, why in suspect:
            print(f"   {nm}: {why}")

    # The third way a geocode goes wrong: it lands on an ADMINISTRATIVE CENTROID
    # rather than the place. "久保 バス停 三好市" resolved to "Miyoshi, Tokushima,
    # Japan" — the city centre, 30 km from the actual bus stop, and nothing about
    # the coordinate looked wrong. The tell is the formatted address itself: a
    # real place has a street, a block or a building number in it, so an address
    # that is only a city and a prefecture means the geocoder never found the
    # thing you asked for. Resolve those with a Places text search and pin the
    # result by hand.
    vague = []
    for query, rec in sorted(_geo().items()):
        addr = (rec.get("formatted") or "").strip()
        if "—" in addr:            # hand-set, with a note saying why
            continue
        if not re.search(r"\d", addr) and addr.count(",") <= 2:
            vague.append((query, addr))
    if vague:
        print(f"\n⚠ {len(vague)} geocode(s) resolved to an address with no street detail —")
        print("   likely an administrative centroid, not the place:")
        for q, a in vague:
            print(f"   {q}  ->  {a!r}")

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
