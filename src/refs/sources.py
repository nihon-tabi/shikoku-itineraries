"""Where every fact comes from.

SOURCES maps a short key to (label, url, tier). Tier is how much the figure can be
trusted: operator > official > third-party > traveller. MATCH maps a fragment of a
leg's "how you travel" text to the source key that justifies its price.
"""

SOURCES = {
 "jr_shinkaisoku": ("Kansai-norikae — Shin-Kaisoku needs no surcharge", "https://kansai-norikae.com/shinkaisoku/", "third-party"),
 "ekitan_osa_him": ("Ekitan fare table, Osaka–Himeji", "https://ekitan.com/transit/fare/sf-5006/st-5884", "third-party"),
 "himeji_price":   ("Himeji City — 2026 admission revision", "https://www.city.himeji.lg.jp/shisei/0000032640.html", "official"),
 "himeji_en":      ("Visit Himeji — revision of castle admission fees", "https://visit-himeji.com/en/news/revision-of-himeji-castle-admission-fees/", "official"),
 "himeji_castle":  ("Himeji Castle official site", "https://www.himejicastle.jp/en/", "official"),
 "himeji_lockers": ("REAL HIMEJI — station coin lockers", "https://realtrip-himeji.com/usefulinformation/156908/", "third-party"),
 "shinki94":       ("Visit Himeji — Shinki Bus route 94 to the port", "https://visit-himeji.com/en/travel-info/ie-island-island-fun-ticket/", "official"),
 "shinki_fare":    ("NAVITIME / Jorudan route data (no operator page states it)", "https://navi.shinkibus.jp/snk/", "third-party"),
 "sf_himeji":      ("Shikoku Ferry — Himeji–Fukuda route page", "https://www.shikokuferry.com/route1", "operator"),
 "sf_takamatsu":   ("Shikoku Ferry — Tonoshō–Takamatsu route page", "https://www.shikokuferry.com/route2", "operator"),
 "sf_angel":       ("Shikoku Ferry — Angel Road tide table", "https://www.shikokuferry.com/angel", "operator"),
 "olive_bus":      ("Shodoshima Olive Bus — fares and passes", "https://www.shodoshima-olive-bus.com/ticket/", "operator"),
 "olive_routes":   ("Shodoshima Olive Bus — route index", "https://www.shodoshima-olive-bus.com/dia/", "operator"),
 "kankakei_rw":    ("Kankakei Ropeway — official fares", "https://www.kankakei.co.jp/ropeway/", "operator"),
 "kankakei_shut":  ("Shodoshima Town — free Kankakei shuttle", "https://www.town.shodoshima.lg.jp/gyousei/kakuka/kikakuzaisei/1/rosenbasu/8893.html", "official"),
 "kankakei_koyo":  ("Kankakei — dated autumn-colour reports", "https://kankakei.co.jp/pickup/koyo.html", "operator"),
 "marukin":        ("Marukin Soy Sauce Memorial Museum", "https://marukin.moritakk.com/kinenkan/", "operator"),
 "yamaroku":       ("Yamaroku Soy Sauce — access", "https://yama-roku.net/en/access", "operator"),
 "kotoku_exp":     ("Yonkou Bus — Takamatsu–Tokushima Kōtoku Express", "https://www.yonkou-bus.co.jp/line/tokushima.html", "operator"),
 "jr_oboke":       ("JR Shikoku — Ōboke station departure board (PDF)", "https://www.jr-shikoku.co.jp/01_trainbus/jikoku/pdf/oboke.pdf", "operator"),
 "jr_awaikeda":    ("JR Shikoku — Awa-Ikeda departure board (PDF)", "https://www.jr-shikoku.co.jp/01_trainbus/jikoku/pdf/awa-ikeda.pdf", "operator"),
 "yahoo_transit":  ("Yahoo! Transit, limited-express excluded", "https://transit.yahoo.co.jp/", "third-party"),
 "jg_oboke":       ("japan-guide — Iya Valley access and fares", "https://www.japan-guide.com/e/e7826.html", "third-party"),
 "jg_iya_bus":     ("japan-guide — Ōboke–Kazurabashi bus", "https://www.japan-guide.com/e/e7828.html", "third-party"),
 "yonkoh_time":    ("Shikoku Kotsu — Iya line timetable (PDF, rev. 1 Oct 2025)", "https://yonkoh.co.jp/wp/wp-content/uploads/2025/09/tozai_iya_timetable2025.pdf", "operator"),
 "miyoshi_en":     ("Miyoshi City — consolidated English bus timetable & fares", "https://miyoshi-tourism.jp/download/?file=bus_timetable_en", "official"),
 "miyoshi_tsurugi":("Miyoshi City — Mt Tsurugi / Oku-Iya bus calendar", "https://www.miyoshi.i-tokushima.jp/docs/4292.html", "official"),
 "oboke_boat":     ("Ōboke-kyō Mannaka — sightseeing boat", "https://mannaka.co.jp/sightseeingboat/", "operator"),
 "kazurabashi":    ("Miyoshi City Tourism — Iya Kazurabashi", "https://miyoshi-tourism.jp/en/spot/46/", "official"),
 "tsurugi_lift":   ("Mt Tsurugi sightseeing chairlift", "https://turugirift.com/", "operator"),
 "lostfilipina":   ("Lost Filipina — itemised 2020 trip, paid these fares", "https://www.lostfilipina.com/2021/03/the-shikoku-adventure.html", "traveller"),
 "yarina":         ("Yarina Shleyan — car-free 5-day Shikoku, logged fares", "https://www.facebook.com/100006253026373/posts/4098532907031770/", "traveller"),
 "nangoku":        ("JR Shikoku Bus — Nangoku Express, Kōchi–Matsuyama", "https://www.jr-shikokubus.co.jp/businfo/nangoku_ex/matsuyama.html", "operator"),
 "myyu":           ("Kōchi MY-YU bus pass", "https://kochi-tabi.jp/my-bus/", "official"),
 "myyu_half":      ("No Less Intrepid — paid ¥600 on a foreign passport", "https://no-less-intrepid.blogspot.com/2020/05/hello-shikoku-visit-kochi-hidden-gem-in.html", "traveller"),
 "tosaden":        ("Tosaden Kotsu — tram one-day pass", "https://www.tosaden.co.jp/train/oneday.php", "operator"),
 "naka1951":       ("naka1951 — Matsuyama trip log, Nov 2024", "https://naka1951.blogspot.com/2024/11/Matsuyama.html", "traveller"),
 "iyotetsu":       ("Iyotetsu — city tram", "https://www.iyotetsu.co.jp/", "operator"),
 "turkeydinner":   ("u/_TurkeyDinner_ — logged every fare on this exact leg", "https://www.reddit.com/r/JapanTravelTips/comments/1gs75qb/hiroshima_to_matsuyama_to_imabari_a_prelude_to/", "traveller"),
 "jg_shimanami":   ("japan-guide — Shimanami Kaido by bus", "https://www.japan-guide.com/e/e3478.html", "third-party"),
 "setouchi_bus":   ("Setouchi Bus — Shimanami Liner", "https://www.setouchibus.co.jp/highway/fukuyama.html", "operator"),
 "shimanami_cyc":  ("Shimanami Japan — rental cycle terminals and fees", "https://shimanami-cycle.or.jp/rental/rental/", "operator"),
 "dive_hiroshima": ("Hiroshima Prefecture — Ōkunoshima access", "https://dive-hiroshima.com/en/feature/usagi-okunoshima/", "official"),
 "omishima_fare":  ("Ōmishima Ferry — fare table (http only)", "http://sanyo-shosen.jp/omishima/fare.html", "operator"),
 "rabbit_island":  ("Tadanoumi Port — official Ōkunoshima site", "http://rabbit-island.info/en/", "official"),
 "geiyo":          ("Geiyo Bus — Kaguya-hime expressway line", "https://www.geiyo.co.jp/expwy_bus.html", "operator"),
 "hiroden_pass":   ("Hiroden — one-day tram & ferry pass", "https://www.hiroden.co.jp/ticket-pass/bargain-tickets/oneday.html", "operator"),
 "hiroden_fare":   ("Hiroden — flat fare", "https://www.hiroden.co.jp/train/use/index.html", "operator"),
 "miyajima_rw":    ("Miyajima Ropeway — fares", "https://miyajima-ropeway.info/fare/", "operator"),
 "jr_miyajima":    ("JR West Miyajima Ferry", "https://www.jr-miyajimaferry.co.jp/en/", "operator"),
 "miyajima_tax":   ("Hatsukaichi City — Miyajima visitor tax", "https://www.city.hatsukaichi.hiroshima.jp/soshiki/110/59551.html", "official"),
 "jenova":         ("Awaji Jenova Line — timetable and fares", "https://www.jenova-line.co.jp/jikoku.php", "operator"),
 "awaji_pass":     ("Awaji Kōtsū — island bus day pass", "https://www.awaji-kotsu.co.jp/profit/", "operator"),
 "awaji_local":    ("Awaji Kōtsū — local route fares (PDF)", "https://www.awaji-kotsu.co.jp/local/", "operator"),
 "awaji_toku":     ("Awaji Kōtsū — Awaji–Tokushima line timetable (PDF)", "https://www.awaji-kotsu.co.jp/_assets/d762e18f435947a5af53e214e409edf2/2010ff933887412ebc4b1dc34395fff3/l_2060_current.pdf", "operator"),
 "awashin":        ("Awaji City — Awa-shin/Awa-hime community bus", "https://www.honshi-bus.co.jp/local/view/11", "operator"),
 "uzunomichi":     ("Uzu-no-michi — admission", "https://www.uzunomichi.jp/usage-guide-uzu-no-michi/", "operator"),
 "uzu_tide":       ("Uzu-no-michi — official tide calendar", "https://www.uzunomichi.jp/tide-calendar/", "operator"),
 "wonder_naruto":  ("Uzushio Cruise — Wonder Naruto fares", "https://www.uzusio.com/geton/", "operator"),
 "tokubus_naruto": ("Tokushima Bus — Naruto Park line timetable (PDF)", "https://www.tokubus.co.jp/themes/default/pdf/kaisei260401/c1_sogo_narutopark.pdf", "operator"),
 "tokubus_fare":   ("NAVITIME / japan-guide (operator publishes only a graphic matrix)", "https://www.japan-guide.com/e/e7852.html", "third-party"),
 "srn_takmat":     ("Shikoku Rail Note — Takamatsu–Matsuyama by local train", "https://shikoku-railway-note.com/takamatsu-matsuyama-futsu-densha/", "third-party"),
 "seishun18":      ("JR — Seishun 18 kippu product page", "https://jr-group.jp/seishun18/", "operator"),
 "tabiris18":      ("Tabiris — 2026 Seishun 18 dates and rules", "https://tabiris.com/archives/seishun18-2026/", "third-party"),
 "nkishou":        ("Nihon Kishou — autumn foliage forecast", "https://n-kishou.com/corp/news-contents/autumn/", "official"),
 "ritsurin":       ("Ritsurin Garden — official", "https://www.my-kagawa.jp/ritsuringarden/", "official"),
}


