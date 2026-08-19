"""What things cost, when they are open, and how long people spend there.

ATTRACTIONS = admission, hours, closing days. BOOKINGS = what must be reserved and by
when. DWELL = how long real visitors actually stayed. TIDES = the three sights that
only work at the right water level. Plus the yen-to-shekel conversion.
"""

# Admissions and other non-transport costs, so they can be cited too.
ADMISSIONS = [
 ("Himeji Castle + Koko-en combined", 2600, "himeji_price",
  "Adult 18+, non-resident. Rose from ¥1,000 on 1 March 2026; under-18s now free."),
 ("Himeji Castle alone", 2500, "himeji_price", "Combined ticket saves only ¥300."),
 ("Kōko-en alone", 400, "himeji_en", ""),
 ("Kankakei ropeway, return", 2340, "kankakei_rw",
  "21 Mar–31 Oct. Rises to ¥2,700 for 1–30 Nov."),
 ("Iya Kazurabashi vine bridge", 550, "kazurabashi", "One-way crossing only. Adults."),
 ("Oku-Iya double vine bridges", 550, "miyoshi_en", "Closed December–March."),
 ("Ōboke gorge cruise", 1500, "oboke_boat", "30 min. Last boat 16:30. Runs all year."),
 ("Mt Tsurugi chairlift, return", 2300, "tsurugi_lift", "From 1 Apr 2026. Closed 1 Dec–29 Apr."),
 ("Yamaroku Soy Sauce tour", 0, "yamaroku", "Free, no reservation, 09:00–17:00 daily."),
 ("Uzu-no-michi glass walkway", 510, "uzunomichi", "Option B only."),
 ("Wonder Naruto whirlpool cruise", 2000, "wonder_naruto", "Option B only. No reservation needed."),
 ("Miyajima visitor tax", 100, "miyajima_tax",
  "Per person per visit since 1 Oct 2023. INCLUDED in the Hiroden ¥1,000 day pass."),
 ("Miyajima ropeway, return", 2000, "miyajima_rw", "¥1,500 with the Hiroden day pass."),
 ("Ōkunoshima rabbit food", 200, "rabbit_island",
  "Buy at Tadanoumi station before boarding — not sold on the island."),
]


# ── How long people actually spend, with who said it ────────────────────────
# (place, typical time, source key, the quote or basis)
DWELL = [
 ("Himeji Castle", "1.5–3 h", "bassetts",
  "“Exploring Himeji castle took me about an hour and a half … you could easily "
  "enjoy 2-3 hours here on a nice day.” Earth Trekkers give “2 to 4 hours”. "
  "The keep is capped at 1,000 entries an hour, so queues form on busy days."),
 ("Koko-en garden", "45–60 min", "bassetts", "“I would leave at least 45 minutes to explore Kokoen.”"),
 ("Kankakei ropeway + summit", "~1.5 h", "kankakei_shut",
  "A published car-free plan: shuttle 10:30, up at 10:47, back down 12:12."),
 ("Shodoshima Olive Park", "1–2 h", "olive_routes",
  "Open 08:30–17:00; flat, and the bus stops at the gate. No published dwell time."),
 ("Angel Road", "45–60 min", "sf_angel",
  "The sandbar is exposed for about 6 hours around each low tide; the walk out and "
  "back is short. 30 min each way on foot from Tonoshō Port."),
 ("Ritsurin Garden", "~2 h", "mrhoca", "A February 2026 visitor logged about two hours."),
 ("Ōboke gorge cruise", "30 min", "oboke_boat", "Operator's published duration, 4 km round trip."),
 ("Iya Kazurabashi vine bridge", "30–60 min", "gift_blog",
  "Crossing time is not published. One visitor queued “about 30 minutes” for the "
  "ticket counter at peak season; add Biwa Falls, 50 m away."),
 ("Iya Valley as a whole", "2.5 days car-free", "ptr_iya",
  "“We managed to see all of the above sights in two and a half days using only "
  "public buses.”"),
 ("Mt Tsurugi (bus-locked)", "3 h 45 min", "miyoshi_tsurugi",
  "Not a choice: the buses give you 11:10 → 14:55 on the mountain, or two minutes."),
 ("Kōchi Sunday Market", "1–2 h", "myyu", "Roughly 1 km of stalls up to the castle."),
 ("Kōchi — Katsurahama + Makino", "half a day", "myyu",
  "The MY-YU pass exists because these are spread out; Makino is on a mountainside."),
 ("Matsuyama Castle", "1.5–2 h", "naka1951",
  "Including the chair lift up and back. Ropeway/lift is 3 minutes each way."),
 ("Dogo Onsen bathing", "45–90 min", "naka1951", "Bathe, then the arcade for dinner."),
 ("Ōkunoshima (rabbit island)", "4–5 h", "nickjerry",
  "A couple who allowed three hours “ended up hustling back to the port” and "
  "concluded they “really needed like 5 hours”. Another spent ~3 h and was happy. "
  "A guide recommends 3–4 h minimum and 9–11 h door to door from Hiroshima."),
 ("Takehara old town", "1–2 h", "japan_experience",
  "Described as “a leisurely afternoon”; 12 minutes' walk from the station. No firm figure published."),
 ("Miyajima — shrine, town, ropeway", "half to full day", "miyajima_rw",
  "The ropeway is ~20 min each way in two stages; last ascent 16:00."),
 ("Miyajima — Mt Misen summit", "+1 h beyond the ropeway", "miyajima_rw",
  "The ropeway's own page: 「弥山の山頂へはさらに往復約1時間かかります」 "
  "— about an hour round trip, ~30 min up a steep stepped trail."),
 ("Hiroshima Peace Museum", "2–3 h", "hiroden_fare",
  "No official figure; every account says allow more time than you expect."),
 ("Shimanami Kaido, full 70 km by bike", "8–10 h", "shimanami_cyc",
  "Beginners' figure. Do not attempt it in a travel day — ride one or two bridges instead."),
]


