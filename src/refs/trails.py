"""Walks: exact trailhead coordinates, GPS-app routes, and a blunt verdict.

Every entry carries the trailhead as lat/lng (the start is rarely obvious on the
ground), a YAMAP and/or AllTrails route so the phone can track position offline, and
an honest difficulty call for two people who are not keen hikers.
"""

# ── Walks: exact trailhead, GPS app route, and a blunt verdict ───────────────
# (name, where it is, trailhead lat/lng, YAMAP url|None, AllTrails url|None,
#  distance, time, verdict, notes, source key)
TRAILHEADS = [
 ("Mt Tsurugi — chairlift top to the summit", "Tokushima, Iya",
  "33.86047,134.0924", "https://yamap.com/model-courses/23874",
  "https://www.alltrails.com/trail/japan/tokushima/mt-tsurugi",
  "2.0 km return", "1 h 20 return (40 min up)", "EASY STROLL",
  "Trailhead is the Nishijima chairlift top station (1,750 m) — the lift does the "
  "climbing. Take the 尾根道 ridge trail up: the official site calls it the shortest AND "
  "best-maintained, with few hazards. Come down the 大剣道 past the shrine for an easy "
  "loop. ⚠️ The AllTrails page exists but could not be opened and has no figures — use YAMAP.",
  "nishiawa"),
 ("Mt Tsurugi — from Minokoshi on foot (if the lift is shut)", "Tokushima, Iya",
  "33.86705,134.0897", "https://yamap.com/model-courses/6927", None,
  "4.7 km return, 561 m", "3 h 06", "MODERATE",
  "Only needed outside lift season (mid-Apr to late Nov) or if it's closed for weather.",
  "yamap"),
 ("Mt Misen — ropeway top to the summit", "Miyajima, Hiroshima",
  "34.27946,132.32505", "https://yamap.com/model-courses/23987", None,
  "1.8 km return, 210 m", "1 h 08 return (~30 min each way)", "MODERATE",
  "⚠️ NOT a flat promenade: the path drops to a saddle then climbs, hence 210 m of gain on "
  "a 535 m hill, over rock steps. The Shishiiwa observatory at the top station is a "
  "perfectly good stopping point. ⚠️ AllTrails' 'Miyajima Ropeway – Daishoin Course' is "
  "NOT this walk — AllTrails rates it hard, 5.8 km, 510 m, 3–3.5 h. Downloading it by "
  "mistake would be genuinely dangerous.",
  "miyajima_toz"),
 ("Mt Misen — Momijidani, the easiest walk-up from sea level", "Miyajima, Hiroshima",
  "34.29527,132.32236", "https://yamap.com/model-courses/30462", None,
  "5.7 km, 567 m", "1.5–2 h one way", "SKIP IT",
  "Included only to correct a mistake: the Tourism Association names MOMIJIDANI, not "
  "Daishō-in, as 「一番初心者向き」 — the most beginner-friendly route. Daishō-in is stone "
  "steps almost the whole way. Local practice is Momijidani up, Daishō-in down.",
  "miyajima_toz"),
 ("Kankakei Gorge — the 表12景 front trail, walking DOWN", "Shodoshima, Kagawa",
  "34.51563,134.30084", "https://yamap.com/model-courses/93076",
  "https://www.alltrails.com/trail/japan/kagawa/kankakei",
  "2 km, ~317 m descent", "1 h up / ~50 min down", "MODERATE",
  "Ride the ropeway up, walk down. The operator calls this trail 「ゆるやか」 (gentle) and "
  "it is the ONLY one that finishes at Kouuntei station and its bus stop. ⚠️ The 裏8景 "
  "back trail dumps you ~1 km BELOW the bus stop on a road you must then climb. ⚠️ The "
  "path is paved with anti-slip grooves and is genuinely slippery under wet leaves.",
  "kankakei_trl"),
 ("Konpira-san — the stone stairway", "Kotohira, Kagawa",
  "34.18712,133.81844", "https://yamap.com/model-courses/33048", None,
  "785 steps to the main shrine; 1,368 to the inner", "~30 min one way to the main shrine",
  "MODERATE",
  "No route-finding risk at all — it's a shopping street and then a staircase. Steps 113 "
  "to the 大門 are the steepest bit. Stop at the 御本宮; the further 583 steps to the "
  "奥社 is where it becomes a hike. Free walking sticks from the shops at the base. "
  "⚠️ No AllTrails page exists for this — the only 'Konpira' result is a different shrine "
  "in Nagasaki.",
  "konpira_off"),
 ("Ōboke station lookout loop", "Tokushima, Iya",
  "33.87669,133.76722", None, None,
  "1.0 km return", "about 30 min including breaks", "EASY STROLL",
  "The genuinely easy one. Miyoshi City's own walking map grades it 初級 (beginner): "
  "station → 10 min → lookout over the Yoshino River and the gorge → 10 min → station. "
  "Starts at Ōboke station forecourt, where the vine-bridge bus also leaves. No GPS app "
  "needed for a 1 km out-and-back, and neither YAMAP nor AllTrails has it.",
  "oboke_teku"),
 ("Kazurabashi → Biwa Falls → riverside path", "Tokushima, Iya",
  "33.87509,133.83542", None, None,
  "~200 m each way", "15–20 min", "EASY STROLL",
  "Cross the vine bridge, 50 m left to the 40–50 m falls, another 50 m to a riverside "
  "promenade with stone steps down to the water. Neither app has it; none needed.",
  "oboke_teku"),
]


