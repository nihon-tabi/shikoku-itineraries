"""Fetch the Denso map code for every pin, keyed by coordinate.

Map codes are on this map even though all four options are car-free. A pin
outlives the itinerary it was built for: the traveller may rent a car for a
day, or need to give a driver something a Japanese nav will accept, and a
Japanese address often will not resolve.

The lookup itself lives in the japan-map-codes skill, which refuses to compute
a code and only ever quotes one. Results are cached so a rebuild is free.

    python -m src.fetch_mapcodes            # anything not cached
    python -m src.fetch_mapcodes --refresh  # all of it
"""
import importlib.util
import json
import os
import sys
import time

from .refs.geo import PLACES, _geo
from .refs.trails import TRAILHEADS

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "refs", "mapcodes.json")
SKILL = os.path.expanduser(
    "~/projects/japan-trip-planner/.claude/skills/japan-map-codes/scripts/mapcode.py")


def _lookup_fn():
    spec = importlib.util.spec_from_file_location("mapcode", SKILL)
    if spec is None or not os.path.exists(SKILL):
        sys.exit(f"japan-map-codes skill not found at {SKILL}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    refresh = "--refresh" in sys.argv
    mod = _lookup_fn()
    cache = {} if refresh else (json.load(open(CACHE)) if os.path.exists(CACHE) else {})

    # Prove the converter still behaves before trusting a run of new lookups.
    if mod.selftest() != 0:
        sys.exit("map code selftest FAILED — not fetching anything")

    geo = _geo()
    points = {}
    for _name, q in PLACES.items():
        g = geo.get(q)
        if g:
            points[f"{g['lat']:.6f},{g['lng']:.6f}"] = (g["lat"], g["lng"])
    for t in TRAILHEADS:
        lat, lon = [float(x) for x in t[2].split(",")]
        points[f"{lat:.6f},{lon:.6f}"] = (lat, lon)

    todo = [k for k in points if k not in cache]
    print(f"{len(points)} coordinates; {len(todo)} to fetch")
    missing = 0
    for i, k in enumerate(todo, 1):
        lat, lon = points[k]
        code = mod.lookup(lat, lon)
        if code:
            cache[k] = code
        else:
            missing += 1
        if i % 25 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)}")
            json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
        time.sleep(mod.THROTTLE)

    json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)
    print(f"cache holds {len(cache)} codes; {missing} coordinate(s) returned none")
    if missing:
        print('  those pins will read "not stated" — they are not guessed')


if __name__ == "__main__":
    main()
