# Shikoku itineraries — October 2026

Three costed, sourced itineraries for two backpackers crossing Shikoku car-free,
on local trains, between Osaka and Kyushu.

    ... → Osaka (leave 9 Oct 2026) → [ SHIKOKU ] → Ōkunoshima (rabbit island)
        → Hiroshima → Miyajima → Kyushu

| | |
|---|---|
| **A** | Himeji → Shodoshima → down through Shikoku. 16 days. Cleanest logistics, catches Kōchi's Sunday market. |
| **B** | Awaji Island → the Naruto whirlpools → Shikoku. 17 days. Buys the whirlpools; hangs on a four-a-day bus and a tide table. |
| **C** | One week, two bases, barely any packing. 11 days. Cheapest and least tiring; never sees inland or southern Shikoku. |

Options A and B include the Shimanami Kaido, which can be taken four ways
(no cycling / bus / 2 days riding / 3 days riding) — a toggle in the dashboard
and a separate workbook.

## Constraints these are built against

- No rental car. No limited-express (tokkyu) surcharges except where noted.
- Backpacker budget. Roughly 1–2 weeks in Shikoku; no hard limit.
- **Not big hikers** — short, scenic, transport-supported walks only.
- Every walk carries an exact trailhead lat/lng plus YAMAP and AllTrails routes,
  so a phone can track position offline.
- Every price is **per person** unless it says per bag, and carries a source.

## Build

```sh
make setup     # create .venv, install openpyxl
make           # rebuild everything into out/
```

Nothing in `out/` is edited by hand — it is regenerated from `src/`.

## Layout

```
src/                  the single source of truth
  itineraries.py        the three options, day by day, plus glossary,
                        foliage table and the Shimanami variants
  variants.py           splices a Shimanami variant in and shifts later dates
  refs/                 everything the itineraries are checked against
    sources.py            where each figure comes from, and how solid it is
    geo.py                place names -> Google Maps pins, inline linkification
    trails.py             trailhead GPS, YAMAP/AllTrails routes, difficulty
    costs.py              admission, hours, booking deadlines, dwell, currency
    places_geo.json       geocode cache (rebuild with `make geocode`)
  build_sheets.py       -> out/sheets/Shikoku-Option-{A,B,C}.xlsx + CSVs
  build_shimanami.py    -> out/sheets/Shimanami-Kaido.xlsx
  build_dashboard.py    -> out/dashboard.html, out/dashboard-standalone.html
  geocode.py            resolves new PLACES entries (costs API calls)

out/                  generated deliverables — safe to delete, never edited
  shikoku-sights.kml    the sights as a Google My Maps import (see below)
  shikoku-sights.csv    the same, if you prefer CSV
research/             the sourced findings, with an index and the sourcing rules
docs/tooling.md       what the Google Maps connector can and cannot do here
archive/              the superseded hand-written draft
```

`dashboard.html` is the artifact body (no document shell — it gets wrapped on
publish). `dashboard-standalone.html` is the same page with a full HTML shell
and a viewport meta tag, for opening straight off a phone.

## Putting the sights on your own Google map

Google My Maps has **no public write API** — the Maps Platform covers geocoding, places
and routing, but creating or editing a My Maps layer is not exposed, so no tool can add
these pins to your account for you. Import instead, which takes about a minute:

1. Open <https://mymaps.google.com> → **Create a new map** (or open an existing one).
2. **Import** under the layer name → upload `out/shikoku-sights.kml`.
3. KML carries the names and notes, so the pins arrive titled and described. If you use
   the CSV instead, pick `Latitude`/`Longitude` for position and `Name` for the title.

56 pins: sights only. Stations, ports, bus stops and beds are deliberately excluded —
they are in the workbooks, where they belong. Rebuild with `make map`.

## Two rules that keep this honest

**One source of truth.** The workbooks, the CSVs and the dashboard are all
generated from `src/`. They drifted apart once, when the itineraries were
hand-written in three places; they cannot now.

**Never estimate.** No travel time or price is inferred. If a figure is not
published, the deliverables say "not stated" and name who to ring. Sources are
tiered — operator > official > third-party > traveller — and the tier is shown
next to the figure so you can weigh it yourself.
