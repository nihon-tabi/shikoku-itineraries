"""Fetch current address, phone, hours and website for every pinned place.

Google's Places *Details* endpoint is the only bulk source for a venue's phone
number, and it is the field the My Maps entry format needs that nothing else in
this repo carries. Hours from here are a CROSS-CHECK, not the citation: the
operator's own page still wins, because Google's hours go stale and say nothing
about seasonal closures or last-entry times.

Results are cached in src/refs/places_details.json so a rebuild costs nothing.

    python -m src.fetch_places            # fetch anything not cached
    python -m src.fetch_places --refresh  # re-fetch everything
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from .refs.geo import PLACES, _geo

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "refs", "places_details.json")
ENDPOINT = "https://maps.googleapis.com/maps/api/place/details/json"
FIELDS = ("name,formatted_address,formatted_phone_number,"
          "international_phone_number,opening_hours,website,url")
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def _key():
    k = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not k:
        sys.exit("GOOGLE_MAPS_API_KEY not set — "
                 "run:  set -a; . ~/.config/google-maps-mcp.env; set +a")
    return k


def fetch(place_id, key):
    url = f"{ENDPOINT}?{urllib.parse.urlencode({'place_id': place_id, 'fields': FIELDS, 'key': key})}"
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.loads(r.read().decode())
    if d.get("status") != "OK":
        return None, d.get("status")
    res = d["result"]
    oh = res.get("opening_hours") or {}
    return {
        "name": res.get("name"),
        "address": res.get("formatted_address"),
        "phone": res.get("international_phone_number"),
        "website": res.get("website"),
        "maps_url": res.get("url"),
        "hours": oh.get("weekday_text"),
        "periods": oh.get("periods"),
    }, "OK"


def main():
    refresh = "--refresh" in sys.argv
    key = _key()
    cache = {}
    if os.path.exists(CACHE) and not refresh:
        cache = json.load(open(CACHE))

    geo = _geo()
    wanted = {}
    for name, q in PLACES.items():
        g = geo.get(q)
        if g and g.get("place_id"):
            wanted[g["place_id"]] = name

    todo = [pid for pid in wanted if pid not in cache]
    print(f"{len(wanted)} places with a place_id; {len(todo)} to fetch")
    ok = fail = 0
    for i, pid in enumerate(todo, 1):
        rec, status = fetch(pid, key)
        if rec is None:
            print(f"  ! {wanted[pid]}: {status}", file=sys.stderr)
            fail += 1
        else:
            cache[pid] = rec
            ok += 1
        if i % 25 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)}")
            json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
        time.sleep(0.12)

    json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
    have_phone = sum(1 for v in cache.values() if v.get("phone"))
    print(f"fetched ok={ok} failed={fail}; cache holds {len(cache)}")
    print(f"  with a phone number: {have_phone}/{len(cache)}")
    print(f"  with hours:          {sum(1 for v in cache.values() if v.get('hours'))}/{len(cache)}")


if __name__ == "__main__":
    main()
