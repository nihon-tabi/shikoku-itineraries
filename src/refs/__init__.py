"""Everything the itineraries are checked against: sources, places, trails, costs.

Split by topic, but re-exported flat — `from .refs import gmap, SOURCES, ATTRACTIONS`
works exactly as it did when this was one file. The four modules are independent:
none of them imports another, so they can be read in any order.

    sources.py   where every price and time comes from, and how solid it is
    geo.py       place names -> Google Maps pins, and inline linkification
    trails.py    walks: trailhead GPS, YAMAP/AllTrails routes, difficulty verdicts
    costs.py     admission, hours, booking deadlines, dwell times, currency
"""

from .sources import SOURCES, MATCH, resolve
from .geo import (PLACES, MAPS, gmap, maps_for, places_in, day_places, linkify, pin, autolink)
from .trails import TRAILHEADS, walks_for
from .costs import (ADMISSIONS, ATTRACTIONS, BOOKINGS, DWELL, TIDES,
                    price_unit, PRICE_NOTE, PRICE_HEADLINE, PRICE_BODY,
                    JPY_ILS, JPY_ILS_ASOF, LIVE_FORMULA, RATE_HELP)

__all__ = [
    "SOURCES", "MATCH", "resolve",
    "PLACES", "MAPS", "gmap", "maps_for", "places_in", "day_places", "linkify", "pin", "autolink",
    "TRAILHEADS", "walks_for",
    "ADMISSIONS", "ATTRACTIONS", "BOOKINGS", "DWELL", "TIDES",
    "price_unit", "PRICE_NOTE", "PRICE_HEADLINE", "PRICE_BODY",
    "JPY_ILS", "JPY_ILS_ASOF", "LIVE_FORMULA", "RATE_HELP",
]