# method-substring -> source key.  First match wins, so order matters.
MATCH = [
 ("Shin-Kaisoku",                 "ekitan_osa_him"),
 ("Shinki Bus route 94",          "shinki_fare"),
 ("Shodoshima Ferry",             "sf_himeji"),
 ("Olive Bus, South Fukuda",      "olive_bus"),
 ("Olive Bus 1-day pass",         "olive_bus"),
 ("FREE town shuttle",            "kankakei_shut"),
 ("Ropeway (rises",               "kankakei_rw"),
 ("Ropeway",                      "kankakei_rw"),
 ("Shikoku Ferry (car ferry)",    "sf_takamatsu"),
 ("Shikoku Ferry",                "sf_takamatsu"),
 ("JR Kōtoku Line local",         None),          # no published fare found
 ("Kōtoku Express",               "kotoku_exp"),
 ("JR Tokushima Line local",      "yahoo_transit"),
 ("JR Dosan Line local",          "jg_oboke"),
 ("Local bus, 4 min",             "miyoshi_en"),
 ("Sightseeing boat",             "oboke_boat"),
 ("LAST BUS of the day",          "yonkoh_time"),
 ("Shikoku Kotsu bus",            "jg_iya_bus"),
 ("Shikoku Kotsu, Higashi-Iya",   "yarina"),
 ("Miyoshi City bus",             "miyoshi_en"),
 ("Mt Tsurugi chairlift",         "tsurugi_lift"),
 ("MY-YU",                        "myyu_half"),
 ("Tosaden",                      "tosaden"),
 ("Nangoku Express",              "nangoku"),
 ("Chair lift",                   "naka1951"),
 ("Iyotetsu tram",                "naka1951"),
 ("JR Yosan Line local",          "turkeydinner"),
 ("JR Yosan Line, all local",     "srn_takmat"),
 ("Shimanami Liner",              "jg_shimanami"),
 ("JR Sanyo Line local",          None),
 ("JR Kure Line local",           "dive_hiroshima"),
 ("Ferry — CASH ONLY",            "omishima_fare"),
 ("per bag per day",              "rabbit_island"),
 ("Geiyo Bus",                    "geiyo"),
 ("Hiroden 1-day",                "hiroden_pass"),
 ("Ropeway — ¥1,500",             "miyajima_rw"),
 ("Jenova Line ferry",            "jenova"),
 ("Community or highway bus",     "awashin"),
 ("Awaji Kōtsū 1-day pass",       "awaji_pass"),
 ("Awaji Kōtsū",                  "awaji_toku"),
 ("Walkway under the bridge",     "uzunomichi"),
 ("Wonder Naruto",                "wonder_naruto"),
 ("Tokushima Bus",                "tokubus_fare"),
 ("JR local via Tadotsu",         "yahoo_transit"),
 ("JR Sanyo Line",                None),
]