DWELL.extend([
 ("Nakabu-an somen workshop", "45 min", "nakabuan",
  "Operator's published duration for the 箸分け hand-stretching experience, materials "
  "included. Sessions 10:00 / 11:00 / 12:30 / 13:30, max 15 people."),
 ("Yamaroku Soy Sauce", "30–60 min", "yamaroku",
  "Free, no reservation, 09:00–17:00, open year-round. Cedar-barrel warehouses you walk "
  "straight into."),

 # Visit durations found by a dedicated 所要時間 / 滞在時間 sweep, Aug 2026.
 # 17 of 34 places searched produced a figure whose source page is provably
 # about that place. The other 17 are left blank on purpose: several promising
 # hits turned out to describe a same-named site elsewhere -- a 琵琶の滝 in Nara,
 # Tomioka Silk Mill standing in for Benesse House -- and a wrong duration is
 # worse than none, because the traveller builds a day around it.
 ("A-Bomb Dome", "about 1 h", "dw_abomb",
  "\u201cAbout 1 hour is the guide. 30 minutes if you are just looking, 3 hours or more if you take it slowly.\u201d It is outdoors and free, so the time is yours to choose."),
 ("Art House Project, Honmura", "3 h to do it properly", "dw_arthouse",
  "Benesse's own model plan builds Honmura into a 4\u20135 h island visit. A visitor who had 1 h 30 wrote that it was \u201cvery tight\u201d and gave up on Kinza and Go\u2019o Shrine."),
 ("Awa Odori Kaikan", "2\u20133 h for everything; ~1 h for the show alone", "dw_awaodori",
  "Jalan reviewers repeatedly log a 2\u20133 h stay. That covers the museum, a show and the ropeway; the performance by itself is about an hour."),
 ("Awaji Yumebutai", "1 h greenhouse only; 1 h 30 with the Yumebutai grounds", "dw_yumebutai",
  "The greenhouse's own FAQ: \u201cabout 1 hour for the greenhouse alone, about 1 hour 30 including a walk around the Yumebutai area\u201d, and about 2 h if you add Akashi Kaikyo Park."),
 ("Chichu Art Museum", "60\u201390 min recommended, 30 min minimum", "dw_chichu",
  "Stated as a minimum stay of 30 minutes and a recommended 60\u201390. The building is part of the work, so rushing it defeats the point."),
 ("K\u014dsanji", "about 2 h 30", "dw_kousanji",
  "The temple museum complex alone is given as about 2 h 30."),
 ("Hill of Hope", "1 h 30 for K\u014dsanji and the Hill together", "dw_hillhope",
  "\u201cThe route takes you round the K\u014dsanji precinct first, then up to the Hill of Hope. Both together took about 1 hour 30.\u201d The marble hill sits above the temple and is reached through it."),
 ("Itsukushima Shrine", "30 min at a normal pace; 40\u201350 if you linger", "dw_itsuku",
  "\u201cThe shrine takes about 30 minutes at a normal pace \u2014 though I ended up spending 40 or 50.\u201d A Miyajima half-day plan allots it 45 minutes."),
 ("Izanagi Shrine", "45 min", "dw_izanagi",
  "\u201c45 minutes is plenty for a visit.\u201d"),
 ("K\u014dchi Castle", "30 min to 1 h", "dw_kochijo",
  "Tripadvisor reviewers give 30 minutes to an hour; a K\u014dchi half-day plan allows about 60 minutes for the castle."),
 ("Makino Botanical Garden", "2 h for a first visit; 1 h if pushed, 4 h to see it all", "dw_makino",
  "The garden publishes its own model courses: a 1-hour route, a 1 h 30 route, \u201cMakino for the first time\u201d at 2 hours, and a full 4-hour circuit."),
 ("Mt Misen ropeway top", "about 2 h for the ropeway and Shishiiwa lookout", "dw_misen",
  "The tourist association's own two-hour course: roughly 20\u201330 min each way on the ropeway including the change at Kayatani, plus about 20 min at the Shishiiwa lookout. The summit is a further 30 min of steps beyond this."),
 ("Peace Memorial Museum", "60 min typical; 30 min main building only; 2 h 30 to do it justice", "dw_peace",
  "\u201cAbout 60 minutes to view, or about 30 for the main building alone.\u201d Other guides put a thorough visit at 2 h 30, and warn that busy periods need 2.5\u20133 h."),
 ("Shikoku Mura", "about 2 h 30", "dw_shikokumura",
  "Given as about 2 h 30 for the open-air museum; another guide says 1\u20132 h is enough if you are moving briskly. It is a hillside site, so the time is mostly walking."),
 ("Uchiko", "about 1 h 30 strolling", "dw_uchiko",
  "The town's own suggested walk: \u201cabout 1 hour 30 taken slowly\u201d, covering the main townscape and its shops."),
 ("Yashima", "about 3 h", "dw_yashima",
  "Given as about 3 h for the plateau. A visitor who had 1 h 30 between shuttle buses managed the lookout and the temple but no more."),
 ("\u014ctsuka Museum", "about 2 h average", "dw_otsuka",
  "\u201cJust walking the galleries takes an hour, so reckon on about 2 hours average.\u201d The full route is over 4 km of corridor."),

 # Second dwell pass, with region qualifiers in the query. The first pass had
 # matched same-named places elsewhere; adding 祖谷 / 宮島 / 直島 to each search
 # and requiring the page to NAME the place removed that whole failure mode.
 ("Benesse House Museum", "about 1 h 30 including lunch", "dw_benesse",
  "A cyclist's itemised Naoshima day logs \u201cBenesse House Museum and lunch, 1.5 hours\u201d. The museum alone is less; it is open till 21:00, unusually late for an art museum."),
 ("Botchan Train", "about 20 min end to end", "dw_botchan",
  "\u201cIt runs daily from Matsuyama-ekimae or Matsuyama-shieki to D\u014dgo Onsen station. The trip takes about 20 minutes.\u201d A ride rather than a visit \u2014 it is transport you take for its own sake."),
 ("Nagoro", "1\u20132 h", "dw_nagoro",
  "\u201cAllow 1\u20132 hours to wander at leisure.\u201d Around 300 scarecrows across the village, in Miyoshi\u2019s Higashi-Iya."),
 ("\u014czu \u2014 Gary\u016b Sans\u014d villa", "30\u201340 min", "dw_garyu",
  "\u014czu City\u2019s own tourism page: \u201cGary\u016b Sans\u014d can be seen in about 30\u201340 minutes, even listening to the guide.\u201d Add the Ohanahan-d\u014dri lanes and the castle for a half day in the town."),
 ("Asuka-no-Yu", "~3 h for a D\u014dgo visit built around it", "dw_dogo",
  "A day-tripper who booked nothing \u201cstayed in D\u014dgo from 3:30 to 6:30 \u2014 three hours\u201d, bathing at Asuka-no-Yu and walking the arcade. The bath itself is a fraction of that."),

 ("Mt Bizan", "1\u20131.5 h; 2\u20132.5 h with the Awa Odori Kaikan below it", "dw_bizan",
  "\u201cReckon on 1 to 1.5 hours, or about 2 to 2.5 including the Awa Odori Kaikan at the foot.\u201d The ropeway starts from inside the Kaikan, so the two are naturally done together."),
 ("Tamamo Park", "60\u201390 min", "dw_tamamo",
  "Given as 60\u201390 minutes for the castle grounds \u2014 the moat is filled with SEAWATER and stocked with sea bream, which is the part people linger over."),
])


