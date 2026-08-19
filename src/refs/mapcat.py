"""Folder and icon for every pin on the My Maps export.

Colour is the category, glyph is the subtype — that split is what lets a reader
scan a hundred pins. So each folder holds ONE colour, and variety comes from
the glyph. Catalogue and rationale: the `japan-my-maps` skill.

Assigned by hand rather than by regex. A regex would put "Mt Misen ropeway top"
and "Mt Misen" in the same bucket and call Ōkunoshima a mountain; the whole
point of the categorisation is that a human decided what each place IS.
"""

# folder -> (order on the map, its one colour)
FOLDERS = {
    "Attractions":                  (1, "795548"),  # brown
    "Nature views & Hikes":         (2, "DB4436"),  # red — walks and trailheads live here
    "Shrines and Temples":          (3, "9C27B0"),  # purple
    "Food and Markets":             (4, "E65100"),  # deep orange
    "Accommodation":                (5, "AFB42B"),  # olive
    "Stations, Ports and Stops":    (6, "0288D1"),  # blue
}

# name -> (folder, glyph)   glyph numbers are from the catalogue in the skill
SIGHTS = {
    # --- Castles, gardens, museums, townscapes -------------------------------
    "Himeji Castle":              ("Attractions", "1598"),
    "Koko-en":                    ("Attractions", "1582"),
    "Ritsurin Garden":            ("Attractions", "1582"),
    "Olive Park":                 ("Attractions", "1582"),
    "Makino Botanical Garden":    ("Attractions", "1582"),
    "Ninomaru Garden":            ("Attractions", "1582"),
    "Awaji Yumebutai":            ("Attractions", "1582"),
    "Kōchi Castle":               ("Attractions", "1598"),
    "Matsuyama Castle":           ("Attractions", "1598"),
    "Ōzu":                        ("Attractions", "1598"),
    "Tamamo Park":                ("Attractions", "1598"),
    "Kanamaru-za":                ("Attractions", "1834"),
    "Awa Odori Kaikan":           ("Attractions", "1834"),
    "Ōtsuka Museum":              ("Attractions", "1834"),
    "Peace Memorial Museum":      ("Attractions", "1834"),
    "Shikoku Mura":               ("Attractions", "1834"),
    "Chichu Art Museum":          ("Attractions", "1834"),
    "Teshima Art Museum":         ("Attractions", "1834"),
    "Benesse House Museum":       ("Attractions", "1834"),
    "Lee Ufan Museum":            ("Attractions", "1834"),
    "Art House Project, Honmura": ("Attractions", "1834"),
    "A-Bomb Dome":                ("Attractions", "1599"),
    "Hill of Hope":               ("Attractions", "1599"),
    "Zenigata Sunae":             ("Attractions", "1599"),
    "Uchiko":                     ("Attractions", "1599"),
    "Takehara":                   ("Attractions", "1599"),
    "Nagoro":                     ("Attractions", "1599"),
    "Iya Kazurabashi":            ("Attractions", "1599"),
    "Oku-Iya double vine bridges": ("Attractions", "1599"),
    "Uzu-no-michi":               ("Attractions", "1892"),
    "Botchan Train":              ("Attractions", "1716"),
    "Dogo Onsen":                 ("Attractions", "1811"),
    "Asuka-no-Yu":                ("Attractions", "1811"),

    # --- Landscape ----------------------------------------------------------
    # The custom icons exist because nothing native marks a foliage spot or a
    # cape; see the skill's assets/icons/README.md.
    "Kankakei Gorge":             ("Nature views & Hikes", "custom:foliage-maple-cluster"),
    "Momijidani, Miyajima":       ("Nature views & Hikes", "custom:foliage-maple-cluster"),
    "Angel Road":                 ("Nature views & Hikes", "custom:cape-coastal"),
    "Katsurahama":                ("Nature views & Hikes", "custom:cape-coastal"),
    "Chichibugahama":             ("Nature views & Hikes", "custom:cape-coastal"),
    "Mt Tsurugi":                 ("Nature views & Hikes", "1596"),
    "Mt Misen":                   ("Nature views & Hikes", "1596"),
    "Mt Bizan":                   ("Nature views & Hikes", "1634"),
    "Yashima":                    ("Nature views & Hikes", "1634"),
    "Mt Misen ropeway top":       ("Nature views & Hikes", "1634"),
    "Biwa Falls":                 ("Nature views & Hikes", "1892"),
    "Naruto Park":                ("Nature views & Hikes", "1720"),
    "Ōkunoshima":                 ("Nature views & Hikes", "1766"),

    # --- Shrines and temples -------------------------------------------------
    "Konpira-san":                ("Shrines and Temples", "1677"),
    "Itsukushima Shrine":         ("Shrines and Temples", "1677"),
    "Izanagi Shrine":             ("Shrines and Temples", "1677"),
    "Takaya Shrine":              ("Shrines and Temples", "1677"),
    "Daishō-in":                  ("Shrines and Temples", "1706"),
    "Kōsanji":                    ("Shrines and Temples", "1706"),

    # The boat pier reads as transit to the name regex ("乗り場"), but the
    # cruise is a destination in its own right and carries its own fare, so it
    # is named here to override that.
    "Ōboke-kyō boat pier":        ("Attractions", "1681"),
    "gorge cruise":               ("Attractions", "1681"),

    # --- Food ---------------------------------------------------------------
    "Hirome Market":              ("Food and Markets", "1577"),
    "Sunday Market":              ("Food and Markets", "1578"),
    "Nakabu-an":                  ("Food and Markets", "1640"),
    "Yamaroku":                   ("Food and Markets", "1565"),  # soy sauce brewery
}