_MATCH_ORDER = None


def resolve(method):
    """method string -> (label, url, tier) or None.

    Matched LONGEST FRAGMENT FIRST, not in list order. Insertion order is a trap:
    a generic rule sitting above a specific one silently steals it — the bare
    "Ropeway" rule was claiming Miyajima's "Ropeway — ¥1,500 with the pass" and
    citing Kankakei on Shodoshima, 200 km away. Sorting by specificity makes the
    table order-independent, so adding a rule can no longer break an old one.
    """
    global _MATCH_ORDER
    if _MATCH_ORDER is None or len(_MATCH_ORDER) != len(MATCH):
        _MATCH_ORDER = sorted(MATCH, key=lambda kv: len(kv[0]), reverse=True)
    for frag, key in _MATCH_ORDER:
        if frag in method:
            return SOURCES[key] if key else None
    return None


for _k, _v in {
 "bassetts": ("Bassett's Bouken — West Japan in a week", "https://bassettsbouken.com/west-japan-in-a-week-itinerary/", "traveller"),
 "mrhoca": ("mrhocA — A week in Shikoku, Feb 2026 (FlyerTalk)", "https://www.flyertalk.com/forum/trip-reports/2213067-week-shikoku.html", "traveller"),
 "gift_blog": ("Space Stories by Gift — Iya Valley by bus", "https://spacestoriesbygift.wordpress.com/2019/06/30/iya-valley-kazurabashi-vine-bridge/", "traveller"),
 "ptr_iya": ("Perchance to Roam — Iya Valley on public buses only", "https://perchancetoroam.com/2022/04/12/the-ultimate-guide-to-the-iya-valley-japan/", "traveller"),
 "nickjerry": ("Nick & Jerry — Ōkunoshima day trip", "https://www.nickandjerry.com/blog/japan-2023-day-13-okunoshima-island-aka-rabbit-island", "traveller"),
 "japan_experience": ("Japan Experience — Takehara", "https://www.japan-experience.com/all-about-japan/hiroshima/attractions-excursions/takehara", "third-party"),
}.items():
    SOURCES[_k] = _v