ADMISSIONS.extend([
 ("Nakabu-an somen workshop + factory tour", 1200, "nakabuan",
  "Adult; child 6–18 ¥900. 45 min. Reserve by the previous day, phone 0879-82-3669. "
  "CLOSED Tue/Wed/Thu except public holidays."),
 ("Nakabu-an factory tour only", 500, "nakabuan", "~30 min."),
 ("Fresh somen at Nakabu-an", 750, "nakabuan",
  "From ¥750 on the operator page (the town site says ¥650). Meals 10:00–13:30, "
  "also reserve the day before."),
])


# ── Tide tables: three things on this trip only work at the right water level ──
# (what, when it matters, the rule, source key, extra sources)
TIDES = [
 ("Miyajima — the floating torii",
  "Option A: 23 Oct  ·  Option B: 24 Oct",
  "Below 100 cm you can WALK OUT to the gate across the seabed. Above 250 cm it appears "
  "to FLOAT. The association publishes a month per page with both high and low water, "
  "time and height in cm — October 2026 is sio10.html.",
  "miyajima_tide", ["jma_tide"]),
 ("Angel Road, Shodoshima",
  "Option A: 11 Oct  ·  Option B: 19 Oct",
  "The sandbar to the four islets surfaces around each low tide and is walkable for "
  "roughly six hours, twice a day. The ferry company publishes the daily window.",
  "sf_angel", []),
 ("Naruto whirlpools (Option B only)",
  "Option B: 11 Oct",
  "The vortices only form around PEAK TIDAL FLOW. The usable window scales with the "
  "tide's strength: spring tide (大潮, red on the calendar) ±2 hours, middle tide ±1.5, "
  "neap tide only ±1. Pick the day off the calendar FIRST, then fit the buses round it — "
  "on a Sunday the cross-bridge bus runs three times.",
  "uzu_tide", ["uzu_kisen_tide", "uzusio_tide_en"]),
]


