"""Splice a Shimanami variant into an option and re-date everything after it.

The dashboard toggle just swaps which pre-computed array it renders, so no date
arithmetic happens in the browser.
"""
import copy, datetime, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from .itineraries import OPTIONS, SHIMANAMI_VARIANTS

def _shimanami_index(days):
    for i, d in enumerate(days):
        if "Shimanami" in d["title"]:
            return i
    return None

def with_shimanami(opt, variant):
    """Return a copy of `opt` with its Shimanami day replaced by `variant`,
    and every following date pushed back by the days added."""
    o = copy.deepcopy(opt)
    i = _shimanami_index(o["days"])
    if i is None:
        return o
    new_days = copy.deepcopy(SHIMANAMI_VARIANTS[variant])
    start = datetime.date.fromisoformat(o["days"][i]["date"])
    for n, d in enumerate(new_days):
        d["date"] = (start + datetime.timedelta(days=n)).isoformat()
    shift = len(new_days) - 1
    tail = o["days"][i + 1:]
    for d in tail:
        d["date"] = (datetime.date.fromisoformat(d["date"])
                     + datetime.timedelta(days=shift)).isoformat()
    o["days"] = o["days"][:i] + new_days + tail
    o["shimanami"] = variant
    return o

def all_variants(opt):
    return {v: with_shimanami(opt, v) for v in SHIMANAMI_VARIANTS}

if __name__ == "__main__":
    for k, opt in OPTIONS.items():
        i = _shimanami_index(opt["days"])
        print(f"Option {k}: Shimanami day at index {i} ({opt['days'][i]['date'] if i is not None else '—'})")
        for v, o in all_variants(opt).items():
            last = o["days"][-1]
            print(f"   {v:5s} -> {len(o['days'])} days, ends {last['date']} "
                  f"(¥{sum(l[5] for d in o['days'] for l in d['legs'] if l[5] is not None):,})")