SOURCES.update({
 "olive_fukuda":  ("Olive Bus — South Fukuda Line timetable, 1 Apr 2026 rev. (PDF)", "https://www.shodoshima-olive-bus.com/wp/wp-content/uploads/2021/09/dia_minamihukuda_kudari.pdf", "operator"),
 "olive_sakate":  ("Olive Bus — Sakate Line timetable, 1 Apr 2026 rev. (PDF)", "https://www.shodoshima-olive-bus.com/wp/wp-content/uploads/2021/09/dia_sakate_kudari.pdf", "operator"),
 "olive_fare_pdf":("Olive Bus — Fukuda line fare chart (PDF)", "https://www.shodoshima-olive-bus.com/wp/wp-content/uploads/2021/09/fare_chart-fukuda_w.pdf", "operator"),
 "kankakei_pdf":  ("Shodoshima Town — FY2026 Kankakei shuttle timetable (PDF)", "https://www.town.shodoshima.lg.jp/material/files/group/6/R8choeibuskankakeisengaiyo.pdf", "official"),
 "kankakei_cal":  ("Shodoshima Town — FY2026 Kankakei shuttle operating calendar (PDF)", "https://www.town.shodoshima.lg.jp/material/files/group/6/R8choeibuskankakeisencalendar.pdf", "official"),
 "nakabuan":      ("Nakabu-an — somen hand-stretching experience", "https://shodoshima-nakabuan.co.jp/experience/", "operator"),
 "nakabuan_time": ("Shodoshima Tourism Association — Nakabu-an session times", "https://shodoshima.or.jp/sightseeing/detail.php?id=216&c=2", "official"),
 "hirokiya":      ("Hirokiya Ryokan, Yasuda — rates via the tourism association", "https://shodoshima.or.jp/sightseeing/detail.php?id=117&c=4", "official"),
 "hirokiya_acc":  ("Hirokiya Ryokan — access and free port pick-up", "http://hirokiya.net/access.php", "operator"),
 "chigusa":       ("Chigusa Ryokan, Fukuda Port — rates via the tourism association", "https://shodoshima.or.jp/sightseeing/detail.php?id=477&c=4", "official"),
 "marukin_kagawa":("Kagawa tourism board — Marukin museum hours and price", "https://www.my-kagawa.jp/point/235/", "official"),
})