ADMISSIONS.extend([
 ("Shimanami cross bike, per day", 3000, "shimanami_cyc",
  "The ONLY bike type that can be dropped off at the far end. Helmet included."),
 ("Shimanami one-way drop-off surcharge", 1000, "shimanami_cyc",
  "Cross bikes and city cycles only. Charged once, not per day."),
 ("Shimanami electric-assist bicycle, per day", 4000, "shimanami_cyc",
  "MUST be returned to the renting terminal, and one-day rentals only — so it cannot "
  "cross Imabari→Onomichi one-way. Fine for an out-and-back day ride."),
 ("Shimanami e-bike, per day", 8000, "shimanami_cyc",
  "Same one-way restriction as the electric-assist. Same-terminal return only."),
 ("Sagawa Hands-Free Cycling, per bag", 2200, "sagawa_bags",
  "Same-day luggage between Onomichi, the islands and Imabari. Drop by 09:00 in "
  "Onomichi, 10:00 on the islands and at Imabari. Reserve the night before."),
 ("Setouchi Cruising, Setoda → Onomichi", 1500, "setouchi_cru",
  "Plus ¥500 for a bicycle, which rolls straight aboard. 40 min. The escape valve — "
  "it REPLACES the last riding leg rather than adding to it."),
])


# ── What each price is actually FOR ─────────────────────────────────────────
# Everything is per person unless the method string says otherwise. The two
# exceptions on this trip are luggage (charged per bag) and the bike drop-off
# surcharge (charged per bicycle). With two travellers both still double, but
# the label should say what it is rather than leaving you to guess.
def price_unit(method):
    return "per bag" if "per bag" in (method or "").lower() else "per person"


# Two fields, not one string that every renderer then has to cut in half. The old
# single-string form forced `PRICE_NOTE.split(". ", 1)[1]` at three call sites — and
# one of them was JavaScript, where split()'s second argument caps the ARRAY LENGTH
# rather than the number of splits, so it silently produced "per person. undefined".
PRICE_HEADLINE = "Every figure is PER PERSON unless marked otherwise."
PRICE_BODY = ("Luggage forwarding and bag storage are charged PER BAG — with two "
              "travellers and two bags those also double. Accommodation is not included "
              "in these totals: dorm rates quoted in the itinerary are per person, "
              "ryokan and private rooms are usually per room.")
PRICE_NOTE = PRICE_HEADLINE + " " + PRICE_BODY