# Trailheads get the hiker glyphs, harder ones the poled hiker, so difficulty
# reads off the map before the entry is opened.
TRAIL_GLYPH = {
    "EASY STROLL": "1596",
    "MODERATE":    "1597",
    "STEEP":       "1597",
    "SKIP IT":     "1597",
}

# Transit subtypes — a port and a station are not the same problem to solve.
TRANSIT_GLYPH = [
    (("Port", "港", "渡船", "乗り場", "Ferry"), "1569"),
    (("Bus", "バス", "ターミナル", "Terminal", "Centre"), "1532"),
    (("Ropeway", "ロープウェイ", "chairlift", "Lift", "リフト"), "1634"),
]
TRANSIT_DEFAULT = "1716"  # train station


def transit_glyph(name, query):
    hay = f"{name} {query}"
    for needles, glyph in TRANSIT_GLYPH:
        if any(n in hay for n in needles):
            return glyph
    return TRANSIT_DEFAULT


# A costs row and a pin often have different names for the same thing, and
# fuzzy matching cannot bridge the gap safely -- "Miyajima ropeway" shares no
# word with "Mt Misen". Anything listed here is a row that WAS researched and
# would otherwise reach no pin, so the traveller would see a blank next to a
# figure that exists. Left-hand side is the costs row, right-hand the pin.
ROW_TO_PIN = {
    "Kankakei ropeway, return":                      "Kankakei Gorge",
    "Miyajima ropeway, return":                      "Mt Misen ropeway top",
    "Miyajima visitor tax":                          "Itsukushima Shrine",
    "Wonder Naruto whirlpool cruise":                "Naruto Park",
    "Art House Project, 5 houses":                   "Art House Project, Honmura",
    "Awa Odori — daytime show":                      "Awa Odori Kaikan",
    "Awa Odori — evening show (famous troupes)":     "Awa Odori Kaikan",
    "Awa Odori 3-in-1 set (museum + day show + ropeway)": "Awa Odori Kaikan",
    "Ninomaru historic garden":                      "Ninomaru Garden",
    "Hearts Shuttle — all-day hop-on-hop-off":       "Chichibugahama",
    "Takaya Shrine shuttle bus, return":             "Takaya Shrine",
    "Takaya Shrine — the shrine itself":             "Takaya Shrine",
    "Matsuyama ropeway / chair lift":                "Matsuyama Castle",
    "Matsuyama Castle keep":                         "Matsuyama Castle",
    "Naoshima — island bus":                         "Benesse House Museum",
    "Himeji Castle + Koko-en (combined)":            "Himeji Castle",
    "Yamaroku Soy Sauce":                            "Yamaroku",
    "Nakabu-an somen workshop":                      "Nakabu-an",
    "Ōkunoshima Poison Gas Museum":                  "Ōkunoshima",
    "Kōsanji + Hill of Hope":                        "Kōsanji",
    "Mt Tsurugi chairlift, return":                  "Mt Tsurugi",
    "Mt Bizan ropeway, return":                      "Mt Bizan",
    "Iya Kazurabashi vine bridge":                   "Iya Kazurabashi",
    "Uzu-no-michi glass walkway":                    "Uzu-no-michi",
    "Zenigata Sunae sand coin":                      "Zenigata Sunae",
    "Chichibugahama beach":                          "Chichibugahama",
    "Hiroshima Peace Memorial Museum":               "Peace Memorial Museum",
    "Ōtsuka Museum of Art":                          "Ōtsuka Museum",
    "Dogo Onsen Honkan — Kami-no-Yu, ground floor":  "Dogo Onsen",
    "Dogo Onsen Honkan — Tama-no-Yu, 2nd floor":     "Dogo Onsen",
    "Dogo Asuka-no-Yu — 1st floor bath":             "Asuka-no-Yu",
    "Kanamaru-za kabuki theatre":                    "Kanamaru-za",
    "Shikoku Mura open-air museum":                  "Shikoku Mura",
    "Tamamo Park (Takamatsu Castle)":                "Tamamo Park",
    "Yashima summit — museums and shuttle":          "Yashima",
    "Yashima Aquarium":                              "Yashima",
    # Dwell rows
    "Ōboke gorge cruise":                            "Ōboke-kyō boat pier",
    "Kankakei ropeway + summit":                     "Kankakei Gorge",
    "Iya Valley as a whole":                         "Iya Kazurabashi",
}