MATCH[:0] = [
 ("Olive Bus, South Fukuda Line",  "olive_fukuda"),
 ("Olive Bus, Sakate Line",        "olive_sakate"),
 ("free Kankakei shuttle",         "kankakei_pdf"),
]


SOURCES.update({
 "miyajima_tide": ("Miyajima Tourist Association — monthly tide tables (Oct 2026)", "https://www.miyajima.or.jp/sio/sio10.html", "official"),
 "jma_tide":      ("Japan Meteorological Agency — national tide tables", "https://www.jma.go.jp/bosai/tide/", "official"),
 "uzu_kisen_tide":("Uzushio Kisen — whirlpool tide table", "https://www.uzushio-kisen.com/shiomihyou.html", "operator"),
 "uzusio_tide_en":("Uzushio Cruise — tide table, English", "https://www.uzusio.com/en/siomi/", "operator"),
})


SOURCES.update({
 "yamap":        ("YAMAP — Japan's main hiking app, GPS tracking + offline maps", "https://yamap.com/", "operator"),
 "nishiawa":     ("Nishi-Awa Tourism — Mt Tsurugi official trail descriptions", "https://nishi-awa.jp/tsurugisan/", "official"),
 "miyajima_toz": ("Miyajima Tourism Association — Mt Misen trail courses", "https://www.miyajima.or.jp/course/course_tozan3.html", "official"),
 "kankakei_trl": ("Kankakei Ropeway — the two gorge walking trails", "https://www.kankakei.co.jp/miryoku/", "operator"),
 "konpira_off":  ("Konpira-san — the shrine's own visitor guide", "https://www.konpira.or.jp/articles/20200616_guide/article.htm", "official"),
 "oboke_teku":   ("Miyoshi City — Ōboke walking map (PDF, 4 graded courses)", "https://miyoshi-tourism.jp/wp-content/uploads/2024/10/teku_oboke.pdf", "official"),
 "shimanami_op": ("Shimanami Japan — how long the ride actually takes", "https://shimanami-cycle.or.jp/go-shimanami/experience/613/", "operator"),
 "touring_shim": ("Touring Shimanami — local cyclist, 2-day plan in our direction", "https://touring-shimanami.com/en/2days-cycling-e/", "third-party"),
 "touring_wind": ("Touring Shimanami — wind analysis by season and direction", "https://touring-shimanami.com/wind/", "third-party"),
 "touring_dist": ("Touring Shimanami — measured per-island distances", "https://touring-shimanami.com/distance/", "third-party"),
 "sagawa_bags":  ("Sagawa — Shimanami Hands-Free Cycling luggage transfer", "https://www.sagawa-exp.co.jp/hands-freetravel/service/cycling/", "operator"),
 "cyclonoie":    ("Cyclonoie — cyclists' guest house, 1 min from Imabari Station", "https://www.cyclonoie.com/", "operator"),
 "setouchi_cru": ("Setouchi Cruising — Onomichi ⇄ Setoda, bikes roll aboard", "https://s-cruise.jp/timetable/", "operator"),
 "omishima_bl":  ("Ōmishima Blue Line — Imabari ⇄ Ōmishima ferry", "https://omishima-bl.net/", "operator"),
 "train_cycling":("train-cycling.com — GPS-measured 79.8 km log with beginner timings", "https://train-cycling.com/shimanami-time-required/", "third-party"),
 "epic_roads":   ("Epic Road Rides — recommends 3 days for casual riders", "https://epicroadrides.com/cycling-blog/shimanami-kaido-cycle-route-faqs/", "third-party"),
 "tomarigi":     ("TOMARIGI — hostel, Ōmishima Miyaura", "https://oomishimatomarigi.wixsite.com/tomarigi", "operator"),
 "wakka":        ("WAKKA — cycling resort, Ōmishima Inokuchi", "https://wakka.site/hotel/dormitory/", "operator"),
})