# ── Currency ────────────────────────────────────────────────────────────────
# ONE self-healing formula, not two cells. GOOGLEFINANCE() exists only in Google
# Sheets; Excel and Numbers see an unknown function and raise #NAME?. IFERROR
# catches exactly that and hands back the fixed fallback — so the cell is live
# in Sheets, correct everywhere else, and typeable over in both.
JPY_ILS = 0.01858


JPY_ILS_ASOF = "16 Aug 2026"


# One formula that works everywhere. In Google Sheets GOOGLEFINANCE resolves and
# the rate is live. In Excel and Numbers the function is unknown, so it errors with
# #NAME? — and IFERROR catches that and hands back the fixed fallback instead.
LIVE_FORMULA = f'=IFERROR(GOOGLEFINANCE("CURRENCY:JPYILS"),{JPY_ILS})'


RATE_HELP = ("Live in Google Sheets, fixed everywhere else. GOOGLEFINANCE exists only in "
             "Google Sheets; in Excel or Numbers it errors and IFERROR falls back to "
             f"{JPY_ILS} (as of {JPY_ILS_ASOF}). Either way the sheet works — and you can "
             "type a rate straight over the cell whenever you like.")


# ── Attractions: what it costs, when it's open, and what will catch you out ──
# (name, where, adult price, hours, closed / seasonal, booking, source key)
ATTRACTIONS = [
 ("Himeji Castle + Koko-en (combined)", "Himeji", "¥2,600",
  "09:00–17:00, last entry 16:00", "29–30 Dec",
  "No — but the keep is capped at 1,000 entries/hour and queues form",
  "himeji_price"),
 ("Kankakei ropeway, return", "Shodoshima", "¥2,340",
  "08:30–17:00 (08:00–17:00 from 21 Oct)", "Rises to ¥2,700 for 1–30 Nov",
  "No", "kankakei_rw"),
 ("Yamaroku Soy Sauce", "Shodoshima", "FREE",
  "09:00–17:00", "Open year-round", "No reservation needed", "yamaroku"),
 ("Nakabu-an somen workshop", "Shodoshima", "¥1,200",
  "Sessions 10:00 / 11:00 / 12:30 / 13:30, 45 min", "CLOSED Tue/Wed/Thu except holidays",
  "YES — phone 0879-82-3669 by the previous day", "nakabuan"),
 # Ritsurin and Konpira had placeholder rows here reading "not yet confirmed".
 # Both were resolved later in this list (Ritsurin ¥500 with October hours;
 # Konpira grounds FREE, 08:30–17:00) but the placeholders were never removed,
 # so every deliverable stated the price twice and contradicted itself. Resolve
 # a placeholder by DELETING it, not by appending the answer.
 ("Ōboke gorge cruise", "Iya Valley", "¥1,500",
  "09:00–17:00, last boat 16:30", "Year-round; cancelled in high wind or high water",
  "No", "oboke_boat"),
 ("Iya Kazurabashi vine bridge", "Iya Valley", "¥550",
  "Sep–Mar 08:00–17:00 (Apr–Jun 08:00–18:00, Jul–Aug 07:30–18:30)",
  "Open year-round; vines replaced some winters", "No — one-way crossing only", "kazurabashi"),
 ("Oku-Iya double vine bridges", "Iya Valley", "¥550",
  "Sep–Nov 09:00–17:00", "CLOSED December–March", "No", "miyoshi_en"),
 ("Mt Tsurugi chairlift, return", "Iya Valley", "¥2,300",
  "09:00–16:30 (08:00–16:30 on October weekends)", "Closed 1 Dec – 29 Apr",
  "No", "tsurugi_lift"),
 ("Naoshima — island bus", "Naoshima", "¥100 flat",
  "roughly hourly", "—", "No", "jg_naoshima"),
 ("Uzu-no-michi glass walkway", "Naruto", "¥510",
  "Mar–Sep 09:00–18:00 (last 17:30); Oct–Feb 09:00–17:00 (last 16:30)",
  "2nd Monday of Mar/Jun/Sep/Dec", "No", "uzunomichi"),
 ("Wonder Naruto whirlpool cruise", "Naruto", "¥2,000",
  "12 sailings, 09:00–16:20, ~30 min", "Tide-dependent — check the calendar first",
  "No reservation (Aqua Eddy at ¥2,500 DOES need one)", "wonder_naruto"),

 ("Kōsanji + Hill of Hope", "Ikuchijima (Shimanami)", "¥1,800",
  "09:00–17:00, last entry 16:30", "Chōseikaku hall is ¥500 extra",
  "No", "kosanji"),
 ("Itsukushima Shrine", "Miyajima", "¥300 (¥500 with the Treasure Hall)",
  "06:30–18:00 — but 06:30–17:30 FROM 15 OCTOBER", "Open all year", "No", "itsukushima"),
 ("Daishō-in temple", "Miyajima", "FREE",
  "Grounds 08:00–17:00 (changed from 06:00–18:00 in April 2025)", "—", "No", "daishoin"),
 ("Miyajima ropeway, return", "Miyajima", "¥2,000 (¥1,500 with the Hiroden day pass)",
  "Ascents 09:00–16:00", "Summit is a further ~30 min walk beyond the top station",
  "No", "miyajima_rw"),
 ("Miyajima visitor tax", "Miyajima", "¥100 per person per visit",
  "Collected with the ferry ticket", "Included in the Hiroden ¥1,000 day pass",
  "No", "miyajima_tax"),
 ("Ōkunoshima Poison Gas Museum", "Ōkunoshima", "¥150 (under 19 free)",
  "09:00–16:00, last entry 15:40", "29 Dec – 3 Jan",
  "No. ⚠️ Third-party pages still say ¥100 — it is ¥150", "dokugasu"),
 ("Hiroshima Peace Memorial Museum", "Hiroshima", "¥200 (high school ¥100, under 15 free)",
  "Mar–Nov 07:30–19:00, last entry 18:30", "30–31 Dec, and mid-February",
  "Only for the 07:30–08:30 and 17:30–18:30 slots — mid-day walk-up is fine", "hpm"),
]


