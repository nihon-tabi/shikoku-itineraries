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


def icon_for(folder, glyph):
    """Compose the icon spec the map builder wants."""
    if glyph.startswith("custom:"):
        return glyph
    return f"{glyph}-{FOLDERS[folder][1]}"