SOURCES.update({
 "jumbo":      ("Jumbo Ferry — Kobe ⇄ Takamatsu, incl. the overnight sailing", "https://ferry.co.jp/en/sea_route/kobe-takamatsu/", "operator"),
 "shikoku_kisen":("Shikoku Kisen — Takamatsu ⇄ Naoshima ferry", "https://www.shikokukisen.com/", "operator"),
 "jg_naoshima":("japan-guide — Naoshima access and island bus", "https://www.japan-guide.com/e/e5476.html", "third-party"),
 "jg_teshima": ("japan-guide — Teshima access and sailing frequency", "https://www.japan-guide.com/e/e5440.html", "third-party"),
 "jg_kotohira":("japan-guide — Kotohira access, Kotoden vs JR", "https://www.japan-guide.com/e/e5453.html", "third-party"),
 "jg_ritsurin":("japan-guide — Ritsurin Garden access and fares", "https://www.japan-guide.com/e/e5401.html", "third-party"),
 "jg_shodo":   ("japan-guide — Shodoshima ferries and island bus", "https://www.japan-guide.com/e/e5431.html", "third-party"),
 "setonaikai": ("Setonaikai Kisen — Matsuyama ⇄ Hiroshima Cruise Ferry", "https://setonaikaikisen.co.jp/language/en/cruise/", "operator"),
 "ptr_ferry":  ("Perchance to Roam — rode the Matsuyama–Hiroshima ferry, logged the port access", "https://perchancetoroam.com/2022/03/30/taking-the-ferry-between-matsuyama-and-hiroshima-what-you-need-to-know/", "traveller"),
 "futamichi":  ("ふたみち — 5-night car-free Shikoku loop, two people, with a costed breakdown", "https://futamichi-life.com/shikoku-roundtrip-train-only-experience/", "traveller"),
 "jg_forum_171710": ("japan-guide forum — 'Shikoku trip doable?', the two-base argument", "https://www.japan-guide.com/forum/quereadisplay.html?0+171710", "traveller"),
 "iyotetsu_kochi": ("Iyotetsu — Matsuyama–Kōchi Whale Express, reservation-only", "https://www.iyotetsu.co.jp/bus/kousoku/kochi.html", "operator"),
})


MATCH[:0] = [
 ("Jumbo Ferry",                  "jumbo"),
 ("Shikoku Kisen ferry",          "jg_naoshima"),
 ("Teshima ferry",                "jg_teshima"),
 ("Kotoden to Kotohira",          "jg_kotohira"),
 ("Kotoden to Ritsurin",          "jg_ritsurin"),
 ("Shodoshima ferry",             "jg_shodo"),
 ("Setonaikai Kisen Cruise Ferry","setonaikai"),
 ("Iyotetsu port shuttle",        "ptr_ferry"),
]


MATCH[:0] = [
 ("Town bus, flat fare",          "jg_naoshima"),
 ("JR Yosan Line — or the LEX",   "srn_takmat"),
 ("Hiroden tram line 5",          "hiroden_fare"),
]


SOURCES.update({
 "hpm":        ("Hiroshima Peace Memorial Museum — official", "https://hpmmuseum.jp/", "official"),
 "itsukushima":("Itsukushima Shrine — admission and hours", "https://www.itsukushimajinja.jp/jp/admission.html", "official"),
 "daishoin":   ("Daishō-in, Miyajima — official", "https://daisho-in.com/", "official"),
 "dokugasu":   ("Takehara City — Ōkunoshima Poison Gas Museum", "https://www.city.takehara.lg.jp/soshikikarasagasu/chiikizukurika/gyomuannai/7/1957.html", "official"),
 "kosanji":    ("Kōsanji Temple, Ikuchijima — official", "https://www.kousanji.or.jp/", "operator"),
})