ATTRACTIONS.extend([
 ("Chichu Art Museum", "Naoshima", "¥2,500 online / ¥2,800 on-site (weekend ¥2,700/¥3,000)",
  "10:00–17:00, last entry 16:00", "MONDAYS (open on holidays, shut the next day)",
  "YES — dated, timed booking required. If online sells out there are NO door sales",
  "benesse_chichu"),
 ("Teshima Art Museum", "Teshima", "¥1,800 online / ¥2,000 on-site",
  "FROM 1 OCT: 10:00–16:00, last entry 15:30 (shorter than summer)",
  "TUESDAYS (Mar–Nov)", "YES — dated, timed booking required", "benesse_teshima"),
 ("Benesse House Museum", "Naoshima", "¥1,300 online / ¥1,500 on-site",
  "08:00–21:00, last entry 20:00", "Open year-round",
  "No timed slot — but buy online, it's ¥200 cheaper", "benesse_house"),
 ("Lee Ufan Museum", "Naoshima", "¥1,200 online / ¥1,400 on-site",
  "10:00–17:00, last entry 16:30", "MONDAYS", "No timed slot", "benesse_house"),
 ("Art House Project, 5 houses", "Naoshima (Honmura)", "¥1,200 online / ¥1,400 on-site",
  "10:00–12:00 and 13:00–16:30 (varies by house)", "MONDAYS; Kinza also Tue–Wed",
  "Multi-site ticket no. Minamidera and Kinza YES — both dated and timed",
  "benesse_arthouse"),
 ("Awa Odori Kaikan museum", "Tokushima", "¥500",
  "09:00–17:00, last entry 16:45", "2nd Wed of Feb/Jun/Sep/Dec; 28 Dec–1 Jan",
  "No", "awaodori"),
 ("Awa Odori — daytime show", "Tokushima", "¥1,300",
  "11:00 / 14:00 / 15:00 / 16:00, 40 min each", "As above",
  "No — buy on the door", "awaodori"),
 ("Awa Odori — evening show (famous troupes)", "Tokushima", "¥1,600",
  "20:00–20:50", "As above", "not stated", "awaodori"),
 ("Mt Bizan ropeway, return", "Tokushima", "¥1,500",
  "Apr–Oct 09:00–21:00, every 15 min", "2nd Wed of Feb/Jun/Sep/Dec",
  "No", "awaodori"),
 ("Awa Odori 3-in-1 set (museum + day show + ropeway)", "Tokushima", "¥2,640",
  "—", "Evening show NOT included", "No", "awaodori"),
 ("Ōtsuka Museum of Art", "Naruto", "¥3,300 on the day (¥3,160 advance)",
  "09:30–17:00, tickets sold to 16:00", "MONDAYS (open the next day if a holiday)",
  "No — but advance is ¥140 cheaper", "otsuka"),
 ("Matsuyama Castle keep", "Matsuyama", "¥520",
  "09:00–17:00, keep entry closes 30 min before", "3rd Wed of December",
  "No", "matsuyamajo"),
 ("Matsuyama ropeway / chair lift", "Matsuyama", "¥520 return, ¥270 one way",
  "Ropeway 08:30–17:30; chair lift 08:30–17:00", "Chair lift stops in rain",
  "No", "matsuyamajo"),
 ("Ninomaru historic garden", "Matsuyama", "¥200",
  "09:00–17:00", "3rd Wed of December", "No", "ninomaru"),
 ("Dogo Onsen Honkan — Kami-no-Yu, ground floor", "Matsuyama", "¥700",
  "06:00–23:00, last tickets 22:30", "not stated",
  "No — but there's a numbered-queue system when busy", "dogo_honkan"),
 ("Dogo Onsen Honkan — Tama-no-Yu, 2nd floor", "Matsuyama", "¥2,000",
  "06:00–22:00, last tickets 21:00", "not stated", "No", "dogo_honkan"),
 ("Dogo Asuka-no-Yu — 1st floor bath", "Matsuyama", "¥610",
  "06:00–23:00, last entry 22:30", "not stated",
  "Cannot be booked — same day only", "dogo_asuka"),
])


