"""Resolve every PLACES entry to lat/lng + place_id via the Geocoding API.

A name-only Maps URL is ambiguous: Google resolves it, but the app can drop the
result into whatever mode it was last in (which is how you end up staring at a
directions form with the same place twice). A coordinate + place_id URL always
opens the place card.

Results cache to src/refs/places_geo.json so this only costs API calls once.

Run from the project root:  python -m src.geocode
"""
import json, os, sys, time, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from .refs import PLACES, TRAILHEADS, MAPS

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "refs", "places_geo.json")   # lives beside geo.py, which reads it

def key():
    p = os.path.expanduser("~/.config/google-maps-mcp.env")
    for line in open(p):
        if line.startswith("GOOGLE_MAPS_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no API key")

def geocode(q, k):
    url = ("https://maps.googleapis.com/maps/api/geocode/json?"
           + urllib.parse.urlencode({"address": q, "key": k, "language": "en", "region": "jp"}))
    with urllib.request.urlopen(url, timeout=20) as r:
        d = json.load(r)
    if d.get("status") != "OK" or not d.get("results"):
        return None
    top = d["results"][0]
    loc = top["geometry"]["location"]
    return {"lat": round(loc["lat"], 6), "lng": round(loc["lng"], 6),
            "place_id": top.get("place_id"), "formatted": top.get("formatted_address")}

def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    k = key()
    # key on the QUERY STRING, not the display name — the same place can appear
    # under two different queries (PLACES vs a hand-added MAPS pin) and both need
    # resolving or one of them silently falls back to a name search.
    wanted = {q: n for n, q in PLACES.items()}
    for pins in MAPS.values():
        for n, q in pins:
            wanted.setdefault(q, n)
    todo = [(n, q) for q, n in wanted.items() if q not in cache]
    print(f"{len(cache)} cached, {len(todo)} to resolve")
    ok = fail = 0
    for n, q in todo:
        r = geocode(q, k)
        if r:
            cache[q] = r; ok += 1
            print(f"  OK   {n:32s} {r['lat']},{r['lng']}  {r['formatted'][:52]}")
        else:
            cache[q] = None; fail += 1
            print(f"  MISS {n:32s} (will fall back to a name search)")
        time.sleep(0.05)
    json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1, sort_keys=True)
    print(f"\nresolved {ok}, failed {fail}, cache now {len(cache)} entries -> places_geo.json")

if __name__ == "__main__":
    main()