SOURCES.update({
 "benesse_chichu": ("Benesse Art Site — Chichu Art Museum", "https://benesse-artsite.jp/en/art/chichu.html", "operator"),
 "benesse_teshima":("Benesse Art Site — Teshima Art Museum", "https://benesse-artsite.jp/en/art/teshima-artmuseum.html", "operator"),
 "benesse_house":  ("Benesse Art Site — Benesse House Museum", "https://benesse-artsite.jp/en/art/benessehouse-museum.html", "operator"),
 "benesse_arthouse":("Benesse Art Site — Art House Project, Honmura", "https://benesse-artsite.jp/en/art/arthouse.html", "operator"),
 "benesse_tickets":("Benesse Art Site — ticket portal and booking window", "https://benesse-artsite.eventos.tokyo/", "operator"),
 "awaodori":       ("Awa Odori Kaikan — fees, shows and the Bizan ropeway", "https://www.awaodori-kaikan.jp/fee", "operator"),
 "otsuka":         ("Ōtsuka Museum of Art — admission", "https://o-museum.or.jp/pages/28/", "operator"),
 "matsuyamajo":    ("Matsuyama Castle — keep, ropeway and chair lift fees", "https://www.matsuyamajo.jp/guide/#fee", "operator"),
 "ninomaru":       ("Matsuyama — Ninomaru historic garden", "https://www.matsuyamajo.jp/guide/ninomaru.html", "operator"),
 "dogo_honkan":    ("Dogo Onsen Honkan — bathing tiers", "https://dogo.jp/onsen/honkan", "operator"),
 "dogo_asuka":     ("Dogo Onsen Asuka-no-Yu", "https://dogo.jp/onsen/asuka", "operator"),
})


SOURCES.update({
 "takaya_shuttle": ("Kan-onji City — Takaya Shrine shuttle bus (updated 12 Aug 2026)",
                    "https://www.city.kanonji.kagawa.jp/soshiki/21/22812.html", "official"),
 "takaya_access":  ("Kan-onji City — Takaya Shrine, the 270 steps and the road ban",
                    "https://www.city.kanonji.kagawa.jp/soshiki/21/13387.html", "official"),
 "takaya_mitoyo":  ("Mitoyo Tourism — Takaya Shrine, 20 min walk from JR Kan-onji",
                    "https://www.mitoyo-kanko.com/takayashrine/", "official"),
 "takaya_fare26":  ("Cool Kagawa — shuttle fare rise to ¥1,500 from 1 March 2026",
                    "https://www.coolkagawa.jp/news/entry-2912.html", "official"),
 "yamap_inazumi":  ("YAMAP — Inazumiyama 404 m, model course 2.5 km / 354 m / 2 h",
                    "https://yamap.com/mountains/8797", "third-party"),
 "hearts_shuttle": ("Mitoyo Chuo Kanko — Hearts Shuttle, ¥1,500 hop-on-hop-off",
                    "https://www.mitoyochuo-kanko.co.jp/home/business_overview-3/hearts_shuttle/", "operator"),
 "sanseto_taxi":   ("Sanseto Sunset Shuttle Taxi — weekday shared taxi, route 4 ¥2,000",
                    "https://k-sss.com/sunset/", "operator"),
 "iroha_taxi":     ("Iroha Taxi — published fares from JR Kan-onji station",
                    "https://www.iroha-taxi.net/taxi/", "operator"),
 "kanonji_noriai": ("Kan-onji City — Noriai community bus, ¥100 flat, 4/day, no Sundays",
                    "https://www.city.kanonji.kagawa.jp/soshiki/7/206.html", "official"),
 "zenigata":       ("Kan-onji City — Zenigata Sunae, free and open 24 h",
                    "https://www.city.kanonji.kagawa.jp/soshiki/21/333.html", "official"),
 "chichibu":       ("Mitoyo Tourism — Chichibugahama and the official mirror calendar",
                    "https://www.mitoyo-kanko.com/chichibugahama/", "official"),
 "jr_yosan_fare":  ("JR Shikoku — official Yosan Line fare table (PDF)",
                    "https://www.jr-shikoku.co.jp/01_trainbus/rosen/yosan.pdf", "operator"),
 "jr_saihakken":   ("JR Shikoku — Shikoku Saihakken Hayatoku Kippu, ¥2,400, Sat/holidays only",
                    "https://www.jr-eki.com/ticket/brand/2-3W0", "operator"),
 "ritsurin":       ("My Kagawa — Ritsurin Garden official guide, fees and monthly hours",
                    "https://www.my-kagawa.jp/ritsuringarden/feature/ritsuringarden/guide", "official"),
 "konpira":        ("Kotohira-gu official site — grounds, Treasure House calendar",
                    "https://www.konpira.or.jp/", "official"),
 "konpira_museum": ("Kotohira-gu — Treasure House and Shoin opening calendar",
                    "https://www.konpira.or.jp/index.htm?stageID=hp_museum", "official"),
 "kanamaruza":     ("Kotohira Town — Kyu-Konpira Ozashiki, Kanamaru-za",
                    "https://www.town.kotohira.kagawa.jp/soshiki/3/1270.html", "official"),
 "tamamo":         ("Takamatsu City — Tamamo Park fees and monthly gate hours",
                    "https://www.city.takamatsu.kagawa.jp/kurashi/kurashi/shisetsu/park/tamamo/bunzai2018060.html", "official"),
 "shikokumura":    ("Shikoku Mura Museum — admission and hours",
                    "https://www.shikokumura.or.jp/information/", "operator"),
 "yashima_navi":   ("Yashima Navi — the official portal (prices NOT published)",
                    "https://yashima-navi.jp/", "official"),
 "chichibu_sunset_bus": ("Chichibugahama sunset shuttle bus from JR Kotohira — daily, sunset-timed",
                    "https://www.mitoyo-kanko.com/chichibugahama/", "official"),
})