# Things that must be booked, and by when.
BOOKINGS = [
 ("Naoshima — Chichu Art Museum", "Dated + timed ticket, no door sales if it sells out",
  "Tickets open 10:00 JST on the SECOND FRIDAY of the month two months ahead. "
  "For mid-October 2026 that was Friday 14 August 2026 — already open, book now.",
  "benesse_tickets"),
 ("Teshima — Teshima Art Museum", "Dated + timed ticket", "Same booking window as Chichu.",
  "benesse_tickets"),
 ("Naoshima — Minamidera and Kinza", "Dated + timed; Kinza is one person per 15-min slot",
  "Same window. The other Art House sites need no booking.", "benesse_tickets"),
 ("Shodoshima — Nakabu-an somen workshop", "Phone 0879-82-3669",
  "By the previous day. CLOSED Tue/Wed/Thu except public holidays.", "nakabuan"),
 ("Naruto — Aqua Eddy whirlpool boat", "Reservation required (the ¥2,000 Wonder Naruto is walk-up)",
  "Book once your tide date is fixed.", "wonder_naruto"),
 ("Shimanami — Sagawa luggage transfer", "Reserve the night before",
  "Drop by 09:00 in Onomichi, 10:00 on the islands and at Imabari.", "sagawa_bags"),
 ("Kōchi → Matsuyama highway bus", "Reservation-only, all seats assigned",
  "Options A and B only. No walk-up. Book as soon as dates are fixed.", "iyotetsu_kochi"),
 ("Shimanami — Imabari→Hiroshima direct bus", "All seats reserved, advance purchase",
  "Bookable from one month ahead until 30 min before departure.", "setouchi_bus"),
]


DWELL.extend([
 ("Takaya Shrine (upper shrine, by shuttle)", "1–1.5 h door to door", "takaya_shuttle",
  "25 min up, then about 150–200 m of steep slope from the summit car park to the torii. "
  "30–40 minutes at the gate is plenty. Departures are every 30 min, so the natural visit "
  "is one bus up and the one after next back down."),
 ("Zenigata Sunae viewpoint", "15–30 min", "hearts_shuttle",
  "The Hearts Shuttle builds in a 15-minute photo halt here, which is the operator's own "
  "measure of how long it takes. Free and open 24 hours."),
 ("Chichibugahama (for the mirror)", "1.5–2 h", "chichibu",
  "You want to be in place well before sunset and stay through it — the reflection is at "
  "its best in the last hour of light. The official calendar publishes a window per day."),
 ("Kotohira — Konpira-san and Kanamaru-za", "3–4 h", "konpira",
  "785 steps to the main hall at an unhurried pace, plus the shopping stairway and the "
  "kabuki theatre. The inner shrine (1,368 steps) adds about another hour."),
])


