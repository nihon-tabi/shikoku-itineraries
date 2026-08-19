"""Sanity-check every trailhead coordinate against terrain and its own note.

A trailhead is the one figure in a walk record that cannot be eyeballed: the
numbers all look reasonable whether the pin is at the bottom of a path or the
top. Two real defects were shipped before this existed —

  * "Ōboke station lookout loop", whose note says it starts at the station
    forecourt, was pinned 2.5 km away and 700 m higher, on a ridge.
  * "Kankakei — walking DOWN" was pinned at the point where the walk ENDS,
    so the traveller would have been sent to the bottom of a descent.

Elevation comes from GSI, Japan's national mapping agency, which is free and
authoritative for Japanese terrain (Google's Elevation API is not enabled).

    python -m src.check_trailheads
"""
import json
import re
import sys
import time
import urllib.request

from .refs.trails import TRAILHEADS

GSI = ("https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php"
       "?lon={lon}&lat={lat}&outtype=JSON")

# Phrases in a record's own note that assert where the walk STARTS or ENDS.
STARTS_AT = re.compile(r"[Ss]tarts? at ([^.,;]+)")
DESCENT = re.compile(r"(\d+)\s*m\s*descent")


def elevation(lat, lon):
    try:
        d = json.loads(urllib.request.urlopen(
            GSI.format(lat=lat, lon=lon), timeout=20).read())
        e = d.get("elevation")
        return float(e) if e not in (None, "-----") else None
    except Exception:
        return None


def main():
    problems = []
    print(f"{'walk':50} {'elev':>8}  note")
    for t in TRAILHEADS:
        name, note = t[0], t[8] or ""
        lat, lon = [float(x) for x in t[2].split(",")]
        elev = elevation(lat, lon)
        flags = []

        # A record that says where it starts must be pinned there.
        m = STARTS_AT.search(note)
        if m:
            flags.append(f"note says it starts at: {m.group(1).strip()[:44]}")

        # A stated descent must fit between this point and somewhere lower.
        # If the record describes walking DOWN, the pin should be the HIGH end.
        d = DESCENT.search(t[5] or "")
        if d and elev is not None:
            drop = float(d.group(1))
            if "down" in (name + note).lower() and elev < drop:
                flags.append(f"describes a {drop:.0f} m descent but sits at {elev:.0f} m")

        print(f"{name[:48]:50} {('%.0f m' % elev) if elev else '     ?':>8}  "
              f"{'; '.join(flags) if flags else ''}")
        if flags:
            problems.append((name, flags))
        time.sleep(0.3)

    print()
    if problems:
        print(f"{len(problems)} walk(s) need a human to confirm the pin is the START:")
        for n, f in problems:
            print(f"  {n}\n     {'; '.join(f)}")
        print("\nThis check cannot prove a pin is right — it can only surface the ones\n"
              "whose own description disagrees with where they sit. Read each one.")
    else:
        print("no walk contradicts its own description")
    return 0


if __name__ == "__main__":
    sys.exit(main())