MATCH[:0] = [
 ("Takaya Shrine shuttle", "takaya_shuttle"),
 ("Hearts Shuttle",        "hearts_shuttle"),
 ("sunset shuttle",        "chichibu_sunset_bus"),
 ("JR Yosan Line rapid",   "jr_yosan_fare"),
]


# ── Source rules that were missing, found by auditing every leg ──────────────
# resolve() now matches longest-fragment-first, so these are order-independent.
MATCH.extend([
 ("Rented cross bike",                      "shimanami_cyc"),
 ("Shimanami rental cycle",                 "shimanami_cyc"),
 ("Sagawa Hands-Free Cycling",              "sagawa_bags"),
 ("Setouchi Cruising ferry",                "setouchi_cru"),
 ("Same shuttle — return included",         "takaya_shuttle"),
 # The Yosan Line fares are on JR Shikoku's own PDF fare table — use the
 # operator, not the traveller blog that happened to log one of these legs.
 ("JR Yosan Line local train",              "jr_yosan_fare"),
 # Matsuyama's chair lift and keep fees are published by the castle itself.
 ("Chair lift",                             "matsuyamajo"),
])


SOURCES["kaneyoshi"] = (
 "Onomichi ⇄ Mukaishima ferry — ¥100 is what travellers consistently report; I could "
 "NOT confirm it on an operator or city page (ononavi.jp returns 403 to automated access). "
 "Treat as unverified and carry coins.",
 "https://www.ononavi.jp/sightseeing/tosen/", "traveller")


MATCH.append(("Kaneyoshi ferry", "kaneyoshi"))


# The old ("Chair lift" -> traveller blog) rule ties on length with the operator
# one above, and a stable sort keeps whichever came first. Drop the loser.
MATCH[:] = [kv for kv in MATCH if kv != ("Chair lift", "naka1951")]


_MATCH_ORDER = None


# ── Verified boarding points ────────────────────────────────────────────────
# "Take the bus" is not directions. These are the operator's own stop names,
# read off the current timetable revision rather than inferred from a map.
SOURCES.update({
 "yonkoh_iya2025": ("Shikoku Kotsu — Nishi-Iya/Iya line timetable, rev. 1 Oct 2025 (PDF)",
                    "https://yonkoh.co.jp/wp/wp-content/uploads/2025/09/tozai_iya_timetable2025.pdf",
                    "operator"),
 "miyoshi_connect": ("Miyoshi Tourism — consolidated Iya bus connection sheet, current 1 Apr 2026 "
                     "(all stop times AND fares for the Tsurugi/Nagoro wing)",
                     "https://miyoshi-tourism.jp/wp-content/uploads/2024/10/ece53a69bb92db6723984134a3745d49.pdf",
                     "official"),
 "mannaka_boat":    ("Ōboke-kyō Mannaka — the sightseeing boat, official",
                     "https://mannaka.co.jp/sightseeingboat/", "operator"),
})
MATCH.extend([
 ("Miyoshi City bus — 名頃線", "miyoshi_connect"),
 ("Shikoku Kotsu, Higashi-Iya line", "yonkoh_iya2025"),
])