ATTRACTIONS.extend([
 ("Takaya Shrine — the shrine itself", "Kan-onji, Kagawa", "FREE",
  "Not published — it is an open hilltop site, unfenced",
  "Shrine office often unstaffed; goshuin and omamori come from vending machines at the top",
  "No", "takaya_access"),
 ("Takaya Shrine shuttle bus, return", "Kan-onji, Kagawa", "¥1,500 (child ¥700)",
  "Up 10:30–17:00, down 11:00–18:00, every 30 min — NO 12:30 or 15:00 up, NO 13:00 or 15:30 down",
  "SATURDAYS, SUNDAYS AND PUBLIC HOLIDAYS ONLY — it does not run on a weekday",
  "CANNOT be reserved. Tickets from a machine at the tourism office from 09:00, ¥1,000 notes "
  "only, 20 seats a bus, and it sells out in good weather", "takaya_shuttle"),
 ("Hearts Shuttle — all-day hop-on-hop-off", "Kan-onji / Mitoyo", "¥1,500 (child ¥700)",
  "Loops JR Takuma – Chichibugahama – Takaya lower shrine – Zenigata – Kotohiki Park – JR Kan-onji",
  "Saturdays, Sundays and public holidays only",
  "Reserve by 17:00 three days before; walk-up only if seats remain", "hearts_shuttle"),
 ("Zenigata Sunae sand coin", "Kan-onji, Kagawa", "FREE",
  "24 hours; floodlit from sunset to 22:00", "Never", "No", "zenigata"),
 ("Chichibugahama beach", "Mitoyo, Kagawa", "FREE",
  "Open beach, no gate", "Never — but the MIRROR needs low tide at sunset plus still air",
  "No — but check the official mirror calendar before picking your day", "chichibu"),
 ("Ritsurin Garden", "Takamatsu", "¥500 (child ¥170)",
  "OCTOBER 06:00–17:30 — the hours move month by month with sunrise and sunset",
  "No closing day at all; may shut on a gale warning", "No", "ritsurin"),
 ("Konpira-san — grounds and main shrine", "Kotohira", "FREE",
  "Worship area and shop 08:30–17:00", "None", "No", "konpira"),
 ("Konpira-san — Treasure House", "Kotohira", "¥800 (high school + university ¥400, JHS and under free)",
  "09:00–17:00, last entry 16:30",
  "OPEN DAILY 1 Oct–30 Nov except TUESDAYS (the next weekday if Tuesday is a holiday). "
  "The opening-day scheme was revised on 1 April 2026",
  "No", "konpira_treasure"),
 ("Konpira-san — Takahashi Yuichi gallery", "Kotohira", "not published",
  "not published",
  "In October, WEEKENDS AND PUBLIC HOLIDAYS ONLY — its summer run ends 30 September. "
  "Under the scheme revised 1 April 2026",
  "No", "konpira_opendays"),
 ("Kanamaru-za kabuki theatre", "Kotohira", "¥500 (JHS/HS ¥300, primary ¥200)",
  "09:00–17:00, last entry 16:30", "Open all year, bar performance days", "No", "kanamaruza"),
 ("Tamamo Park (Takamatsu Castle)", "Takamatsu", "¥300 — UNDER 18 FREE",
  "OCTOBER: west gate 06:00–17:30, east gate 08:30–17:00", "29–31 Dec", "No", "tamamo"),
 ("Shikoku Mura open-air museum", "Yashima, Takamatsu", "¥1,600 (university ¥1,000, JHS/HS ¥600, primary free)",
  "09:30–17:00, reception to 16:30", "TUESDAYS (the next day if Tuesday is a holiday)",
  "No", "shikokumura"),
 ("Yashima summit — museums and shuttle", "Takamatsu", "not published anywhere I could reach",
  "not published", "not published",
  "The official Yashima Navi portal does not publish prices, hours or the shuttle fare — "
  "ring ahead if you plan to go", "yashima_navi"),
 ("Yashima Aquarium", "Yashima, Takamatsu", "CLOSED — do not plan for it",
  "—",
  "SHUT for rebuilding since 7 Apr 2025, reopening spring 2027, so it is closed for this trip. "
  "It trades meanwhile as Ichiba Aquarium at 40-12 Setouchichō, Takamatsu — down by the fish "
  "market near JR Shōwachō, NOT on the Yashima plateau",
  "n/a", "yashima_aq_closed"),
])


BOOKINGS.extend([
 ("Kan-onji — Hearts Shuttle day pass", "Reserve by 17:00 three days before",
  "Reserved passengers get priority; walk-up only if seats are left. Tel 0875-57-1717. "
  "⚠️ Only the spring/summer timetable is published — the AUTUMN diagram goes up around "
  "early September 2026, so re-check it then. It decides whether you can get back from "
  "Chichibugahama after sunset.", "hearts_shuttle"),
 ("Kan-onji — Takaya Shrine shuttle", "CANNOT be reserved — first come, first served",
  "Buy from the machine at the tourism office (道の駅ことひき) from 09:00 on the day, "
  "¥1,000 notes only. 20 seats a departure and it sells out on fine days, so go early.",
  "takaya_shuttle"),
])