def icon_for(folder, glyph):
    """Compose the icon spec the map builder wants."""
    if glyph.startswith("custom:"):
        return glyph
    return f"{glyph}-{FOLDERS[folder][1]}"


# A trailhead, an open hillside or a free island has no telephone of its own.
# The entry format keeps the field anyway and names who to ring INSTEAD -- the
# body that actually controls access, which is what the traveller needs when
# the last bus is in doubt or the lift is not turning. A blank teaches nothing;
# "ring the chairlift operator" is actionable.
# Numbers verified via Google Places against the named operator, Aug 2026.
CONTACTS = {
    "Ōkunoshima":            ("+81 846-26-3036", "the Poison Gas Museum on the island"),
    "Mt Tsurugi":            ("+81 883-62-2772", "the Tsurugi chairlift at Minokoshi, which controls access"),
    "Yashima":               ("+81 87-841-9418", "Yashima-ji, the temple on the plateau"),
    "Oku-Iya double vine bridges": ("+81 883-88-2211", "Miyoshi City, Higashi-Iya branch office"),
    "Takaya Shrine":         ("+81 875-24-2150", "Kanonji City Tourism Association"),
    "Mt Misen":              ("+81 829-44-0316", "Miyajima Ropeway, which controls the ascent"),
    "Mt Misen ropeway top":  ("+81 829-44-0316", "Miyajima Ropeway"),
    "Art House Project, Honmura": ("+81 50-1794-1100", "Benesse Art Site Naoshima"),
    # The four walking routes, which are paths rather than places
    "Konpira-san — the stone stairway": ("+81 877-75-2121", "the shrine office"),
    "Takaya Shrine — the 270 steps from the lower shrine": (
        "+81 875-24-2150", "Kanonji City Tourism Association — they also run the shuttle"),
    "Kazurabashi → Biwa Falls → riverside path": (
        "+81 883-88-2211", "Miyoshi City, Higashi-Iya branch office"),
    "Ōboke station lookout loop": (
        "+81 883-84-1211", "Ōboke-kyō Mannaka, the boat operator at the pier"),
}