TRAILHEADS.append(
 ("Takaya Shrine — the 270 steps from the lower shrine", "Kan-onji, Kagawa",
  "34.15311,133.64887", "https://yamap.com/mountains/8797", None,
  "2.5 km return, 354 m of ascent", "2 h 00 return (about 50 min up)", "STEEP — take the bus",
  "Trailhead is the LOWER shrine (下宮) car park at 34.15311, 133.64887; the torii you have "
  "seen in photographs is the UPPER shrine (本宮) at 34.15864, 133.65308, on the 404 m summit "
  "of Inazumiyama. The route runs lower shrine → middle shrine → the Yurugi-iwa boulder → the "
  "270 stone steps → the gate. ⚠️ The '270 steps' figure is only the FINAL flight — the whole "
  "ascent is about 350 vertical metres in 1.2 km, and the city's own page asks for proper "
  "shoes. Given you are not keen hikers, take the shuttle bus and skip this. ⚠️ AllTrails has "
  "NO matching trail — it blocks automated access and nothing for Takaya or Inazumiyama "
  "surfaced. YAMAP does: the mountain page above carries six model courses, of which "
  "「稲積山 往復」 (2.5 km / 354 m / 02:00) is the one that matches.",
  "takaya_access"))


# Match key -> the substring that identifies the walk's place in a day's text.
# Derived from the walk name rather than hand-listed, then overridden where the
# name alone is ambiguous.
_WALK_KEYS = {
 "Mt Tsurugi — chairlift top to the summit": "Mt Tsurugi",
 "Mt Tsurugi — from Minokoshi on foot (if the lift is shut)": "Mt Tsurugi",
 "Mt Misen — ropeway top to the summit": "Mt Misen",
 "Mt Misen — Momijidani, the easiest walk-up from sea level": "Momijidani",
 "Kankakei Gorge — the 表12景 front trail, walking DOWN": "Kankakei",
 "Konpira-san — the stone stairway": "Konpira-san",
 "Ōboke station lookout loop": "Ōboke",
 "Kazurabashi → Biwa Falls → riverside path": "Kazurabashi",
 "Takaya Shrine — the 270 steps from the lower shrine": "Takaya Shrine",
}

def walks_for(day):
    """Indices into TRAILHEADS for walks that belong to this day.

    A day card that mentions a mountain should say where the walk starts — the
    trail table is useless if the reader has to know it exists and go looking.
    """
    blob = " ".join([day.get("title", ""), " ".join(day.get("do", [])),
                     day.get("travel", ""), " ".join(day.get("watch", "")),
                     " ".join(x for _, x in day.get("flow", []))]).lower()
    out = []
    for i, t in enumerate(TRAILHEADS):
        key = _WALK_KEYS.get(t[0])
        if key and key.lower() in blob:
            out.append(i)
    return out
