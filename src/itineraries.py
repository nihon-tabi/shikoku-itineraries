"""Single source of truth for both itineraries.

Everything downstream — the .xlsx workbooks, the CSVs and the dashboard — is
generated from this file, so the three can never drift apart again.

Each day:
  date   ISO date
  title  short headline for the day
  do     highlights: what you actually DO. Plain language, no jargon.
  travel how you get there, in words
  watch  things that will break the day if ignored
  sleep  where you sleep that night
  legs   [from, to, dep, arr, method, yen|None]  - the transport table
"""

RATE_NOTE = "Seeded 0.01858 on 16 Aug 2026; B1 refreshes itself via Google Finance."

# ── Things that can strand you ───────────────────────────────────────────────
# A day is not "planned" until the way BACK is known. These are the services
# with no later alternative — miss one and you are sleeping where you stand.
#
# Each carries a STATE, because "I checked and it runs at 17:45" and "nobody
# has published this yet" are different facts and the traveller must be able to
# tell them apart at a glance:
#
#   CONFIRMED    read off the operator's own current timetable, date given
#   UNPUBLISHED  the operator has not issued the timetable for this date yet
#   UNREADABLE   published, but as images/PDF the planner could not extract
#
# Anything not CONFIRMED must say exactly WHAT to check, WHERE, WHO to ring and
# BY WHEN — a warning the traveller cannot act on is just anxiety.

# `links` is what the traveller actually clicks. Pass SOURCES keys so the tier
# travels with the link — the page you must check to clear an UNPUBLISHED row is
# usually the operator's, and knowing that is half the value.
def _S(what, state, detail, check="", who="", by="", fallback="", links=()):
    return dict(what=what, state=state, detail=detail, check=check,
                who=who, by=by, fallback=fallback, links=list(links))


GLOSSARY = [
    ("Manchō / kanchō", "満潮 / 干潮",
     "High tide and low tide. 満 is 'full', 干 is 'dry'. A Japanese tide table (潮見表, "
     "shiomihyō) prints both times for every date.",
     "Four things on this trip are locked to these two numbers, and they are NOT locked "
     "the same way — see the Tides tab. Beware the homophone: 干潮 (low tide) and 観潮 "
     "(whirlpool-viewing) are both KANCHŌ, so a 観潮船 kanchōsen is a whirlpool boat, "
     "nothing to do with low water."),
    ("Ōshio / nakashio / koshio", "大潮 / 中潮 / 小潮",
     "Spring, middle and neap tide — how BIG the day's tide is, which is a separate "
     "thing from whether it is high or low. Spring tides fall around new and full moon "
     "and move the most water; neap tides move the least.",
     "This sets how wide your viewing window is at Naruto: the operator allows ±2 hours "
     "either side of the listed time on a 大潮, ±1.5 on a 中潮 and only ±1 on a 小潮. On "
     "渦の道's calendar 大潮 prints in RED, 中潮 in blue, 小潮 in black."),
    ("Seishun 18 kippu", "青春18きっぷ",
     "A seasonal JR ticket giving 3 or 5 days of unlimited travel on SLOW trains only "
     "(local + rapid), for a flat price. Despite the name it has no age limit.",
     "NOT usable on this trip. It is only sold for fixed seasons — 1 Mar–10 Apr, "
     "18 Jul–8 Sep, 11 Dec–11 Jan — and October falls in none of them. Since a 2024 "
     "rule change the days must also be consecutive and it can no longer be shared."),
    ("Local / futsu", "普通",
     "The all-stations slow train. No surcharge — your basic ticket is the whole price.",
     "This is what you ride almost everywhere. It is the cheap option and the reason "
     "some days are long."),
    ("Limited express / tokkyu", "特急",
     "The fast intercity train. Costs your basic fare PLUS a limited-express surcharge, "
     "often roughly doubling the price.",
     "Avoided throughout, with one exception noted on the Kōchi–Matsuyama day where "
     "no reasonable slow alternative exists."),
    ("IC card", "ICOCA / Suica / PASMO",
     "The tap-to-pay transport smartcards used across Japan.",
     "They work far less than you would expect here. JR Shikoku station gates do not "
     "take them, Kōchi uses its own incompatible card (Iruca), and the Iya buses and "
     "the rabbit-island ferry are cash only. Matsuyama accepts Suica since 2025 and is "
     "the exception. Carry cash and ¥100 coins."),
    ("Wanman", "ワンマン",
     "A one-person-operated train with no conductor. You board at one door, take a "
     "numbered paper ticket, and pay the driver as you get off.",
     "Most Iya-area local trains are these. Have coins ready."),
    ("Kippu", "きっぷ",
     "Ticket. A 'free kippu' (フリーきっぷ) means an unlimited-travel pass, not a free one.",
     "The day passes on Shodoshima, Awaji and in Kōchi are all of this type."),
    ("Ichinichi joshaken", "一日乗車券",
     "A one-day unlimited pass for a given operator's buses/trams.",
     "Three of these carry the trip: Shodoshima's Olive Bus ¥1,600, Awaji's ¥880, and "
     "Hiroshima's Hiroden ¥1,000, which also covers the Miyajima ferry AND the island "
     "visitor tax."),
    ("Koyo / miyoro", "紅葉 / 見頃",
     "Koyo is autumn leaf colour. Miyoro is the 'best viewing' window — distinct from "
     "irozuki-hajime (色づき始め), which just means it has started to turn.",
     "See the Foliage tab. Short version: this trip is a few weeks before nearly "
     "everything except the summit of Mt Tsurugi."),
    ("Onsen", "温泉",
     "Natural hot-spring bath. You wash thoroughly at the taps first, then soak; no "
     "swimwear, no towel in the water.",
     "Dogo Onsen in Matsuyama is one of Japan's oldest and reopened from restoration "
     "in July 2025. Tattoos can be a problem at some baths — Hotel Candeo in Matsuyama "
     "explicitly allows them if covered."),
    ("Ryokan / minshuku / guesthouse", "旅館 / 民宿",
     "Ryokan is a traditional inn, usually with dinner and breakfast included. Minshuku "
     "is the cheaper family-run version. Guesthouses are the backpacker tier.",
     "Iya's only in-valley options are expensive ryokan (~¥20,000pp with dinner) or a "
     "campsite — which is why this plan sleeps in Awa-Ikeda instead."),
    ("Takkyubin", "宅急便",
     "Same-day/next-day luggage courier between hotels, stations and convenience stores.",
     "The standard fix for the long transfer days. Several travellers shipped their big "
     "bag ahead and rode with a daypack, roughly ¥1,400 a bag."),
    ("Michi-no-eki", "道の駅",
     "A roadside station — toilets, local food, produce, often a viewpoint.",
     "Michi-no-eki Ōboke is a signed bus stop and a decent lunch stop. ⚠️ ORIENTATION: "
     "it is in the Iya/Ōboke gorge in WESTERN Tokushima prefecture, about 72 km west "
     "of Tokushima CITY, which sits on the east coast. Awa-Ikeda, Ōboke and the vine "
     "bridges are all in that western cluster — so the michi-no-eki belongs with the "
     "Awa-Ikeda nights, not with the Tokushima city day."),
    ("Shotengai", "商店街",
     "A covered shopping arcade, usually the town's main eating-and-browsing street.",
     "Takamatsu's is one of the longest in Japan; Kōchi's leads to the Sunday market."),
    ("Henro", "遍路",
     "A pilgrim walking the 88-temple Shikoku circuit, in white vest and conical hat.",
     "You will see them constantly. Temples 1–5 near Tokushima are a flat, signposted "
     "walk if you want a taste without committing to 1,200 km."),
    ("Kaisoku / Shin-Kaisoku", "快速 / 新快速",
     "Rapid and Special Rapid services. They skip stations but charge NO surcharge.",
     "The Shin-Kaisoku is how you get Osaka→Himeji in about an hour for ¥1,460 — same "
     "price as the slow train, less than half the time."),
]

FOLIAGE = [
    ("Mt Tsurugi summit", "1,955 m", "25 Oct", "1 Nov", "12 Nov",
     "ON TIME (just)", "The only real koyo destination in your window. You arrive as "
     "the summit starts; true peak is the last week of October."),
    ("Iya-kei gorge", "403 m", "late Oct", "—", "mid Nov",
     "MARGINAL", "Only the very start, and only if you are there after ~27 Oct."),
    ("Kankakei, Shodoshima", "250–816 m", "20 Nov", "27 Nov", "8 Dec",
     "TOO EARLY", "The summit begins ~24 Oct; the gorge as a whole peaks a month after "
     "you leave. Operator reports put full colour at 17–20 Nov three years running."),
    ("Miyajima Momijidani", "~50 m", "21 Nov", "26 Nov", "3 Dec",
     "TOO EARLY", "Recorded COMPLETELY GREEN on 12 October 2025 in n-kishou's own "
     "observation feed. You are about six weeks early."),
    ("Koko-en, Himeji", "~15 m", "27 Nov", "30 Nov", "5 Dec",
     "TOO EARLY", "Observed 25 Nov–1 Dec in 2024. Go for the garden itself, not the leaves."),
    ("Ritsurin Garden", "~10 m", "28 Nov", "3 Dec", "10 Dec",
     "TOO EARLY", "The biggest miss on the route. Still worth the visit — it is widely "
     "called the finest garden in Japan regardless of season."),
    ("Matsuyama Castle", "~130 m", "4 Dec", "7 Dec", "12 Dec",
     "TOO EARLY", "The latest-peaking spot on the whole list, about six weeks out."),
    ("Kōsanji, Shimanami", "lowland", "26 Nov", "1 Dec", "9 Dec",
     "TOO EARLY", "Representative of Onomichi and the islands generally."),
    ("Nakatsu-keikoku, Kōchi", "lowland", "24 Nov", "27 Nov", "2 Dec",
     "TOO EARLY", "Kōchi city's own kaede forecast was 13 Dec in 2025."),
]

# ─────────────────────────────────────────────────────────────────────────────
# DAY ALTERNATIVES — a day that can be spent more than one way.
#
# The Matsuyama free day is the clearest case: the castle is a half-day at most,
# and travellers who had seen the rest of Shikoku kept naming Uchiko and Ōzu
# instead. Rather than bury that in a "you could also…" line, the day carries
# real alternatives and the traveller picks one — in the dashboard with a switch
# on the day itself, in the workbook on the "Day alternatives" tab.
#
# Shape:  alt_label  names the DEFAULT plan (alternative 0)
#         alts       lists the others, each a full replacement for the day

NAGORO_ALT = dict(label="Nagoro's scarecrows and the double vine bridges instead",
  do=["NAGORO, the scarecrow village — a hamlet where one resident has made life-size straw "
      "figures of every neighbour who died or moved away. They sit at the bus stops, in the "
      "schoolroom, in the fields. Roughly 300 of them and around 20 living people. Strange "
      "and quietly moving, and unlike anything else on this trip.",
      "THE OKU-IYA DOUBLE VINE BRIDGES — the 'husband and wife' pair, with a hand-hauled "
      "cable cart slung across the river beside them. Smaller, older-feeling and far quieter "
      "than the famous Kazurabashi.",
      "This is the deep-valley day WITHOUT the mountain. You trade a 1,955 m summit for two "
      "places almost no visitor without a car ever reaches — and you get three unhurried "
      "hours at Nagoro instead of a chairlift and a bus chase."],
  flow=[
   ("10:16 → 10:20", "Arrive 久保 Kubo and change straight onto the Miyoshi City 名頃線. Four "
    "minutes — do not wander."),
   ("10:45", "Off at 名頃 Nagoro (¥230 from Kubo). You have until 13:43, which sounds like a "
    "lot and is roughly right: the village is small but you will not want to hurry it."),
   ("13:43 → 13:50", "The next uphill bus takes you seven minutes further to 二重かずら橋, the "
    "double bridges (¥430 from Kubo)."),
   ("13:50 – 15:13", "The double bridges and the cable cart. About an hour and a half, which "
    "is the right amount."),
   ("15:13 → 15:45", "The LAST bus down, through Nagoro again, to 久保 Kubo."),
   ("16:44 → 18:07", "Kubo → かずら橋夢舞台 17:30, then the 17:41 — the last bus out of the "
    "valley — to 大歩危駅前, and the 18:19 train home."),
  ],
  travel="The same chain as far as Kubo, then the Miyoshi City 名頃線 up the Higashi-Iya road. "
         "Every one of these times is off the operator's own connection sheet.",
  watch=["⚠️ THIS IS WHY YOU CANNOT ALSO DO MT TSURUGI. The 13:50 bus does continue to 剣山, "
         "arriving 14:08 — but the last bus down is 14:55. That is 47 minutes on the "
         "mountain, and the chairlift alone is 30 minutes return. It does not fit, and the "
         "penalty for trying is being stranded at 1,420 m.",
         "⚠️ SEASONAL, AND YOU ARE INSIDE IT BY DAYS. The 二重かずら橋 stop runs daily only "
         "1 Oct–3 Nov (otherwise weekends and holidays from 4 Apr, ending 23 Nov). The 剣山 "
         "stop has the same daily window.",
         "The double bridges charge admission; the hand-hauled cable cart is included.",
         "Cash only, and there is nothing up there to break a note with.",
         "If anything slips, the 15:13 is the last way down. There is no later service and "
         "no taxi."],
  legs=[("Awa-Ikeda","Ōboke","07:45","08:14","JR Dosan Line local train",530),
        ("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line",670),
        ("かずら橋夢舞台 Kazurabashi Yumebutai","久保 Kubo","09:30","10:16","Shikoku Kotsu, Higashi-Iya line",750),
        ("久保 Kubo","名頃 Nagoro (かかしの里)","10:20","10:45","Miyoshi City bus, 名頃線 — daily 1 Oct–3 Nov only",230),
        ("名頃 Nagoro","二重かずら橋 Oku-Iya double bridges","13:43","13:50","Miyoshi City bus, 名頃線 (¥430 from Kubo)",430),
        ("二重かずら橋 Oku-Iya double bridges","久保 Kubo","15:13","15:45","Miyoshi City bus, 名頃線 — LAST down of the day",430),
        ("久保 Kubo","かずら橋夢舞台 Kazurabashi Yumebutai","16:44","17:30","Shikoku Kotsu, Higashi-Iya line",750),
        ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","17:41","18:07","Shikoku Kotsu — LAST BUS of the day",670),
        ("Ōboke","Awa-Ikeda","18:19","+~30 min","JR Dosan Line local train",530)])

# ─────────────────────────────────────────────────────────────────────────────
# SHARED DAY FLOWS — days that recur across options, defined once.
#
# A flow means the ORDER IS FORCED: by a tide, a ferry, a last ascent, a bus
# that runs four times, or the light. Days that are genuinely pick-your-own
# (a city with frequent trams, a museum afternoon) deliberately have none.

RABBIT_FLOW = [
 ("BEFORE you board",
  "BUY THE RABBIT FOOD. None is sold on the island — this is the single thing that ruins "
  "the visit if you get it wrong. About ¥200 at the shop by 忠海 Tadanoumi station, open "
  "07:00–19:45. Buy PELLETS, not vegetables: the island's own rules say leftover veg spoils "
  "and draws crows that prey on the kits."),
 ("at the port",
  "BAG STORAGE, ¥500 a bag, at 忠海港 Tadanoumi Port. You do not want a backpack while a "
  "hundred rabbits climb you. ⚠️ THE FERRY IS CASH ONLY."),
 ("every 30–45 min",
  "THE FIFTEEN-MINUTE CROSSING to 大久野島 Ōkunoshima."),
 ("allow 4–5 hours",
  "THE ISLAND. Around a thousand feral rabbits that will run at you en masse the moment you "
  "sit down. The other half of the island is its history: it made poison gas for the "
  "Imperial Army and was erased from maps. The museum is unflinching and costs ¥150. Ruined "
  "batteries and a power plant stand in the woods. ⚠️ A couple who budgeted three hours "
  "ended up running for the boat."),
 ("do not",
  "PICK THE RABBITS UP. They panic and break bones, and there is no vet on the island."),
 ("last out 18:30",
  "THE LAST FERRY BACK. Check it against your own date before you settle in with the "
  "rabbits — it is the one hard edge of the day."),
]

MIYAJIMA_FLOW = [
 ("check the tide FIRST",
  "THE OCTOBER TIDE TABLE — https://www.miyajima.or.jp/sio/sio10.html — decides the shape of "
  "the day. BELOW 100 cm you can walk out across the seabed to the great gate; ABOVE 250 cm "
  "it appears to float. The water turns over about six hours, so with a bit of planning you "
  "can see both in one day, which is the thing to aim for."),
 ("buy at the tram stop",
  "THE HIRODEN ¥1,000 DAY PASS. It covers every city tram, the ferry, AND the ¥100 island "
  "visitor tax, and it cuts the ropeway from ¥2,000 to ¥1,500. It pays for itself before "
  "lunch."),
 ("9:10–16:10 only",
  "TAKE THE JR FERRY OUT in that window and it detours close past the torii at no extra "
  "cost and no extra time. Outside it, you get the ordinary crossing."),
 ("morning",
  "ITSUKUSHIMA SHRINE, on stilts over the water since the 12th century. ¥300. ⚠️ HOURS "
  "CHANGE ON 15 OCTOBER: 06:30–18:00 until the 14th, 06:30–17:30 from the 15th."),
 ("last ascent 16:00",
  "THE ROPEWAY UP MT MISEN for the Inland Sea panorama. ⚠️ 16:00 IS THE LAST ASCENT and it "
  "is not negotiable. The observatory at the top station is enough; the summit is a further "
  "~30 minutes up a steep stepped trail — see the Walks tab before you decide. ⚠️ The "
  "Reikadō hall with its 1,200-year flame burned down in May 2026 and is gone."),
 ("on the way down",
  "DAISHŌ-IN, the temple complex on the slope — free, 08:00–17:00, and the best thing on "
  "the island that nobody queues for. Then the deer, and momiji manjū made in front of you "
  "along the main street."),
 ("late afternoon",
  "THE GATE AGAIN, at the other end of the tide. Momijidani — literally 'maple valley' — "
  "was recorded completely green on 12 October 2025, so go for the walk, not the leaves."),
]

SHIMANAMI_BUS_FLOW = [
 ("~1 per hour",
  "LOCAL TRAIN UP THE COAST to 今治 Imabari, 71 minutes on the Yosan Line."),
 ("hourly",
  "THE SHIMANAMI LINER as far as 因島大橋 Innoshima Ōhashi. ⚠️ THERE IS NO DIRECT "
  "IMABARI–ONOMICHI BUS — that route was abolished in 2005. You change here, and the "
  "operator itself warns the connection 'may not be smooth'. Build in slack and do not plan "
  "anything tight at the far end."),
 ("the second bus",
  "ON TO ONOMICHI. Six islands and seven of the most elegant suspension bridges in the "
  "world go past the window; even from a bus seat this is one of Japan's great scenic "
  "routes."),
 ("on arrival",
  "ONOMICHI — a steep temple town of alleys and cats above a working shipping strait. The "
  "Path of Literature, cat alley, and ramen. ⚠️ If you are carrying a rented bike, it "
  "CANNOT go on the bus unless it is bagged; the service that took assembled bikes ended in "
  "June 2020."),
]

MATSUYAMA_ALTS = [
dict(label="Uchiko and Ōzu — two quiet old towns",
 do=["UCHIKO — a merchant town that got rich on wax, with a preserved street of "
     "ochre-plastered townhouses and the UCHIKO-ZA, a 1916 wooden playhouse you can walk "
     "into, revolving stage and all.",
     "ŌZU — a castle town on a river bend, rebuilt in wood in 2004 using the original "
     "techniques rather than concrete, which is rare and you can tell.",
     "Both are small, flat and quiet. This is the day for wandering rather than ticking "
     "things off — one traveller who had seen the whole island named these two the best "
     "thing in Ehime."],
 travel="Local trains down the Yosan Line, both towns on the same line, and back. Uchiko "
        "first (further), then Ōzu on the way home, so you finish closer to Matsuyama.",
 watch=["⚠️ Smaller stations here have PHYSICAL departure boards only — no screens, no "
        "announcements you will follow. One traveller missed a train at Ōzu because of "
        "exactly this. Photograph the board when you arrive.",
        "Trains are roughly hourly. Check the return before you settle into lunch.",
        "This costs a day of trains rather than admissions — the towns themselves are free "
        "to walk."],
 legs=[("Matsuyama","Uchiko","roughly hourly","not published","JR Yosan Line local train",None),
       ("Uchiko","Iyo-Ōzu","roughly hourly","not published","JR Yosan Line local train",None),
       ("Iyo-Ōzu","Matsuyama","roughly hourly","not published","JR Yosan Line local train",None)]),

dict(label="The Iyonada coast and Shimonada station",
 do=["The old coastal branch of the Yosan Line, which runs right along the water — the "
     "scenic alternative to the inland main line.",
     "SHIMONADA STATION: a single platform with the Inland Sea directly behind it and "
     "nothing else. One of the most photographed stations in Japan.",
     "Iyo-Ōzu on the loop back."],
 travel="Down the coastal branch, out at Shimonada, then round via Iyo-Ōzu and back — about "
        "2 h 15 of riding, 104 km.",
 watch=["⚠️ READ THIS BEFORE CHOOSING IT. Shimonada gets ONE train per hour in one "
        "direction. Get it wrong and you are on an unstaffed platform for two hours. "
        "Multiple travellers reported exactly that, one of them freezing.",
        "⚠️ It is also crowded — it is famous, and it is one small platform. A 2026 "
        "traveller wrote: “I could not stop at Shimonada station itself… I would recommend "
        "skipping this, when planning I was too impressed by the photos on Google Maps.”",
        "The ride itself is the point. If you only want the view, stay on the train.",
        "¥2,470 for the loop without a pass."],
 legs=[("Matsuyama","Shimonada and round via Iyo-Ōzu","1 train/hour in one direction","2 h 15 riding, 104 km","JR Yosan Line coastal branch, all local",2470)]),
]

# ─────────────────────────────────────────────────────────────────────────────

A = dict(
    key="A",
    name="Option A — Himeji, Shodoshima, then down through Shikoku",
    verdict=("Cleanest logistics. Shodoshima sits naturally on the way in, the ferry "
             "chain works, nothing backtracks, and you get Kōchi's Sunday market. "
             "Slightly dearer than B because of the Himeji ferry and the Kōchi bus."),
    days=[
dict(date="2026-10-09", title="Osaka → Himeji Castle and Koko-en → Shodoshima",
 flow=[
  ("every 15 min", "THE SHIN-KAISOKU TO HIMEJI — an hour, and it costs the same ¥1,460 as the "
   "slow train for less than half the time. Bags straight into the North Exit lockers "
   "(¥400–¥700, IC cards accepted, open 24 h): everything today is on foot or on a bus."),
  ("09:00–11:00", "HIMEJI CASTLE from opening. The finest surviving castle in Japan — white "
   "plaster, six storeys, never bombed and never burned. Go early: the keep is capped at "
   "1,000 entries an hour and the queue builds. ⚠️ Six floors of steep ladder-stairs climbed "
   "in socks; the grounds are the flat part and skipping the interior is completely fine."),
  ("11:00–12:00", "KOKO-EN next door — nine walled Edo gardens on the old samurai residences, "
   "a carp pond, a bamboo grove, a tea house, and a flat gravel circuit that is exactly the "
   "counterweight you want after the castle stairs. The combined ticket makes it ¥100."),
  ("~2 per hour", "SHINKI BUS 94 from JR Himeji North Exit, PLATFORM 1, to 姫路港 Himeji Port. "
   "20–30 minutes. Collect the bags on the way."),
  ("13:35 → 15:15", "THE FERRY east across the Inland Sea to 福田港 Fukuda on Shodoshima's "
   "wild coast."),
  ("15:25 → 15:47", "⚠️ THE TIGHTEST CONNECTION OF THE TRIP: ten minutes from boat to bus. "
   "Miss it and the next is 2 h 20 away, at a port with no town and no taxi rank. Off at "
   "安田上 Yasuda-kami, five minutes' walk from the inn."),
  ("to 17:00", "YAMAROKU SOY SAUCE if you are quick — free, no reservation, cedar barrels two "
   "storeys high. ✅ And if you miss it, it does not matter: it is three minutes from your "
   "inn and opens at 09:00, so it moves to tomorrow morning. Do NOT rush the bus for it."),
 ],
 do=["HIMEJI CASTLE — the finest surviving castle in Japan and the whole reason to stop "
     "here. White plaster, six storeys, never bombed and never burned. Give it a proper "
     "two hours from opening.",
     "KOKO-EN next door — nine walled Edo gardens on the site of the old samurai residences: "
     "a carp pond, a bamboo grove, a tea house, and a flat gravel circuit that is exactly "
     "the counterweight you want after the castle stairs. Reckon on an hour.",
     "Then the ferry east across the Inland Sea, landing at Fukuda on Shodoshima's wild "
     "coast as the light goes.",
     "YAMAROKU SOY SAUCE at Yasuda, if you're quick — a working brewery you walk straight "
     "into, free, no reservation, open until 17:00. Cedar barrels two storeys high and over "
     "a century old, furred with the wild yeast that makes the flavour. One of the last "
     "places in Japan still doing it this way."],
 travel="Rapid train to Himeji (an hour, no surcharge). Bags into the station lockers, castle "
        "and garden all morning, city bus to the port, then the 13:35 ferry. One bus 22 "
        "minutes down the coast from Fukuda and you're five minutes' walk from the inn.",
 watch=["Reaching Yasuda at 15:47 still leaves Yamaroku, which is open to 17:00 and free. "
        "That is the one soy-sauce stop worth making — a working brewery beats a museum.",
        "✅ AND IF YOU DON'T MAKE IT, IT DOESN'T MATTER. Yamaroku is 3 minutes from your "
        "inn and opens at 09:00, so it moves to tomorrow morning at no cost — see "
        "tomorrow's first line. Do NOT rush the ferry or the bus connection for it.",
        "The Fukuda ferry-to-bus connection is 10 minutes. Miss it and the next bus is 2h20 "
        "away, at a port with no town and no taxi rank.",
        "The castle keep is six floors of steep ladder-stairs, climbed in socks. The grounds "
        "and Koko-en are the flat part — skipping the interior is completely fine.",
        "Admission rose to ¥2,500 in March 2026; most blogs still say ¥1,000. The combined "
        "castle + Koko-en ticket is ¥2,600, so the garden effectively costs ¥100.",
        "JR Himeji North Exit lockers take IC cards and are open 24 h — ¥400 to ¥700."],
 sleep="Yasuda, Shodoshima — Hirokiya Ryokan (¥3,300 room-only; free port pick-up if you phone)",
 legs=[("Osaka","Himeji","every 15 min","+1h03–06","JR Shin-Kaisoku (rapid, no surcharge)",1460),
       ("JR Himeji Stn, North Exit Platform 1","Himeji Port","~2 per hour","+20–30 min","Shinki Bus route 94",320),
       ("Himeji Port","Fukuda Port, Shodoshima","13:35","15:15","Shodoshima Ferry (7 sailings/day)",2100),
       ("Fukuda Port","Yasuda-kami (安田上)","15:25","15:47","Olive Bus, South Fukuda Line",500)]),

dict(date="2026-10-10", title="Kankakei Gorge, somen by hand, and the vine-thin noodles",
 flow=[
  ("09:32 → 09:41", "Leave the bags at the inn. 安田上 Yasuda-kami to 草壁港 Kusakabe Port on "
   "the Olive Bus South Fukuda line."),
  ("09:50 → 10:02", "THE FREE TOWN SHUTTLE up to 紅雲亭 Kouuntei, the ropeway base. Eight runs "
   "a day, EVERY day in October — and none at all through November."),
  ("10:05 – 11:35", "KANKAKEI GORGE. Five minutes of cable car over red rock spires with the "
   "Inland Sea opening out behind you. ¥2,340 return, cars every 12 minutes. ⚠️ It rises to "
   "¥2,700 on 1 November. Foliage here peaks 27 November — you are seven weeks early."),
  ("11:40 → 12:09", "Shuttle down at 11:40, then the 12:02 Olive Bus back east to 安田 Yasuda."),
  ("12:30 – 13:15", "NAKABU-AN, the somen workshop you booked yesterday, a hundred metres from "
   "where you slept. You do the 箸分け step yourself — dough stretched between two chopsticks "
   "until it becomes hair-thin noodles — then eat what you made. 45 min, ¥1,200. Their "
   "nama-somen, the fresh un-dried kind, is from ¥750 and is essentially island-only."),
  ("13:20 – 14:10", "YAMAROKU SOY SAUCE, three minutes away, if you did not manage it last "
   "night. Free, open to 17:00, no reservation."),
  ("14:16 → 14:48", "Collect the bags, then the westbound bus to 土庄港 Tonoshō. Its Yasuda "
   "departure is not published separately; it passes Kusakabe at 14:16."),
  ("dusk", "ANGEL ROAD if the tide is out — but tomorrow morning is the proper window, so "
   "treat tonight as a bonus rather than the plan."),
 ],
 book=["☎ NAKABU-AN — phone 0879-82-3669 THE DAY BEFORE. There is no online booking and "
       "no walk-up. If you are not comfortable phoning in Japanese, ASK YOUR INN TO RING "
       "FOR YOU — Hirokiya is 3 minutes away and this is an ordinary favour to ask; "
       "Japanese accommodation does it routinely. Do it when you check in.",
       "CLOSED Tue/Wed/Thu except public holidays. 10 Oct 2026 is a Saturday, so it is "
       "open — but if your dates move, re-check before anything else in this day."],
 do=["KANKAKEI GORGE first thing, while the light is good — one of Japan's three great "
     "gorges, a five-minute cable ride over red rock spires with the Inland Sea opening out "
     "behind you.",
     "MAKING SOMEN AT NAKABU-AN, a hundred metres from where you slept. Shodoshima is one of "
     "Japan's three great somen regions, and here you do the 箸分け step yourself: dough "
     "stretched between two chopsticks until it becomes hair-thin noodles. 45 minutes, "
     "¥1,200, and you eat what you made.",
     "Their restaurant does NAMA-SOMEN — fresh, un-dried somen you can essentially only eat "
     "on this island. From ¥750.",
     "IF YOU MISSED YAMAROKU YESTERDAY, GO THIS MORNING INSTEAD — it is 3 minutes' walk "
     "from where you slept and opens at 09:00. Swap it with Kankakei: do the brewery "
     "first, take the 10:32 bus instead of the 09:32, and you still make the somen "
     "session. Nothing else in the day moves.",
     "Then west to Tonoshō with the afternoon free — and Angel Road at dusk if the tide "
     "is out."],
 travel="Leave your bags at the inn. The 09:32 bus to Kusakabe, the 09:50 free shuttle up to "
        "the ropeway, the 11:40 shuttle back down, the 12:02 bus back to Yasuda for the 12:30 "
        "somen session, collect the bags there, then the westbound bus that passes Kusakabe "
        "at 14:16 through to Tonoshō by 14:48. Six moves, all of them published — this is a "
        "day where being on the right bus matters.",
 watch=["BOOK NAKABU-AN THE DAY BEFORE — phone 0879-82-3669. CLOSED Tue/Wed/Thu except public "
        "holidays. Today is a Saturday, so you're fine; if the trip shifts, re-check.",
        "The Kankakei shuttle is a FREE town bus, 8 runs a day, running EVERY day in October. "
        "It stops completely for the whole of November.",
        "Don't buy the ¥1,600 Olive Bus day pass — today's singles come to about ¥1,200.",
        "Foliage here peaks 27 November; you're about seven weeks early.",
        "10–12 Oct is a three-day weekend (Sports Day), so buses will be fuller.",
        "💡 WORTH CONSIDERING, NOT REQUIRED: the island convenience stores run takkyubin "
        "(宅急便, Yamato/Kuroneko). Sending the big bags from Yasuda straight to your "
        "Takamatsu hostel — roughly ¥1,400 a bag, next day — turns the next two days into "
        "daypack days across two ferries and a garden. Only worth it if carrying packs "
        "onto buses sounds miserable; the day works fine without it."],
 sleep="Tonoshō, Shodoshima",
 legs=[("Yasuda-kami (安田上)","Kusakabe Port","09:32","09:41","Olive Bus, South Fukuda Line",200),
       ("Kusakabe Port","Kouuntei (ropeway base)","09:50","10:02","FREE town shuttle, 12 min",0),
       ("Kankakei base","Summit and back","every 12 min","~5 min each way","Ropeway (rises to ¥2,700 on 1 Nov)",2340),
       ("Kouuntei","Kusakabe Port","11:40","11:52","FREE town shuttle, 12 min",0),
       ("Kusakabe Port","Yasuda (安田)","12:02","12:09","Olive Bus, Sakate Line",200),
       ("Yasuda (安田)","Tonoshō Port","not published for Yasuda — the up-bus passes Kusakabe at 14:16","14:48","Olive Bus, Sakate Line",500)]),

dict(date="2026-10-11", title="Angel Road at dawn, then across to Takamatsu",
 do=["Angel Road, the Shikoku Ferry crossing, and Ritsurin Garden in the afternoon."],
 flow=[
  ("before 08:25",
   "ANGEL ROAD, AND IT HAS TO BE THIS MORNING. The operator's own tide table "
   "(https://www.shikokuferry.com/angel — check your own date) gives today's "
   "windows as 02:25–08:25 and 14:47–20:47 — so the walkable daylight window closes at "
   "08:25 and the next one does not open until the afternoon, by which time you need to be "
   "on a boat. Walk out from Tonoshō at first light; it is about half an hour on foot from "
   "the port, faster than waiting for one of the five daily buses. The sandbar surfaces "
   "and links four islets; couples leave notes on shells. Free."),
  ("mid-morning",
   "THE CAR FERRY to Takamatsu, an hour across the Inland Sea and a sightseeing trip in "
   "itself. Take the ¥700 car ferry, not the ¥1,400 high-speed boat — it is 25 minutes "
   "slower and the deck is the point."),
  ("afternoon",
   "RITSURIN GARDEN with the whole afternoon for it. 300 years old, six ponds, thirteen "
   "landscaped hills and a forested mountain borrowed as the backdrop. ¥500, open to 17:30 "
   "in October, flat paths throughout. Every trip report I read named it the best thing in "
   "Takamatsu; one called it the finest garden in Japan. Allow two hours minimum — one "
   "visitor said two “was not quite enough”."),
  ("evening",
   "SANUKI UDON, and the shotengai arcade — among the longest covered shopping streets in "
   "Japan. Kagawa is the udon prefecture and the self-serve counters are often under ¥400."),
 ],
 travel="Half an hour on foot to the sandbar and back, then the mid-morning ferry, then "
        "seven minutes on the Kotoden out to the garden.",
 watch=["⚠️ TODAY'S WINDOWS ARE 02:25–08:25 AND 14:47–20:47, from the ferry operator's own "
        "table. That is why the day starts early. Re-check before you go — the table is "
        "published per date and weather shifts it.",
        "Takamatsu goes quiet early: travellers describe it as 'virtually dead' by 21:30. "
        "Eat before 20:00.",
        "Ritsurin's own foliage peaks 3 December. You will see it green — go anyway."],
 strand=[
  _S("The last ferry between Shodoshima and Takamatsu",
     "CONFIRMED",
     "Shikoku Ferry's own timetable, 15 sailings each way, 60 minutes, ¥700. LAST 土庄発 "
     "20:10 → 高松 21:10; last 高松発 20:20 → 土庄 21:20. ⚠️ AND A TRAP: on WEEKDAYS the "
     "土庄発 19:30 and the 高松発 15:10 are 危険物搭載車両の航送指定便 — hazardous-cargo sailings "
     "ORDINARY PASSENGERS CANNOT BOARD. On a weekday the real gap before the last boat is "
     "18:40 → 20:10.",
     check="Confirm both directions on the route page; the operator warns diagrams change "
           "for engine maintenance.",
     who="Shikoku Ferry — ask at the Takamatsu or Tonoshō 乗り場",
     by="Before you set out that morning.",
     fallback="A separate 高速艇 also works this route on its own timetable. Otherwise it is "
              "a night on Shodoshima.",
     links=["sf_takamatsu"]),
 ],
 sleep="Takamatsu — WeBase hostel, Kawaramachi",
 legs=[("Tonoshō Port","Takamatsu Port","15/day, last 20:10 → 21:10","+60 min","Shikoku Ferry (car ferry)",700),
       ("Takamatsu","Ritsurin Kōen","every 15 min","+7 min","Kotoden to Ritsurin-kōen — RAISED to ¥250 on 1 Oct 2026 (JR is ¥240)",250)]),

dict(date="2026-10-12", title="The Gate in the Sky, the sand coin, and a mirror beach",
 do=["Takaya Shrine's hilltop torii, the Zenigata sand coin, and Chichibugahama at sunset."],
 flow=[
  ("09:00, before anything else",
   "BUY THE SHUTTLE TICKETS. The machine is inside 道の駅ことひき at the tourism office and "
   "it opens at 09:00 — ¥1,000 NOTES ONLY, 20 seats a departure, and it sells out on fine "
   "days. You cannot buy at the bus stop and you cannot reserve. This is the single thing "
   "that decides whether today happens."),
  ("10:13 from Takamatsu",
   "THE DIRECT RAPID WEST to Kan-onji, :13 past the hour, no surcharge, about 1h05. Then a "
   "20-minute walk to the shuttle stop at 有明グラウンド, inside Kotohiki Park."),
  ("12:00 up, 13:30 down",
   "TAKAYA SHRINE — the 天空の鳥居, a vermilion torii alone on the 404 m summit of "
   "Inazumiyama with nothing behind it but the Inland Sea, so from the steps below it frames "
   "sky and water and nothing else. ⚠️ Mind the gaps: no 12:30 or 15:00 going up, no 13:00 "
   "or 15:30 coming down. The gate is 150–200 m of steep slope above where the bus drops "
   "you. Thirty to forty minutes at the top is plenty."),
  ("~14:00, same park",
   "ZENIGATA SUNAE — a 122-metre Edo coin raked into the sand of Kotohiki Park and re-raked "
   "by the town since 1633. Free, open 24 hours, floodlit until 22:00, and a few minutes' "
   "walk from where the shuttle drops you back."),
  ("16:00–17:45",
   "CHICHIBUGAHAMA for the mirror. The official per-date calendar is at "
   "https://www.mitoyo-kanko.com/chichibugahama/ — look up your own day before you commit. A flat tidal beach that holds a film of water once the "
   "tide drops, turning the whole strand into a reflection. Today's published window is "
   "16:00–17:45 with sunset at 17:36 — which is as good as this month gets, and it is why "
   "the day is built backwards from here. Free. Get there before the light goes soft."),
  ("after dark",
   "BACK TO TAKAMATSU. ⚠️ This is the weak point of the day — see the warnings."),
 ],
 travel="One rapid train west, a 20-minute walk, the shuttle up the mountain and back, then "
        "the Hearts Shuttle along the coast to the beach and back to the train.",
 watch=["⭐ THIS DAY ONLY WORKS TODAY. The Takaya shuttle runs Saturdays, Sundays and public "
        "holidays ONLY — today is Sports Day. On a weekday the alternatives are a ¥3,600 "
        "taxi each way or a 50-minute climb of 350 vertical metres.",
        "⭐ And 12 October is one of only three days this month when the shuttle runs AND the "
        "beach has a mirror window lasting to sunset (the others are the 10th and 11th). "
        "14–17 October has no window at all.",
        "⚠️ GETTING BACK AFTER SUNSET IS THE WEAK POINT, AND IT HAS NO BACKUP. The Hearts "
        "Shuttle's summer diagram ran a final 19:22 Chichibugahama → 19:48 Kan-onji, but "
        "the AUTUMN timetable is still not published (checked 25 Aug 2026; the operator "
        "site still shows the 春・夏ダイヤ). RING 三豊市観光交流局 on 0875-56-5880 in early "
        "September and get the last run in writing before you commit to this day.",
        "⚠️ AND TODAY IS A PUBLIC HOLIDAY, WHICH KILLS EVERY OTHER WAY BACK. The 'mobi' "
        "shared-ride service that used to run here until 22:00 was WITHDRAWN on 31 May "
        "2025 and no longer exists. The 三豊市 community bus does not run on Sundays or "
        "holidays. The 讃･瀬戸シャトルタクシー is weekday-only and must be booked by 10:00 "
        "on the day. So on 12 October the Hearts Shuttle is the ONLY scheduled way off "
        "that beach after dark — everything else is a taxi you arrange yourself. The last "
        "local back to Takamatsu leaves Kan-onji at 22:34.",
        "The ¥2,400 Shikoku Saihakken day pass is valid today (Sat/holiday only, slow trains "
        "only, bought the day before) and covers both JR legs — but those come to ¥2,480, so "
        "it saves ¥80. Buy singles unless you add another trip."],
 strand=[
  _S("Hearts Shuttle — the ONLY scheduled way off Chichibugahama after dark",
     "UNPUBLISHED",
     "The spring/summer diagram ran a final 19:22 Chichibugahama → 19:48 Kan-onji. The "
     "AUTUMN diagram replaces it and is not out: re-checked 25 August 2026 and the "
     "operator page still shows the 春・夏ダイヤ.",
     check="ONLINE FIRST, NO CALL NEEDED — open the operator page below and look for a "
           "秋ダイヤ / 秋・冬ダイヤ link replacing the 春・夏ダイヤ. Read the LAST Chichibugahama "
           "departure and its Kan-onji arrival. The page is Japanese but the times are "
           "digits, and browser translation handles the rest. Look again a few days before "
           "you fly, in case it moved.",
     who="ONLY IF THE PAGE IS STILL BLANK: your Takamatsu accommodation will ring "
         "三豊中央観光 0875-57-1717 (who also take the booking) or 三豊市観光交流局 "
         "0875-56-5880 for you. Front desks do this constantly — write the question on "
         "paper and hand it over rather than phoning yourself.",
     by="Watch the page from early September 2026, then reserve the pass by 17:00 THREE "
        "DAYS before you go.",
     fallback="NONE on a public holiday. 'mobi' was withdrawn 31 May 2025; the 三豊市 "
              "community bus does not run Sundays or holidays; the 讃･瀬戸シャトルタクシー is "
              "weekday-only. It is the Hearts Shuttle or a taxi you arrange yourself. "
              "Last local Kan-onji → Takamatsu is 22:34.",
     links=["hearts_shuttle", "chichibu"]),
  _S("Takaya Shrine shuttle — the only way up and down without a 350 m climb",
     "UNPUBLISHED",
     "Runs Saturdays, Sundays and public holidays, 10:00–18:30. October's timetable is "
     "NOT yet published — the city page (updated 17 Aug 2026) carries August and "
     "September only, so the 12:00-up / 13:30-down times in this plan come from an "
     "earlier month and may move.",
     check="ONLINE, AND EASY — the city page below lists one PDF per month (令和8年8月, "
           "令和8年9月 …). Wait for 令和8年10月 to appear, open it, read the last descent. The "
           "times are digits; no Japanese needed. Check the same page for a 運休 notice on "
           "your date — 27 September 2026 was cancelled outright for a triathlon, so it "
           "does happen. (The 'ページ番号 0048814' on that page is the city's permanent page "
           "ID — search it on their site if the link ever breaks.)",
     who="ONLY IF THE OCTOBER PDF NEVER APPEARS: your accommodation can ring "
         "（一社）観音寺市観光協会, 観音寺市有明町3-37 — the ticket machine sits inside their "
         "office, so they know the times.",
     by="Watch the page from early September; the tickets themselves cannot be reserved.",
     fallback="Tickets sell out on fine days — go at 09:00 when the machine opens, "
              "¥1,000 NOTES ONLY. If the shuttle is cancelled for weather (気象警報), the "
              "alternatives are a ¥3,600 taxi each way or a 50-minute climb of 350 "
              "vertical metres.",
     links=["takaya_shuttle", "takaya_mitoyo"]),
 ],
 sleep="Takamatsu — WeBase hostel",
 legs=[("Takamatsu","Kan-onji","10:13 (direct rapid, :13 past each hour to 18:13)","11:16–11:29","JR Yosan Line rapid — no surcharge",1240),
       ("JR Kan-onji Stn","Ariake Ground (shuttle stop, in Kotohiki Park)","—","20 min","On foot",0),
       ("Ariake Ground","Takaya Shrine upper shrine","12:00 (no 12:30 run)","+25 min","Takaya Shrine shuttle bus — RETURN fare, Sat/Sun/holidays only",1500),
       ("Takaya Shrine","Ariake Ground","13:30 (no 13:00 run)","+25 min","Same shuttle — return included in the ¥1,500 above",None),
       ("Zenigata Sunae","Kotohiki Park viewpoint","—","few min from the shuttle stop","On foot — free, open 24 h",0),
       ("Kan-onji area","Chichibugahama and back","hop on and off all day","—","Hearts Shuttle 1-day pass (Sat/Sun/holidays)",1500),
       ("Kan-onji","Takamatsu","last local 22:34","+1h03–1h16","JR Yosan Line local train",1240)]),

dict(date="2026-10-13", title="Across to Tokushima city, on the east coast",
 flow=[
  ("12 departures", "THE KŌTOKU EXPRESS HIGHWAY BUS, under two hours and the cheapest and "
   "fastest link on the island. Nothing today is tight — this is the rest day before the "
   "mountains."),
  ("11:00 / 14:00 / 15:00 / 16:00", "AWA ODORI KAIKAN — the museum of Tokushima's dance "
   "festival (¥500) and a LIVE DAYTIME SHOW at one of those four times, 40 minutes, ¥1,300, "
   "with a chance to be taught the steps. Pick your show time first and fit the rest around "
   "it; that is the only fixed thing today."),
  ("to 21:00 in October", "THE BIZAN ROPEWAY from the same building, ¥1,500 return, for the "
   "view over the delta. It runs until 21:00 until 31 October, so the night view is easy."),
  ("or ¥2,640", "THE 3-IN-1 SET — museum + day show + ropeway — against ¥3,300 separately."),
  ("20:00, if you stay in", "THE EVENING SHOW, ¥1,600, performed by a different famous troupe "
   "each night and generally rated above the daytime one. It ends about 20:50."),
  ("optional, flat",
   "TEMPLES 1–5 of the 88-temple pilgrimage — a flat, fully signposted walk between local "
   "stations, and the classic first day for henro pilgrims. A taste of the route without "
   "the 1,200 km."),
 ],
 do=["Awa Odori Kaikan — the museum of Tokushima's famous dance festival, with live "
     "demonstrations daily and a chance to be taught the steps.",
     "The ropeway from the same building up Mt Bizan for the view over the delta.",
     "Optional and very easy: temples 1–5 of the 88-temple pilgrimage are a flat, signposted "
     "walk between local stations — a real taste of the henro route without the 1,200 km."],
 travel="A single highway bus, under two hours. The cheapest and fastest link on the island.",
 watch=["Nothing tricky today. It's the rest day before the mountains."],
 sleep="Tokushima — Hostel PAQ, 8 min walk from the station",
 legs=[("Takamatsu","Tokushima","12 departures each way","+1h50","Kōtoku Express highway bus",2300)]),

dict(date="2026-10-14", title="Into the gorge — the Dosan Line ride and the Ōboke boat",
 do=["The train ride into the gorge, and the sightseeing boat through it."],
 flow=[
  ("09:56 → 11:51",
   "THE TOKUSHIMA LINE LOCAL to 阿波池田 Awa-Ikeda. Just under two hours and NO CHANGES at "
   "all — one of the easiest legs on the whole trip. Sit on the right for the Yoshino river."),
  ("11:51 → 12:11",
   "DROP THE BIG BAGS AT AWA-IKEDA. It is staffed, open 05:30–23:30, and has a ¥400 locker "
   "size. Ōboke has been completely unstaffed since 2010, every locker there is ¥500, coins "
   "only, and there is no change machine. Twenty minutes is enough; do not dawdle."),
  ("12:11 → 12:50",
   "THE DOSAN LINE INTO THE GORGE — and THIS is the train ride worth talking about. The line "
   "threads the Ōboke gorge on ledges and bridges above the river, and it is one of the "
   "loveliest slow rides in Japan. Forty minutes, and it is the reason this day is a "
   "sequence rather than a list: it happens between two fixed points and there are only "
   "seven arrivals a day at Ōboke."),
  ("13:34 → 13:38",
   "THE BUS TO THE BOAT. From 大歩危駅前, the stop directly in front of JR Ōboke, four "
   "minutes up the road to 大歩危峡 — the stop is AT the boat. Do not walk it: there is no "
   "footpath, just Route 32 with traffic, and it is 1.5 km."),
  ("13:45 – 14:30",
   "THE ŌBOKE GORGE CRUISE. Half an hour and 4 km on a flat-bottomed boat between "
   "200-metre cliffs of folded marble-grey rock, out to the mouth of Koboke and back. It "
   "asks nothing of you but a seat. ¥1,500, boats hold 25, they run continuously 09:00–17:00 "
   "with the last at 16:30, and the ticket desk is the 1st-floor front counter of the "
   "レストラン大歩危峡まんなか — you walk in through the restaurant. Life jackets are "
   "compulsory and refusing one means refusing the boat."),
  ("15:17",
   "BACK TO AWA-IKEDA, collect the bags, and eat Iya soba — buckwheat from a valley too "
   "steep to grow rice."),
 ],
 travel="Two hours of local train with no changes, twenty minutes to stash the bags, forty "
        "minutes deeper into the gorge, and a four-minute bus to the water.",
 watch=["⚠️ ONLY SEVEN TRAINS A DAY reach Ōboke. Miss the 12:11 and the day loses its shape.",
        "⚠️ The boat does not run in high water or strong wind, and runs a shortened route "
        "when the river is low. There is no booking — you turn up.",
        "Leave the big bags at Awa-Ikeda, not Ōboke. See step 2; this is the single most "
        "useful thing on the day.",
        "Don't walk from the station to the boat. The bus takes 4 minutes for ¥110 and the "
        "walk is 1.5 km along a main road with no pavement."],
 sleep="Awa-Ikeda — 4S STAY (run by JR Shikoku)",
 legs=[("Tokushima","Awa-Ikeda","11 locals/day","+1h55, no changes","JR Tokushima Line local train",1830),
       ("Awa-Ikeda","Ōboke","12:11","12:50","JR Dosan Line local (only 7 arrivals a day)",530),
       ("大歩危駅前 Ōboke-ekimae","大歩危峡 Ōboke-kyō (the stop AT the boat)","13:34","13:38","Shikoku Kotsu, Iya line — 4 min",110),
       ("Gorge cruise","and back","runs continuously, last 16:30","+30 min, 4 km","Sightseeing boat, tickets at the Mannaka restaurant front desk",1500),
       ("Ōboke","Awa-Ikeda","15:17","+~30 min","JR Dosan Line local train",530)]),

dict(date="2026-10-15", title="The vine bridge, and a long slow afternoon",
 do=["Iya Kazurabashi, Biwa Falls, and — because of how the buses fall — a genuinely "
     "unhurried afternoon at Ōboke."],
 flow=[
  ("07:45 / 08:14",
   "DOWN THE VALLEY to Ōboke on the first local. Leave the big bags at Awa-Ikeda: it is "
   "staffed, open 05:30–23:30 and has a ¥400 locker. Ōboke has been completely unstaffed "
   "since 2010, every locker is ¥500, coins only, no change machine."),
  ("08:58 → 09:19",
   "THE BUS TO KAZURABASHI. Cash only — coins and ¥1,000 notes. Break bigger notes at the "
   "Awa-Ikeda 7-Eleven before you set out; there is nothing up the valley."),
  ("09:20–11:00",
   "IYA KAZURABASHI — 45 metres of woven mountain vine hanging 14 metres above the river, "
   "rebuilt every three years, with the slats spaced wide enough to see straight down "
   "between them. Legend says the Heike built these so they could cut them behind "
   "themselves. Five minutes from the bus stop. Then BIWA FALLS, a 50-metre waterfall "
   "literally fifty metres to your left as you step off the bridge."),
  ("11:00–15:11",
   "THE REST OF THE VALLEY, slowly — this is a long window and there is no way to shorten "
   "it, because the return buses are what they are. The riverside path below the bridge, "
   "lunch at the michi-no-eki, and Iya soba, which is what a valley too steep to grow rice "
   "eats instead."),
  ("14:16 → 14:37",
   "TAKE THE 14:16 BUS, NOT THE 15:11. Both exist; the 14:16 puts you at 大歩危駅前 at 14:37 "
   "in time for the 15:17 train, while the 15:11 arrives at 15:32 — fifteen minutes after it "
   "has gone — and leaves you on an unstaffed platform until 17:42. Same bus fare, two hours "
   "of your life."),
  ("14:37 → 15:17",
   "FORTY MINUTES AT ŌBOKE, which is about right for the station lookout loop — a flat 1 km "
   "round trip above the gorge, with its trailhead on the Walks tab. If you would rather "
   "have the extra hour at the bridge, take the 15:11 knowingly and plan for the wait."),
 ],
 travel="Local train down the valley, the one bus line that serves the vine bridge, and back "
        "— with a long, unavoidable gap before the evening train.",
 watch=["⚠️ THE LAST BUS BACK TO ŌBOKE IS 17:41. There is no later one and no taxi rank.",
        "⚠️ THE 15:11 BUS IS A TRAP. It reaches 大歩危駅前 at 15:32, fifteen minutes after "
        "the 15:17 train, so it costs you two hours on an unstaffed platform. The 14:16 gets "
        "you the 15:17. Northbound departures from かずら橋夢舞台 are 08:11, 09:11, 11:13, "
        "12:11, 13:11, 14:16, 15:11 and then 17:41, which is the last.",
        "The buses take cash only — coins and ¥1,000 notes.",
        "The Hotel Iya Onsen cable car (a 42-degree funicular dropping 170 m to riverside "
        "baths) has only 3 buses a day serving its stop, so it is a three-hour commitment or "
        "a photo from the window. It is NOT a second mountain — it is a lift to a bath.",
        "Skip Ochiai village despite the photographs: it climbs 400 vertical metres and the "
        "famous viewpoint is across the valley, reachable only by taxi."],
 sleep="Awa-Ikeda — 4S STAY (run by JR Shikoku)",
 legs=[("Awa-Ikeda","Ōboke","07:45","08:14","JR Dosan Line local train",530),
       ("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line",670),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","14:16 (or 15:11)","14:37 (or 15:32)","Shikoku Kotsu, Iya line",670),
       ("Ōboke","Awa-Ikeda","15:17 (or 17:42 if you took the later bus)","+~30 min","JR Dosan Line local train",530)]),

dict(date="2026-10-16", title="Mt Tsurugi — the one day that goes deep up the valley",
 do=["Mt Tsurugi by chairlift, and the ride up the valley to reach it."],
 flow=[
  ("07:45 / 08:14", "Down to Ōboke on the first local, bags left at Awa-Ikeda again."),
  ("08:58 → 09:19",
   "THE VALLEY BUS. Yes, this passes the vine bridge stop again — Kazurabashi Yumebutai is "
   "the interchange for everything deeper in the valley, so you go through it rather than "
   "to it. You are not visiting the bridge twice; today you change buses there."),
  ("09:30 → 10:16", "Change at Kazurabashi Yumebutai onto the Higashi-Iya line as far as Kubo."),
  ("10:20 → 11:10",
   "THE MIYOSHI CITY BUS UP TO MINOKOSHI, the trailhead village at 1,420 m. ⚠️ This wing "
   "runs DAILY only between 1 Oct and 3 Nov — outside that it is weekends only, and from "
   "24 Nov it stops altogether. You are inside the window, barely."),
  ("11:10–14:55",
   "MT TSURUGI. The chairlift lifts you from 1,420 m to 1,750 m in fifteen minutes and the "
   "ridge walk from the top station is gentle — second-highest peak in western Japan for "
   "very little effort. See the Walks tab for the exact trailhead and the route the "
   "official site recommends. THE FOLIAGE: at 1,955 m this is the one place on the whole "
   "trip that is turning while you are here; true peak is 25 Oct–1 Nov, so you catch the "
   "beginning. Carry food — there are no shops up here."),
  ("14:55, and not the 11:12",
   "COME BACK ON THE 14:55. The only other return is 11:12, which would give you two "
   "minutes on the mountain. Then Kubo 16:44, Kazurabashi 17:41 — the last bus of the day — "
   "and Ōboke 18:19."),
 ],
 travel="Train, then two buses with a change at Kubo, then the chairlift, and the whole "
        "chain back again. Long, but it is the payoff day and almost all of it is sitting down.",
 watch=["⚠️ WHAT YOU CANNOT ALSO DO TODAY, AND WHY. Nagoro the scarecrow village and the "
        "Oku-Iya double vine bridges sit on this same road, and every guide lists all three "
        "together — but that assumes a car. On buses there is ONE useful pair a day up to "
        "Minokoshi and back (10:20 up, 14:55 down); stepping off at Nagoro means giving up "
        "the mountain entirely. Pick one. The alternative below does Nagoro and the double "
        "bridges instead.",
        "⚠️ Very long day with tight connections and no slack. If a bus is late, the 17:41 "
        "is the last one out of the valley.",
        "The buses are cash only. Bring more coins than you think.",
        "This wing runs daily only 1 Oct – 3 Nov."],
 strand=[
  _S("The four-bus chain out of the valley — 14:55 down, then 17:41 is the last bus",
     "CONFIRMED",
     "Miyoshi City's own English sheet: Mt Tsurugi 14:55 → Kubo 15:45, Kubo 16:44 → "
     "Kazurabashi Yumebutai 17:30, Yumebutai 17:41 → 大歩危駅前 18:07, train 18:19. The "
     "only earlier return from the mountain is 11:12, which gives you two minutes up "
     "there. The 17:41 is the LAST bus out of the valley in any direction.",
     check="Re-read the sheet before you go — it is revised each 1 April and 1 October, "
           "and you travel just after a revision date: miyoshi-tourism.jp → "
           "bus_timetable_en.",
     who="Awa-Ikeda Bus Terminal (Shikoku Kotsu) 0883-72-1231",
     by="Check again in early October 2026, after the 1 October revision.",
     fallback="None. There is no taxi rank at Minokoshi and no accommodation you can "
              "walk to. If a bus is late, everything after it is lost.",
     links=["miyoshi_en", "jr_oboke"]),
  _S("The Mt Tsurugi bus wing only runs DAILY between 1 Oct and 3 Nov",
     "CONFIRMED",
     "Quoted from the sheet: “Buses for Mt. Tsurugi operate only Saturday, Sunday and "
     "national holidays from Apr 18 to Nov 23. The buses operate daily for Apr 18 to "
     "May 6, Jul 4 to Aug 31 and Oct 1 to Nov 3.” 16 October 2026 is a FRIDAY, so this "
     "day only exists because it falls inside that 1 Oct–3 Nov window.",
     check="Confirm the window has not moved in the 1 October 2026 revision.",
     who="Miyoshi City / Awa-Ikeda Bus Terminal 0883-72-1231",
     by="Early October 2026.",
     fallback="Outside the window it is weekends and holidays only, and from 24 November "
              "it stops altogether. If the window moves, this day becomes the Nagoro "
              "alternative instead.",
     links=["miyoshi_en"]),
 ],
 sleep="Awa-Ikeda — 4S STAY",
 alt_label="Mt Tsurugi and the chairlift",
 alts=[NAGORO_ALT],
 legs=[("Awa-Ikeda","Ōboke","07:45","08:14","JR Dosan Line local train",530),
       ("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line",670),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","久保 Kubo","09:30","10:16","Shikoku Kotsu, Higashi-Iya line",750),
       ("久保 Kubo","剣山 Mt Tsurugi (Minokoshi)","10:20","11:10","Miyoshi City bus, 名頃線 — daily 1 Oct–3 Nov only",1380),
       ("Minokoshi 1,420 m","Nishijima 1,750 m and back","—","15 min each way","Mt Tsurugi chairlift",2300),
       ("剣山 Mt Tsurugi (chairlift base)","久保 Kubo","14:55","15:45","Miyoshi City bus, 名頃線 — last down of the day",1380),
       ("久保 Kubo","かずら橋夢舞台 Kazurabashi Yumebutai","16:44","17:30","Shikoku Kotsu, Higashi-Iya line",750),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","17:41","18:07","Shikoku Kotsu — LAST BUS of the day",670),
       ("Ōboke","Awa-Ikeda","18:19","+~30 min","JR Dosan Line local train",530)]),

dict(date="2026-10-17", title="Down the gorge to Kōchi, on the south coast",
 flow=[
  ("08:15 or 14:22, nothing else",
   "⚠️ ONLY TWO LOCAL TRAINS A DAY RUN THROUGH TO KŌCHI. The 14:22 is the civilised one; the "
   "08:15 costs you the morning. Miss both and you are stuck in the valley for the night — "
   "this is the single most important line in today's plan."),
  ("12:11 → 12:50", "Down from 阿波池田 Awa-Ikeda to 大歩危 Ōboke to meet it, with time to spare "
   "and lunch at the michi-no-eki."),
  ("14:22 →", "THE DOSAN LINE SOUTH — switchbacks, tunnels and river crossings for a couple "
   "of hours. This leg IS the sightseeing; there is nothing to do but look out of the window."),
  ("on arrival", "⚠️ KŌCHI DOES NOT TAKE NATIONAL IC CARDS — it has its own, Iruca. Cash from "
   "here on, for buses, trams and JR."),
  ("evening", "HIROME MARKET — a covered hall of about sixty stalls where you buy from "
   "whichever you like and eat at shared tables. Order katsuo no tataki, bonito seared over "
   "burning rice straw. ⚠️ It divides people: 'very crowded and loud', 'I got overstimulated'. "
   "The stalls just outside are calmer."),
 ],
 do=["The ride itself — the Dosan Line south of Ōboke is switchbacks, tunnels and river "
     "crossings, and you're on it for a couple of hours.",
     "Hirome Market in the evening: a covered hall of about sixty stalls where you buy from "
     "whichever you like and eat at shared tables. Order katsuo no tataki — bonito seared "
     "over burning rice straw, Kōchi's signature dish."],
 travel="Only two local trains a day run right through to Kōchi. The 14:22 is the civilised one.",
 watch=["Two through-trains a day: 08:15 and 14:22. Miss both and you're stuck.",
        "Kōchi does not accept national IC cards — it has its own. Cash from here on.",
        "Hirome Market divides people: 'very crowded and loud', 'I got overstimulated'. The "
        "stalls just outside are calmer."],
 sleep="Kōchi — central, near Hirome Market",
 legs=[("Awa-Ikeda","Ōboke","12:11","12:50","JR Dosan Line local train",530),
       ("Ōboke","Kōchi","14:22","not published","JR Dosan Line local (2 through-trains a day)",1430)]),

dict(date="2026-10-18", title="Kōchi — market, castle, then the Pacific",
 do=["The Sunday market, Kōchi Castle, Katsurahama beach and the Ryōma statue, and "
     "Makino Botanical Garden if you want a fourth thing."],
 flow=[
  ("from 07:00",
   "THE SUNDAY MARKET, first and early. 300 years old, a kilometre of stalls running "
   "straight up Ōtesuji, and it happens ONLY today — this is the entire reason the "
   "itinerary puts you in Kōchi on a Sunday. Produce, knives, antiques, hot food. Go "
   "early: it is a morning market and it thins out through the afternoon. ⚠️ I could not "
   "reach an official page for its exact hours — your accommodation will know."),
  ("~10:30, on foot",
   "KŌCHI CASTLE, which stands at the top of the same street. No transport needed at all: "
   "the market runs up Ōtesuji and the castle is at the end of it, so you walk off the end "
   "of the market into the castle grounds. One of only twelve original keeps in Japan and "
   "the only one keeping BOTH its main keep and its lord's residence. ⚠️ Ladder-stairs "
   "inside — the grounds are the good part and cost nothing."),
  ("~12:30",
   "LUNCH at Hirome Market, five minutes from the castle — about sixty stalls, you buy "
   "from whichever you like and eat at shared tables. Katsuo no tataki, bonito seared over "
   "burning rice straw, is the Kōchi dish. It divides people: “very crowded and loud”, "
   "“I got overstimulated”. The stalls just outside are calmer."),
  ("~14:00",
   "THE MY-YU BUS, boarded AT THE JR KŌCHI STATION TERMINUS — the stop is in the こうち旅広場 "
   "car park at the station's SOUTH exit, not on the street. Do not pick it up at "
   "Harimayabashi: it arrives already full, and a traveller who tried described standing "
   "“in a sardine can”. Afternoon is deliberate — the crush is a morning problem and the "
   "bus empties after Makino."),
  ("~15:00",
   "KATSURAHAMA — a pine-backed crescent of beach facing the open Pacific, with the statue "
   "of Sakamoto Ryōma, the samurai who helped end the shogunate, looking out to sea. This "
   "is last on purpose: it is the west-facing coast and the only part of the day that is "
   "better in low light. Swimming is not allowed here — the current is dangerous."),
  ("instead of the beach",
   "MAKINO BOTANICAL GARDEN on Godaisan is the alternative fourth stop, on the same bus. "
   "⚠️ It is “on the side of a mountain so it's not quite the easy stroll you expect from a "
   "botanical garden”. Pick Makino OR Katsurahama — doing both makes the afternoon a bus "
   "timetable exercise."),
 ],
 travel="Nothing but your feet until lunch — the market, the castle and Hirome are one "
        "continuous walk. The afternoon is a single bus from the station forecourt and back.",
 watch=["⭐ The MY-YU pass is ¥1,000 but HALVED TO ¥600 if you show a foreign passport. Ask "
        "for it explicitly; it is not offered.",
        "⚠️ Kōchi does NOT accept national IC cards — it has its own, Iruca. Cash for the "
        "buses, the trams and JR out here.",
        "⚠️ Board the MY-YU at the JR station, not Harimayabashi. See step 4.",
        "The tram day pass is only worth it if you are moving around the centre a lot — the "
        "market, castle and Hirome are all walkable from each other.",
        "The bus timetable is published as images on the operator's page and I could not "
        "read the departure times out of it. Confirm the last bus back from Katsurahama at "
        "the ticket desk when you buy the pass — this is the one thing today that can strand "
        "you."],
 strand=[
  _S("The last MY遊バス back from Katsurahama",
     "UNREADABLE",
     "17:00 from 桂浜, reaching 高知駅 at 18:01; every run takes 52 minutes. NINE services "
     "on Sundays and holidays, only SIX on weekdays — 18 October 2026 is a Sunday, so "
     "you get the full nine. ⚠️ TIER: this is a third-party site. Tosaden publishes its "
     "own timetable as IMAGES, which is why it could not be read from the operator.",
     check="NO CALL NEEDED. The third-party page below is readable right now and carries "
           "the times; the official page has the same table but only as images. Then "
           "confirm the last 桂浜 departure AT THE TICKET DESK when you buy the MY遊 pass at "
           "Kōchi station, and photograph the board while you are there.",
     who="The JR Kōchi station bus counter, in person. Nothing here needs a phone call.",
     by="On the morning, before you board.",
     fallback="Katsurahama is 13 km from the city with no rail. A taxi back is the only "
              "other option and it is not cheap.",
     links=["myyu_times", "myyu"]),
 ],
 sleep="Kōchi — central, near Hirome Market",
 legs=[("Katsurahama and Makino","—","—","—","MY-YU tourist bus pass (¥600 with a foreign passport)",600),
       ("City trams","—","—","—","Tosaden tram city-zone day pass",500)]),

dict(date="2026-10-19", title="Right across to Matsuyama, on the west coast, and Dogo Onsen",
 flow=[
  ("8:30 / 10:20 / 13:20 / 16:30 / 18:20",
   "THE NANGOKU EXPRESS, five departures and every seat reserved. Take the 10:20 unless you "
   "have a reason not to: it is three hours, and the later ones cost you the evening. There "
   "is no realistic rail alternative — the all-slow route is nearly ten hours on a single "
   "daily 05:39 departure."),
  ("mid-afternoon", "Drop the bags, then the tram out to 道後温泉 Dogo Onsen."),
  ("06:00–23:00", "DOGO ONSEN HONKAN — one of the oldest hot springs in Japan, named in "
   "8th-century chronicles and the model for the bathhouse in Spirited Away. The restoration "
   "finished in July 2025, so you finally see it without scaffolding. ¥700 for the "
   "ground-floor Kami-no-Yu. Bathing etiquette: wash thoroughly at the taps FIRST, no "
   "swimwear, small towel stays out of the water."),
  ("if the queue is long", "飛鳥乃湯泉 ASUKA-NO-YU next door is ¥610, newer and much quieter."),
  ("evening", "THE ARCADE between the tram stop and the bathhouse, for dinner. The footbath "
   "outside is, in every account, 'blisteringly hot, always'."),
 ],
 book=["☎ THE NANGOKU EXPRESS BUS IS RESERVATION-ONLY — every seat is assigned and there "
       "is no walk-up. Only five run a day. Book it as soon as your dates are fixed; your "
       "Kōchi accommodation can do it for you.",
       "There is no realistic rail fallback: the all-slow route is nearly ten hours on a "
       "single daily 05:39 departure."],
 do=["Dogo Onsen — one of the oldest hot springs in Japan, mentioned in 8th-century "
     "chronicles, and the model for the bathhouse in Spirited Away. The restoration finally "
     "finished in July 2025, so you see it without scaffolding.",
     "The Botchan Train, a replica Meiji-era steam locomotive that still runs through the "
     "streets.",
     "The shopping arcade between the tram stop and the bathhouse, good for dinner."],
 travel="A three-hour bus. This is the one leg with no realistic train option — the all-slow "
        "rail route takes nearly ten hours on a single daily service leaving at 05:39.",
 watch=["Five departures: 8:30, 10:20, 13:20, 16:30, 18:20.",
        "The footbath outside Dogo Onsen is, in every account, 'blisteringly hot, always'.",
        "Bathing etiquette: wash thoroughly at the taps first, no swimwear, small towel stays "
        "out of the water."],
 sleep="Matsuyama — Dogo Onsen area or near JR station",
 legs=[("Kōchi","Matsuyama","10:20","+~3 h","Nangoku Express highway bus (5 a day)",4000)]),

dict(date="2026-10-20", title="Matsuyama Castle, or a day out instead",
 do=["MATSUYAMA CASTLE — one of only twelve original keeps left in Japan, on a hill in the "
     "middle of the city, with a connected-keep layout whose walls you can walk. The views "
     "over the Inland Sea are the real point.",
     "NINOMARU GARDEN below it, built over the old lord's residence. ¥200, flat, and the "
     "quiet counterweight to the castle.",
     "DOGO ONSEN in the evening if you didn't get your fill of it, or the arcade for dinner.",
     "Be honest with yourself about the scale of this: the castle is a half-day. If that "
     "sounds thin, switch this day to one of the alternatives — that is what they are for."],
 travel="Trams around town, and a chair lift up the castle hill. Nothing today needs a timetable.",
 watch=["Take the CHAIR LIFT rather than the ropeway — same ticket, same price, much shorter "
        "queue, and it is the nicer ride.",
        "⚠️ You do NOT have to go inside the keep. It is steep narrow ladder-stairs climbed in "
        "socks, and the exterior, the walls and the view are what people come for. The "
        "grounds cost nothing; the keep is ¥520.",
        "Allow ~30 min from the lift station to the ticket window — the castle's own site "
        "says budget about an hour in total before you are actually inside.",
        "Buy water before going up; drinks cost more at the top.",
        "✅ Matsuyama accepts Suica — the one place in Shikoku that reliably does, and here "
        "it PAYS: Iyotetsu raised the tram to ¥250 flat on 1 April 2026, but the cashless "
        "discount takes ¥20 off, so tapping IC costs the old ¥230. Tap, don't pay cash."],
 sleep="Matsuyama",
 alt_label="Matsuyama Castle and the city",
 alts=MATSUYAMA_ALTS,
 legs=[("Castle hill","up and back","—","3 min each way","Chair lift",520),
       ("City trams","—","—","—","Iyotetsu tram, flat fare — ¥250 cash, ¥230 if you tap IC",250)]),

dict(date="2026-10-21", title="The Shimanami Kaido — island-hopping to Onomichi",
 flow=SHIMANAMI_BUS_FLOW,
 do=["The Shimanami Kaido: a chain of six islands linked by seven of the most elegant "
     "suspension bridges in the world, crossing the Inland Sea from Shikoku back to Honshu. "
     "Even by bus it is one of the great scenic routes in Japan.",
     "OPTIONAL and recommended: take the bus out to one island, rent a bike there, ride a "
     "bridge or two on the dedicated cycleway, and ferry back. Bridge tolls are waived for "
     "cyclists until 2028. One blogger did exactly this because of the bus timings.",
     "Onomichi itself — a steep temple town of alleys and cats above a working shipping strait."],
 travel="Local train up the coast, then bus across the islands with one change.",
 watch=["There is NO direct Imabari–Onomichi bus; that route was abolished in 2005. You "
        "change at Innoshima Ōhashi, and the operator warns the connection 'may not be smooth'.",
        "Don't try to cycle all 70 km. Every bridge has a long climbing ramp and beginners "
        "take eight to ten hours.",
        "A one-way bike drop-off costs ¥1,000 extra."],
 sleep="Onomichi — Guesthouse Yadocurly",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari","Onomichi","hourly connections","+1.5–2 h","Shimanami Liner + local bus",2390)]),

dict(date="2026-10-22", title="Rabbit island, then Hiroshima",
 flow=RABBIT_FLOW,
 do=["ŌKUNOSHIMA — the rabbit island. Around a thousand feral rabbits that will run at you "
     "en masse when you sit down. The island's other half is its history: it made poison gas "
     "for the Imperial Army and was erased from maps, and the small museum is unflinching "
     "about it. Ruined batteries and a power plant stand in the woods.",
     "Optional hour on the way: Takehara, an Edo salt-and-sake merchant town 12 minutes' walk "
     "from its station, and home of Nikka Whisky's founder."],
 travel="Two slow trains along the coast, then a 15-minute ferry.",
 watch=["BUY RABBIT FOOD BEFORE YOU BOARD — none is sold on the island. About ¥200 at the shop "
        "by Tadanoumi station, open 07:00–19:45. Buy PELLETS, not vegetables: the official "
        "rules say leftover veg spoils and draws crows that prey on the kits.",
        "The ferry is CASH ONLY.",
        "Do not pick the rabbits up — they panic and break bones, and there is no vet.",
        "Allow 4–5 hours. A couple who budgeted three ended up running for the boat.",
        "Bag storage at the port is ¥500 a bag."],
 strand=[
  _S("The last boat OFF Ōkunoshima — this plan's '18:30' does not match the operator",
     "UNVERIFIED",
     "大三島フェリー's own timetable gives the last call at 大久野島 heading to 忠海 as "
     "※17:16, arriving 忠海 17:30 — and the ※ means that sailing serves the island only "
     "between FEBRUARY AND OCTOBER. The next boat, 18:40 from 盛, does NOT stop at "
     "Ōkunoshima at all. A SECOND operator (休暇村客船) also works this route and is "
     "probably where the '18:30' and 'every 30–45 min' in this plan came from, but its "
     "timetable sits behind a bot wall and could NOT be read. Treat 18:30 as unconfirmed.",
     check="ONLINE: the 大三島フェリー timetable below is readable now and gives 17:16 — take "
           "that as your working deadline. Its 運航情報 notices sit on the same page, so "
           "check them too (the second jetty has closed for repairs before). The second "
           "operator's page is bot-walled from here but may open in a normal browser — "
           "try it, and if it loads, read its last sailing.",
     who="NO PHONE CALL NEEDED IF YOU DO ONE THING: confirm the last sailing AT THE "
         "TADANOUMI TICKET WINDOW when you buy, and ask which operator it is — a "
         "face-to-face question with a printed timetable in front of you. Only if you "
         "want certainty in advance, have your hotel ring 休暇村大久野島 0846-26-0321.",
     by="On the morning, at the port, before you cross.",
     fallback="NONE. Ōkunoshima has one hotel and no other way off. Miss the last boat "
              "and you are on the island for the night. The operator warns of delays at "
              "busy times, and its second jetty has been closed for repairs before now.",
     links=["omishima_time", "qkamura_ohkuno", "rabbit_island"]),
 ],
 sleep="Hiroshima — The Evergreen Hostel or J-Hoppers",
 legs=[("Onomichi","Mihara","not published","not published","JR Sanyo Line local train",None),
       ("Mihara","Tadanoumi","—","+22 min","JR Kure Line local train",320),
       ("Tadanoumi Port","Ōkunoshima and back","every 30–45 min, last out 18:30","+15 min each way","Ferry — CASH ONLY",720),
       ("Tadanoumi Port","bag storage","—","—","¥500 per bag per day",500),
       ("Tadanoumi","Hiroshima Bus Centre","4 round trips/day","+1h40","Geiyo Bus 'Kaguya-hime'",1500)]),

dict(date="2026-10-23", title="Miyajima",
 flow=MIYAJIMA_FLOW,
 do=["The floating torii at Itsukushima — the great vermilion gate standing in the sea at "
     "high tide and walkable to across the seabed at low. Try to see both; the water turns "
     "over about six hours. Below 100 cm you can walk out, above 250 cm it floats — the "
     "October table is at https://www.miyajima.or.jp/sio/sio10.html",
     "Itsukushima Shrine itself, built on stilts over the water since the 12th century.",
     "The ropeway up Mt Misen for the Inland Sea panorama, plus the island's wild deer and "
     "the Daishō-in temple complex on the way up.",
     "Momiji manjū — maple-leaf-shaped cakes, made in front of you all along the main street."],
 travel="Tram out to the pier and a 10-minute ferry. One pass covers everything.",
 watch=["Buy the Hiroden ¥1,000 day pass: all trams + the ferry + the ¥100 island visitor tax "
        "+ it cuts the ropeway from ¥2,000 to ¥1,500.",
        "FREE UPGRADE: ride the JR ferry outbound between 9:10 and 16:10 and it detours close "
        "past the torii at no extra cost or time.",
        "The summit is a further ~30 minutes up a steep stepped trail beyond the ropeway. The "
        "observatory at the top station is enough — treat the summit as optional.",
        "Last ropeway ascent is 16:00.",
        "The Reikadō hall with its 1,200-year flame burned down in May 2026 and is gone.",
        "Momijidani — literally 'maple valley' — was recorded completely green on 12 October "
        "2025. You are about six weeks early for it."],
 sleep="Hiroshima",
 legs=[("Hiroshima","Miyajima + all city trams","—","—","Hiroden 1-day tram & ferry pass",1000),
       ("Momijidani","Shishiiwa (Mt Misen)","last ascent 16:00","+~20 min each way","Ropeway — ¥1,500 with the pass",1500)]),

dict(date="2026-10-24", title="Peace Memorial Park, then on to Kyushu",
 do=["The Peace Memorial Museum and the A-Bomb Dome. Allow more time than you think, and "
     "expect to want quiet afterwards.",
     "Okonomiyaki Hiroshima-style — layered rather than mixed, with noodles — before you go."],
 travel="Everything central. Trams are a flat ¥240 anywhere in the city.",
 watch=[],
 sleep="→ Kyushu",
 legs=[]),
])

# ─────────────────────────────────────────────────────────────────────────────

B = dict(
    key="B",
    name="Option B — Awaji Island and the Naruto whirlpools first",
    verdict=("Buys you the whirlpools and an island almost no foreign backpacker sees, and "
             "on October pricing it works out slightly CHEAPER than A because it skips the "
             "Himeji ferry and the Kōchi bus. The cost is fragility: it hangs on a bus that "
             "runs four times a day, a tide table, and it drops Kōchi."),
    days=[
dict(date="2026-10-09", title="Osaka → Awaji Island",
 flow=[
  ("frequent", "JR to 明石 Akashi, then about ten minutes on foot to 明石港 Akashi Port. The "
   "walk is signed but it is a real walk with a pack — allow the time."),
  ("15–16/day, 05:40–23:40", "THE JENOVA LINE FERRY, thirteen minutes and ¥700, passing under "
   "the Akashi Kaikyō Bridge — the longest suspension bridge in the world for 24 years. This "
   "is the crossing people remember."),
  ("at 岩屋港 on landing", "BUY THE ISLAND BUS DAY PASS at the Iwaya port terminal, before you "
   "go anywhere. ⚠️ AWAJI HAS NO RAILWAY AT ALL — everything on this island is buses, they "
   "take no IC cards, and the network radiates from Sumoto so crossing between spokes means "
   "going back to the hub."),
  ("afternoon", "IWAYA's fishing harbour and the seafood that comes off it, then the bus down "
   "to Sumoto."),
  ("plan tonight", "Use busmo.656.ch rather than Google Maps — it is the official Awaji "
   "planner and covers 13 operators. Tomorrow depends on getting this right."),
 ],
 do=["The crossing itself — a little ferry under the Akashi Kaikyō Bridge, the longest "
     "suspension bridge in the world for 24 years. Thirteen minutes, ¥700.",
     "Awaji is the island the creation myth says was made first, before the rest of Japan.",
     "Iwaya's fishing harbour and the seafood that comes off it."],
 travel="Train to Akashi, ten-minute walk to the port, then the little ferry across.",
 watch=["Awaji has NO RAILWAY AT ALL. Everything on the island is buses.",
        "The Seishun 18 slow-train pass is NOT sold in October, so the train leg is full fare "
        "(see the Glossary tab).",
        "Buy the island bus day pass at the Iwaya port terminal when you land."],
 sleep="Sumoto area — Awaji Tourist Trophy House",
 legs=[("Osaka / Kobe","Akashi","frequent","—","JR Sanyo Line",None),
       ("Akashi Port","Iwaya Port","15–16/day, 05:40–23:40","+13 min","Awaji Jenova Line ferry",700),
       ("Iwaya","Sumoto Bus Centre","—","—","Community or highway bus",500)]),

dict(date="2026-10-10", title="Awaji — pick one corridor and stay in it",
 do=["Awaji Yumebutai — a vast Tadao Ando concrete complex built into a scarred hillside, "
     "with a hundred stepped flower gardens. Free to walk through.",
     "Izanagi Shrine, said to be the oldest in Japan.",
     "The west coast for sunset, and onion everything — Awaji is famous for them."],
 travel="Buses only, on the day pass. The network radiates from Sumoto, so crossing between "
        "spokes usually means going back to the hub.",
 watch=["THE RULE: commit to ONE corridor — either the north-west shuttle strip or Sumoto as "
        "your hub. The one blogger who tried to roam the whole island car-free ended up "
        "walking fifty minutes between bus stops.",
        "Island buses take no IC cards. Cash (PayPay reportedly works).",
        "Plan on busmo.656.ch rather than Google Maps — it's the official Awaji planner and "
        "covers 13 operators."],
 sleep="Sumoto area",
 legs=[("All island buses","—","—","—","Awaji Kōtsū 1-day pass",880)]),

dict(date="2026-10-11", title="The Naruto whirlpools, then Tokushima",
 do=["The whirlpools from under the bridge, and the crossing into Shikoku."],
 flow=[
  ("BEFORE YOU BOOK ANYTHING",
   "PICK THE HOUR OFF THE TIDE CALENDAR FIRST — https://www.uzunomichi.jp/tide-calendar/ — "
   "and build the rest of the day around it. The vortices only form around PEAK TIDAL FLOW: "
   "a spring tide (大潮, red on the calendar) gives you about ±2 hours, a middle tide ±1.5, "
   "a neap tide only ±1. Everything below assumes you have done this."),
  ("07:00 → 07:31",
   "THE ONE USEFUL BUS. From 洲本バスセンター Sumoto Bus Centre across the Ōnaruto Bridge. "
   "⚠️ ON A SUNDAY THIS CROSSING RUNS THREE TIMES — 07:00, 11:15 and 16:00. Getting the "
   "07:00 is what makes the day work. ⚠️ The stop you want, 鳴門公園口 Naruto-kōen-guchi, is "
   "ALIGHT-ONLY: you can get off there, but you cannot board there to go back towards Awaji."),
  ("your tide window",
   "UZU-NO-MICHI — a 450-metre walkway slung under the road deck of the bridge with glass "
   "floor panels 45 metres directly above the churn. ¥510, 09:00–17:00 in October with last "
   "entry 16:30, and the cheapest way to see the whirlpools. Allow an hour."),
  ("or instead, your tide window",
   "THE BOAT, which puts you in among them rather than above them. Wonder Naruto is ¥2,000, "
   "12 sailings 09:00–16:20, and needs no reservation. The Aqua Eddy has an underwater "
   "window but DOES need booking. One operator is cash only."),
  ("if there is time left",
   "THE ŌTSUKA MUSEUM by the bridge — full-size ceramic reproductions of a thousand Western "
   "masterpieces, one of the strangest museums anywhere. ⚠️ ¥3,300, the most expensive "
   "admission on the whole trip, closed Mondays, and ticket sales stop at 16:00. It is a "
   "three-hour museum; do not start it at 15:00."),
  ("evening",
   "TO TOKUSHIMA. This bus runs 21 times on a weekday and is the easy part of the day."),
 ],
 travel="One bus across the bridge to a stop that sits on the bridge approach, the walkway or "
        "the boat in your tide window, then a frequent bus down into Tokushima.",
 watch=["⚠️ THIS DAY IS LOCKED TWICE OVER — by the tide calendar and by a bus that runs three "
        "times on a Sunday. Resolve the tide first, the bus second, everything else after.",
        "⚠️ 鳴門公園口 is alight-only. Plan the return from 鳴門公園 towards Tokushima, not "
        "back across the bridge.",
        "The Uzu-no-michi + Eddy combined ticket is ¥900 against ¥1,130 bought separately."],
 strand=[
  _S("Getting OFF Awaji — the cross-bridge bus runs three times on a Sunday",
     "CONFIRMED",
     "Awaji Kōtsū's 淡路・徳島線 is the only ordinary-passenger bus over the Ōnaruto Bridge: "
     "4 runs on a weekday, 3 at weekends. 11 October 2026 is a SUNDAY, so the crossings are "
     "07:00, 11:15 and 16:00 — taking the 07:00 is what makes the day fit. ⚠️ 鳴門公園口 is "
     "ALIGHT-ONLY: you can get off there, you cannot board there to go back.",
     check="Re-read the timetable PDF; Awaji Kōtsū revises on 1 April.",
     who="Awaji Kōtsū — Sumoto Bus Centre",
     by="Early October 2026.",
     fallback="Miss the 16:00 and there is no fourth crossing. Awaji has no railway at all.",
     links=["awaji_toku"]),
  _S("The last bus from Naruto Park down into Tokushima",
     "CONFIRMED",
     "Tokushima Bus, revised 1 April 2026: only EIGHT runs a day come through to 徳島駅前, "
     "the last leaving 鳴門公園 at 17:45 and reaching Tokushima 19:18. ¥720, CASH ONLY.",
     check="Re-read the PDF; Tokushima Bus revises 1 April and 1 October.",
     who="徳島バス 088-622-1826",
     by="Early October 2026.",
     fallback="Any bus to 鳴門駅前, then JR 鳴門 → 池谷 → 徳島.",
     links=["tokubus_naruto", "tokubus_narutofare"]),
 ],
 sleep="Tokushima — Hostel PAQ",
 legs=[("洲本バスセンター Sumoto Bus Centre","鳴門公園口 Naruto-kōen-guchi (ALIGHT ONLY)","07:00","07:31","Awaji Kōtsū — alight only",1380),
       ("鳴門公園 Naruto Park","渦の道 Uzu-no-michi glass walkway","—","—","Walkway under the bridge",510),
       ("亀浦観光港 Kameura Port","Whirlpool cruise","12 sailings 9:00–16:20","+~30 min","Wonder Naruto (no reservation needed)",2000),
       ("鳴門公園 Naruto Park","徳島駅 Tokushima Stn","last through-bus 17:45 (weekday)","+~86 min","Tokushima Bus, Naruto Park line — fare revised 1 Apr 2026",720)]),

dict(date="2026-10-12", title="Tokushima on foot",
 do=["Awa Odori Kaikan — the dance-festival museum, with daily live performances and a "
     "lesson if you want one.",
     "Mt Bizan by ropeway from the same building.",
     "Temples 1–5 of the 88-temple pilgrimage: a flat, fully signposted walk between local "
     "stations, and the classic first day for henro pilgrims."],
 travel="All walkable or a short local train. Deliberately light — it's a holiday.",
 watch=["Public holiday (Sports Day). Rural buses may not run at all, and holiday timetables "
        "are poorly documented online. Keep today walkable."],
 sleep="Tokushima — Hostel PAQ",
 legs=[]),

dict(date="2026-10-13", title="Into the Iya Valley — the Ōboke gorge boat",
 flow=[
  ("11 locals/day", "徳島 Tokushima to 阿波池田 Awa-Ikeda, just under two hours and NO CHANGES "
   "at all — one of the easiest legs on the trip."),
  ("at Awa-Ikeda", "DROP THE BIG BAGS HERE, not at Ōboke. Awa-Ikeda is staffed, open "
   "05:30–23:30, and has a ¥400 locker size. Ōboke has been unstaffed since 2010, every "
   "locker is ¥500, coins only, and there is no change machine."),
  ("12:11 → 12:50", "THE DOSAN LINE INTO THE GORGE — the line threads the Ōboke gorge on "
   "ledges and bridges above the river and is one of the loveliest slow rides in Japan. "
   "⚠️ Only SEVEN trains a day reach Ōboke; miss this one and the day loses its shape."),
  ("13:34 → 13:38", "THE BUS TO THE BOAT, from 大歩危駅前 — the stop directly in front of JR "
   "Ōboke — four minutes to 大歩危峡, which is the stop AT the boat. Do not walk it: 1.5 km "
   "along Route 32 with no pavement."),
  ("13:45 – 14:30", "THE GORGE CRUISE. Half an hour and 4 km between 200-metre cliffs of "
   "folded marble-grey rock. ¥1,500, boats hold 25, continuous 09:00–17:00 with the last at "
   "16:30. Tickets at the 1st-floor front counter of the レストラン大歩危峡まんなか — you walk "
   "in through the restaurant. Life jackets are compulsory."),
  ("evening", "Back to Awa-Ikeda for Iya soba — buckwheat from a valley too steep for rice."),
 ],
 do=["The Ōboke gorge cruise — half an hour between 200-metre cliffs, flat-bottomed boat, "
     "no effort required.",
     "The Dosan Line ride into the gorge, one of the prettiest slow rides in Japan.",
     "Iya soba, from a valley too steep to grow rice."],
 travel="Two hours of local train from Tokushima with no changes at all.",
 watch=["Leave big bags at Awa-Ikeda (staffed, ¥400 lockers) rather than Ōboke (unstaffed "
        "since 2010, ¥500 coins only).",
        "Take the 4-minute bus to the pier — the walk has no footpath."],
 sleep="Awa-Ikeda — 4S STAY",
 legs=[("Tokushima","Awa-Ikeda","11 locals/day","+1h55, no changes","JR Tokushima Line local train",1830),
       ("Awa-Ikeda","Ōboke","12:11","12:50","JR Dosan Line local train",530),
       ("大歩危駅前 Ōboke-ekimae","大歩危峡 Ōboke-kyō (the stop AT the boat)","13:34","13:38","Shikoku Kotsu, Iya line — 4 min",110),
       ("Gorge cruise","and back","last 16:30","+30 min","Sightseeing boat",1500)]),

dict(date="2026-10-14", title="The vine bridge",
 flow=[
  ("08:58 → 09:19", "From 大歩危駅前 Ōboke-ekimae to かずら橋夢舞台 Kazurabashi Yumebutai. "
   "⚠️ CASH ONLY — coins and ¥1,000 notes. Break bigger notes at the Awa-Ikeda 7-Eleven "
   "before you set out; there is nothing up the valley."),
  ("09:20 – 11:00", "IYA KAZURABASHI — 45 metres of woven mountain vine hanging 14 metres "
   "above the river, rebuilt every three years, slats spaced wide enough to see straight "
   "down between them. Five minutes from the stop. Then BIWA FALLS, fifty metres to your "
   "left as you step off the bridge."),
  ("11:00 – 14:16", "THE VALLEY, slowly. The riverside path below the bridge, lunch at the "
   "michi-no-eki, and the Peeing Boy statue on its cliff ledge if the bus timing works."),
  ("14:16 → 14:37", "⚠️ TAKE THE 14:16, NOT THE 15:11. The 15:11 reaches Ōboke at 15:32, "
   "fifteen minutes after the 15:17 train, and leaves you on an unstaffed platform until "
   "17:42. Northbound departures are 08:11, 09:11, 11:13, 12:11, 13:11, 14:16, 15:11 and "
   "then 17:41, which is the last bus of the day."),
  ("skip", "OCHIAI VILLAGE, despite the photographs: 400 vertical metres, and the famous "
   "viewpoint is across the valley, reachable only by taxi."),
 ],
 do=["Iya Kazurabashi — 45 metres of woven vine, 14 metres above the river, slats spaced "
     "wide enough to see straight through. Rebuilt every three years.",
     "Biwa Falls, fifty metres to the left as you step off the bridge.",
     "The Peeing Boy statue on its cliff ledge, if the bus timing works."],
 travel="One bus line up the valley and back.",
 watch=["LAST BUS BACK IS 17:41.",
        "Cash only — coins and ¥1,000 notes.",
        "Skip Ochiai village: 400 vertical metres, viewpoint is taxi-only."],
 strand=[
  _S("The last bus out of the Iya valley is 17:41",
     "CONFIRMED",
     "Northbound departures from かずら橋夢舞台 are 08:11, 09:11, 11:13, 12:11, 13:11, 14:16, "
     "15:11 and then 17:41, which is the last of the day. ⚠️ The 15:11 is a trap — it "
     "reaches 大歩危駅前 at 15:32, fifteen minutes after the 15:17 train, and leaves you on "
     "an unstaffed platform until 17:42. Take the 14:16.",
     check="Re-read the sheet after the 1 October 2026 revision.",
     who="Awa-Ikeda Bus Terminal (Shikoku Kotsu) 0883-72-1231",
     by="Early October 2026.",
     fallback="None. No taxi rank at the vine bridge and nothing to walk to. The buses are "
              "CASH ONLY — coins and ¥1,000 notes, and there is nowhere up the valley to "
              "break a bigger note.",
     links=["miyoshi_en", "jr_oboke"]),
 ],
 sleep="Awa-Ikeda — 4S STAY",
 legs=[("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line",670),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","14:16 (or 15:11)","14:37 (or 15:32)","Shikoku Kotsu, Iya line",670)]),

dict(date="2026-10-15", title="Mt Tsurugi — the one day that goes deep up the valley",
 flow=[
  ("08:58 → 09:19", "From 大歩危駅前 to かずら橋夢舞台. Yes, this is the vine-bridge stop again "
   "— it is the interchange for everything deeper in the valley, so you change buses there "
   "rather than visiting it twice."),
  ("09:30 → 10:16", "Change onto the Higashi-Iya line as far as 久保 Kubo."),
  ("10:20 → 11:10", "THE MIYOSHI CITY BUS up to 見ノ越 Minokoshi, the trailhead village at "
   "1,420 m. ⚠️ This wing runs DAILY only 1 Oct – 3 Nov; outside that it is weekends and "
   "holidays only, and it stops entirely after 23 November. You are inside the window."),
  ("11:10 – 14:55", "MT TSURUGI. The chairlift lifts you from 1,420 m to 1,750 m in fifteen "
   "minutes and the ridge walk from the top station is gentle — second-highest peak in "
   "western Japan for very little effort. See the Walks tab for the trailhead and the route "
   "the official site recommends. THE FOLIAGE: at 1,955 m this is the one place on the trip "
   "turning while you are here. Carry food; there is nothing up there."),
  ("14:55, not the 11:12", "COME DOWN ON THE 14:55 — the only other return is 11:12, which "
   "would give you two minutes on the mountain. It reaches 久保 Kubo at 15:45."),
  ("16:44 → 18:07", "Kubo → かずら橋夢舞台 17:30, then the 17:41 — THE LAST BUS OUT OF THE "
   "VALLEY — to 大歩危駅前 at 18:07. If a bus is late, that is the one that matters."),
 ],
 do=["Nagoro, the scarecrow village — about 300 life-size straw figures of departed "
     "neighbours, and roughly 20 living residents. Strange and quietly moving.",
     "The Oku-Iya double vine bridges, with a hand-hauled cable cart alongside.",
     "Mt Tsurugi — chairlift from 1,420 m to 1,750 m in fifteen minutes, gentle ridge walk "
     "at the top, second-highest peak in western Japan.",
     "THE FOLIAGE: at 1,955 m this is the only place on the trip that's turning while you're "
     "here.",
     "⚠️ NAGORO AND THE DOUBLE BRIDGES ARE NOT ALSO POSSIBLE TODAY — see the warning below. "
     "They are the alternative version of this day, not an addition to it."],
 travel="Train, then two buses with a change at Kubo, then the chairlift.",
 watch=["⚠️ NAGORO AND THE OKU-IYA DOUBLE BRIDGES CANNOT BE ADDED. They sit on this same "
        "road and every guide lists all three together — but that assumes a car. On buses "
        "there is ONE useful pair a day up to Minokoshi and back (10:20 up, 14:55 down), so "
        "stepping off at Nagoro means giving up the mountain. Pick one.",
        "You pass the vine-bridge stop again today. Kazurabashi Yumebutai is the interchange "
        "for everything deeper in the valley — you change buses there, you do not revisit it.",
        "This wing runs DAILY only between 1 Oct and 3 Nov. You're inside the window.",
        "Return on the 14:55 — the alternative gives you two minutes on the mountain.",
        "Peak colour is 25 Oct – 1 Nov, so you get the start of it.",
        "Carry food; there are no shops up there."],
 strand=[
  _S("The four-bus chain out of the valley — 14:55 down, then 17:41 is the last bus",
     "CONFIRMED",
     "Miyoshi City's own English sheet: Mt Tsurugi 14:55 → Kubo 15:45, Kubo 16:44 → "
     "Kazurabashi Yumebutai 17:30, Yumebutai 17:41 → 大歩危駅前 18:07, train 18:19. The only "
     "earlier return from the mountain is 11:12, which gives you two minutes up there. "
     "The sheet also states Mt Tsurugi buses run DAILY only 1 Oct–3 Nov, so this day "
     "exists solely because it falls inside that window.",
     check="Re-read the sheet after the 1 October 2026 revision, and confirm the daily "
           "window has not moved.",
     who="Awa-Ikeda Bus Terminal (Shikoku Kotsu) 0883-72-1231",
     by="Early October 2026.",
     fallback="None. No taxi rank at Minokoshi, nothing to walk to. If a bus is late, "
              "everything after it is lost.",
     links=["miyoshi_en", "jr_oboke"]),
 ],
 sleep="Awa-Ikeda — 4S STAY",
 alt_label="Mt Tsurugi and the chairlift",
 alts=[dict(NAGORO_ALT, legs=[l for l in NAGORO_ALT["legs"]
                              if "Awa-Ikeda" not in l[0] and "Awa-Ikeda" not in l[1]])],
 legs=[("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line",670),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","久保 Kubo","09:30","10:16","Shikoku Kotsu, Higashi-Iya line",750),
       ("久保 Kubo","剣山 Mt Tsurugi (Minokoshi)","10:20","11:10","Miyoshi City bus, 名頃線 — daily 1 Oct–3 Nov only",1380),
       ("Minokoshi 1,420 m","Nishijima 1,750 m and back","—","15 min each way","Mt Tsurugi chairlift",2300),
       ("剣山 Mt Tsurugi (chairlift base)","久保 Kubo","14:55","15:45","Miyoshi City bus, 名頃線 — last down of the day",1380),
       ("久保 Kubo","かずら橋夢舞台 Kazurabashi Yumebutai","16:44","17:30","Shikoku Kotsu, Higashi-Iya line",750),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","17:41","18:07","Shikoku Kotsu — LAST BUS of the day",670)]),

dict(date="2026-10-16", title="Kotohira, then north to Takamatsu",
 flow=[
  ("07:58 → 08:58", "阿波池田 Awa-Ikeda north out of the gorge to 琴平 Kotohira, about an hour "
   "on the Dosan Line. ⚠️ This fare is not published in any source I could reach — budget "
   "for it separately."),
  ("09:00 – 12:00", "KONPIRA-SAN. 785 steps to the main hall, 1,368 to the inner shrine, up a "
   "stone stairway lined with shops selling walking sticks and sweets. The grounds are FREE. "
   "The climb is entirely optional — the town and the first stretch are the pleasant part, "
   "and the walking sticks are lent, not sold. See the Walks tab before you commit."),
  ("09:00–17:00, last entry 16:30", "KANAMARU-ZA — the oldest surviving kabuki theatre in "
   "Japan, built 1835. You go backstage and work the revolving stage and the trapdoors by "
   "hand. ¥500, and the single most underrated thing in Kagawa."),
  ("open 1 Oct – 30 Nov", "THE TREASURE HOUSE is open on your dates (closed Tuesdays) — but "
   "the shrine does not publish its price. Ring 0877-75-2121 if it matters. The Takahashi "
   "Yuichi gallery is CLOSED in October."),
  ("afternoon", "Sanuki udon once you reach Kagawa — this is the prefecture that is famous "
   "for it — then north to Takamatsu. The Kotoden is cheaper than JR and drops you closer "
   "to the stairway."),
 ],
 do=["Konpira-san — the great sea-god shrine, reached by a stone stairway lined with shops. "
     "785 steps to the main hall, 1,368 to the inner shrine. Entirely optional; the town and "
     "the stairway's first stretch are pleasant on their own.",
     "Kanamaru-za, the oldest surviving kabuki theatre in Japan (1835). You can go backstage "
     "and work the revolving stage machinery by hand.",
     "Sanuki udon once you reach Kagawa."],
 travel="Local train north out of the gorge, then on to Takamatsu.",
 watch=["785 steps is the one genuine climb on this whole itinerary — and it's skippable.",
        "Palanquin carriers used to haul people up; that service has ended."],
 sleep="Takamatsu — WeBase hostel, Kawaramachi",
 legs=[("Awa-Ikeda","Kotohira","07:58","08:58","JR Dosan Line local train",None),
       ("Kotohira","Takamatsu","—","—","JR local via Tadotsu, or the cheaper Kotoden line",1470)]),

dict(date="2026-10-17", title="Ritsurin at dawn, the Gate in the Sky, then over to Shodoshima",
 flow=[
  ("06:00 – 09:30", "RITSURIN GARDEN AT FIRST LIGHT. It opens at 06:00 in October and a "
   "Takamatsu resident's advice is specifically to come in the morning — that is the light "
   "it was designed for. ¥500, flat paths, and two hours is the minimum."),
  ("before you go", "LEAVE THE BACKPACKS IN THE TAKAMATSU STATION LOCKERS and collect them "
   "on the way to the port tonight. You do not want them on the mountain."),
  ("10:13 → 11:16", "THE DIRECT RAPID WEST to 観音寺 Kan-onji, :13 past the hour, no "
   "surcharge. Then 20 minutes on foot to 有明グラウンド Ariake Ground, in Kotohiki Park."),
  ("from 09:00 — do this FIRST", "⚠️ BUY THE SHUTTLE TICKETS at the machine inside "
   "道の駅ことひき. ¥1,000 NOTES ONLY, 20 seats a departure, no reservations, and it sells "
   "out on fine days. You cannot buy at the stop."),
  ("11:30 up, 13:30 down", "TAKAYA SHRINE — the 天空の鳥居, a vermilion torii alone on the "
   "404 m summit with nothing behind it but the Inland Sea. ⚠️ No 12:30 or 15:00 going up, "
   "no 13:00 or 15:30 coming down. The gate is 150–200 m of steep slope above the drop-off."),
  ("~14:00", "ZENIGATA SUNAE — a 122-metre Edo coin raked into the sand of Kotohiki Park "
   "since 1633. Free, 24 hours, floodlit to 22:00, minutes from the shuttle stop."),
  ("evening", "Back east, collect the bags, and the ferry to 土庄港 Tonoshō — 15 a day, last "
   "20:20 → 21:20. ⚠️ Chichibugahama is NOT worth adding today: 14–17 October has no mirror window "
   "at all."),
 ],
 do=["RITSURIN GARDEN AT FIRST LIGHT — it opens at 06:00 in October, and a Takamatsu "
     "resident's advice is specifically to come in the morning. 300 years old, six ponds, "
     "thirteen hills, a borrowed-scenery mountain behind, flat paths throughout. ¥500.",
     "TAKAYA SHRINE — the 天空の鳥居, the 'Gate in the Sky'. A vermilion torii alone on the "
     "404-metre summit of Inazumiyama with only the Inland Sea behind it, so from the steps "
     "below it frames sky and water and nothing else. The most photographed thing in Kagawa "
     "and almost no foreign visitor gets there.",
     "ZENIGATA SUNAE — a 122-metre Edo coin raked into the sand of Kotohiki Park and re-raked "
     "by the town since 1633. Free, and a few minutes from the shuttle stop.",
     "Then the evening ferry across to Shodoshima."],
 travel="Garden at dawn, the 10:13 direct rapid west to Kan-onji, a 20-minute walk to the "
        "shuttle stop, up the mountain and back, then east again for the evening boat.",
 watch=["⭐ TODAY IS THE ONLY DAY ON THIS ITINERARY THAT TAKAYA WORKS. The shuttle runs on "
        "Saturdays, Sundays and public holidays ONLY, and today is the one Saturday you are "
        "within reach of Kan-onji. On a weekday the alternatives are a ¥3,600 taxi each way or "
        "a 50-minute climb.",
        "⚠️ SHUTTLE TICKETS CANNOT BE BOOKED. Buy from the vending machine at the tourism "
        "office inside 道の駅ことひき from 09:00 — ¥1,000 NOTES ONLY, 20 seats a departure, "
        "sells out on fine days. The machine is 5 minutes' walk from the stop and you cannot "
        "buy at the stop itself.",
        "⚠️ No 12:30 or 15:00 departure going up; no 13:00 or 15:30 coming down.",
        "The gate is 150–200 m further up a STEEP slope from the bus drop-off.",
        "LEAVE THE BACKPACKS in the Takamatsu station lockers and collect them on the way to "
        "the port. You do not want them on the mountain.",
        "This is the fullest day in Option B. If it is too much, drop Zenigata, or do Ritsurin "
        "yesterday evening — it is open to 17:30.",
        "Chichibugahama, the mirror beach 20 minutes further west, is NOT worth adding today: "
        "the official calendar gives 14–17 October no mirror window at all. See Option A, "
        "which catches it on the 12th.",
        "Do NOT book the Jumbo Ferry from Sakate — it docks at Takamatsu-HIGASHI port, "
        "15 minutes away from the walkable one. It's the most common mistake here.",
        "Ritsurin's foliage peaks 3 December; you'll see it green."],
 strand=[
  _S("The last ferry between Takamatsu and Shodoshima",
     "CONFIRMED",
     "Shikoku Ferry's own timetable, 15 sailings each way, 60 minutes, ¥700. LAST 高松発 "
     "20:20 → 土庄 21:20. LAST 土庄発 20:10 → 高松 21:10. ⚠️ AND A TRAP: the 土庄発 19:30 and "
     "the 高松発 15:10 are 危険物搭載車両の航送指定便 on WEEKDAYS — hazardous-cargo sailings that "
     "ORDINARY PASSENGERS CANNOT BOARD. On a weekday the real gap before the last boat is "
     "18:40 → 20:10.",
     check="Confirm both directions on the route page; ferry diagrams change with engine "
           "maintenance and the operator says so on the page.",
     who="Shikoku Ferry — ask at the Takamatsu or Tonoshō 乗り場",
     by="Before you set out that morning.",
     fallback="A high-speed boat (高速艇) also works this route and is a separate timetable. "
              "Otherwise it is a night on Shodoshima.",
     links=["sf_takamatsu"]),
 ],
 sleep="Tonoshō, Shodoshima",
 legs=[("Takamatsu","Ritsurin Kōen","every 15 min from 06:00","+7 min","Kotoden to Ritsurin-kōen — RAISED to ¥250 on 1 Oct 2026 (JR is ¥240)",250),
       ("Takamatsu","Kan-onji","10:13 (direct rapid, :13 past each hour)","11:16–11:29","JR Yosan Line rapid — no surcharge",1240),
       ("JR Kan-onji Stn","Ariake Ground (shuttle stop, in Kotohiki Park)","—","20 min","On foot",0),
       ("Ariake Ground","Takaya Shrine upper shrine","11:30","+25 min","Takaya Shrine shuttle bus — RETURN fare, Sat/Sun/holidays only",1500),
       ("Takaya Shrine","Ariake Ground","13:30 (no 13:00 run)","+25 min","Same shuttle — return included in the ¥1,500 above",None),
       ("Zenigata Sunae","Kotohiki Park viewpoint","—","few min from the shuttle stop","On foot — free, open 24 h",0),
       ("Kan-onji","Takamatsu","~1–2 per hour","+1h03–1h16","JR Yosan Line local train",1240),
       ("Takamatsu Port","Tonoshō Port","15/day, last 20:20 → 21:20","+60 min","Shikoku Ferry",700)]),

dict(date="2026-10-18", title="Kankakei Gorge, then the soy-sauce coast",
 book=["☎ NAKABU-AN — phone 0879-82-3669 THE DAY BEFORE. No online booking, no walk-up. "
       "If phoning in Japanese is daunting, ASK YOUR ACCOMMODATION TO RING FOR YOU; it is "
       "an ordinary favour and Japanese inns do it routinely.",
       "CLOSED Tue/Wed/Thu except public holidays. 18 Oct 2026 is a Sunday, so it is open."],
 do=["KANKAKEI GORGE by ropeway first thing — one of Japan's three great gorges, red rock "
     "spires, the Inland Sea opening out behind you.",
     "Then east to the 醤の郷, the soy-sauce village. YAMAROKU is a working brewery you walk "
     "straight into — free, no reservation, cedar barrels two storeys high and over a century "
     "old, furred with the wild yeast that makes the flavour.",
     "Fresh nama-somen at Nakabu-an in Yasuda — Shodoshima is one of Japan's three great "
     "somen regions, and this is the un-dried version you can barely get off the island."],

 flow=[
  ("07:35 → 08:14", "土庄港 Tonoshō Port across the island to 草壁港 Kusakabe Port on the "
   "Olive Bus Sakate line. Early, because everything today hangs off the 09:50 shuttle."),
  ("09:50 → 10:02", "THE FREE TOWN SHUTTLE up to 紅雲亭 Kouuntei, the ropeway base. It is a "
   "free town bus, 8 runs a day, running EVERY day in October — and it stops completely for "
   "the whole of November."),
  ("10:05 – 11:35", "KANKAKEI GORGE. Five minutes of cable car over red rock spires with the "
   "Inland Sea opening out behind you, then the summit walks. ¥2,340 return, cars every 12 "
   "minutes. ⚠️ The fare rises to ¥2,700 on 1 November."),
  ("11:40 → 12:09", "Shuttle down at 11:40, then the 12:02 Olive Bus two stops east to "
   "安田 Yasuda."),
  ("12:30 – 13:15", "NAKABU-AN — the somen workshop you booked yesterday. You stretch the "
   "dough between two chopsticks until it becomes hair-thin noodles, then eat what you made. "
   "45 minutes, ¥1,200. Their restaurant does nama-somen, the fresh un-dried kind you can "
   "essentially only eat on this island, from ¥750."),
  ("13:20 – 14:10", "YAMAROKU SOY SAUCE, three minutes' walk. A working brewery you walk "
   "straight into — free, no reservation, open to 17:00. Cedar barrels two storeys high and "
   "over a century old, furred with the wild yeast that makes the flavour. One of the last "
   "places in Japan still doing it this way."),
  ("14:16 → 14:48", "The westbound bus back to 土庄港 Tonoshō. Its Yasuda departure is not "
   "published separately; it passes Kusakabe at 14:16."),
 ],
 travel="Early bus across to Kusakabe, free shuttle up to the ropeway, back down for the "
        "12:30 somen session at Yasuda, then two stops east to the museum before it shuts, "
        "and one long ride west to Tonoshō.",
 watch=["Yamaroku is free, open to 17:00 and needs no reservation — the one soy-sauce stop "
        "worth making.",
        "BOOK NAKABU-AN THE DAY BEFORE — 0879-82-3669. CLOSED Tue/Wed/Thu except public "
        "holidays. Today is a Sunday, so it's open.",
        "The Kankakei shuttle is FREE, 8 runs a day, and runs every day in October — but stops "
        "completely for the whole of November.",
        "Don't buy the ¥1,600 day pass — today's singles come to about ¥1,600 exactly, so it "
        "breaks even at best.",
        "2026 is not a Setouchi Triennale year, so the island should be quiet.",
        "Foliage peaks 27 November — about six weeks after you."],
 sleep="Tonoshō, Shodoshima",
 legs=[("Tonoshō Port","Kusakabe Port","07:35","08:14","Olive Bus, Sakate Line",500),
       ("Kusakabe Port","Kouuntei (ropeway base)","09:50","10:02","FREE town shuttle, 12 min",0),
       ("Kankakei base","Summit and back","every 12 min","~5 min each way","Ropeway",2340),
       ("Kouuntei","Kusakabe Port","11:40","11:52","FREE town shuttle, 12 min",0),
       ("Kusakabe Port","Yasuda (安田)","12:02","12:09","Olive Bus, Sakate Line",200),
       ("Yasuda (安田)","Tonoshō Port","not published for Yasuda — the up-bus passes Kusakabe at 14:16","14:48","Olive Bus, Sakate Line",500)]),

dict(date="2026-10-19", title="Angel Road in the morning, then back to Takamatsu",
 flow=[
  ("07:22 – 13:22, and that is all",
   "⚠️ TODAY HAS ONLY ONE WINDOW. Most days give two; the operator's table shows no second "
   "window on 19 October 2026, so if you miss the morning there is no evening fallback and "
   "you will have stayed on the island for nothing. Check your own date at "
   "https://www.shikokuferry.com/angel"),
  ("half an hour on foot", "TO ANGEL ROAD from 土庄港 Tonoshō — faster than waiting for one of "
   "the five daily buses. A sandbar that surfaces at low water and links four islets; you "
   "walk out across the seabed and couples leave notes on shells. Free."),
  ("before 16:00–17:00", "THE SOY-SAUCE AND TSUKUDANI DISTRICT if the clock allows — it shuts "
   "between 16:00 and 17:00."),
  ("15/day", "THE FERRY back to 高松港 Takamatsu, an hour."),
 ],
 do=["Angel Road — the sandbar that surfaces at low tide and links four islets. Free, and "
     "genuinely lovely.",
     "The soy-sauce and tsukudani district if the clock allows."],
 travel="Half an hour on foot from Tonoshō port to the sandbar and back — faster than "
        "waiting for one of the five daily buses — then the ferry back in the afternoon.",
 watch=["⚠️ TODAY HAS ONLY ONE WINDOW: 07:22–13:22. Most days offer two, but the operator's "
        "own table shows no second window on 19 October 2026 — so if you miss the morning "
        "there is no evening fallback and you will have crossed to the island for nothing. "
        "Re-check the date before you travel: https://www.shikokuferry.com/angel",
        "The soy-sauce district shuts between 16:00 and 17:00."],
 strand=[
  _S("The last ferry between Takamatsu and Shodoshima",
     "CONFIRMED",
     "Shikoku Ferry's own timetable, 15 sailings each way, 60 minutes, ¥700. LAST 高松発 "
     "20:20 → 土庄 21:20. LAST 土庄発 20:10 → 高松 21:10. ⚠️ AND A TRAP: the 土庄発 19:30 and "
     "the 高松発 15:10 are 危険物搭載車両の航送指定便 on WEEKDAYS — hazardous-cargo sailings that "
     "ORDINARY PASSENGERS CANNOT BOARD. On a weekday the real gap before the last boat is "
     "18:40 → 20:10.",
     check="Confirm both directions on the route page; ferry diagrams change with engine "
           "maintenance and the operator says so on the page.",
     who="Shikoku Ferry — ask at the Takamatsu or Tonoshō 乗り場",
     by="Before you set out that morning.",
     fallback="A high-speed boat (高速艇) also works this route and is a separate timetable. "
              "Otherwise it is a night on Shodoshima.",
     links=["sf_takamatsu"]),
 ],
 sleep="Takamatsu — WeBase hostel",
 legs=[("Tonoshō Port","Takamatsu Port","15/day","+60 min","Shikoku Ferry",700)]),

dict(date="2026-10-20", title="The long one — right across Shikoku to Matsuyama",
 do=["Today is the journey. Five hours of slow train along the north coast, changing twice, "
     "with the Inland Sea out of the window for much of it.",
     "Arrive in time for Dogo Onsen in the evening — one of Japan's oldest hot springs and "
     "the model for the bathhouse in Spirited Away."],
 travel="All-local rail, 4.5–5 hours, two changes. The bus does it in 2h50 for ¥440 more, "
        "which is genuinely worth considering.",
 watch=["BUY A PAPER TICKET. IC cards only work in the Takamatsu area on this line and you "
        "won't be able to exit at the other end.",
        "Connection waits run 30–60 minutes. Bring food.",
        "Dogo's outdoor footbath is 'blisteringly hot, always'."],
 sleep="Matsuyama — Dogo Onsen area or near JR station",
 alt_label="All-local rail, 4.5–5 h, two changes",
 alts=[dict(label="Take the highway bus instead — 2 h 50 for ¥440 more",
  do=["The same crossing in half the time, sitting still the whole way, with the afternoon "
      "in Matsuyama instead of on a platform.",
      "This is the honest recommendation on this particular day. The all-local route is not "
      "scenic enough to be worth 4.5–5 hours and two changes with 30–60 minute waits; you "
      "are paying ¥440 to buy back the better part of a day.",
      "Arrive with time for DOGO ONSEN in daylight rather than at the end of a long haul."],
  travel="One bus, no changes, no ticket-gate problem at the far end.",
  watch=["⚠️ Book ahead if you can — Shikoku's highway buses are usually reservation-based, "
         "and this one is the reason Option B otherwise loses a day.",
         "The ¥440 difference is per person. For two people it is ¥880 to buy back roughly "
         "two hours each — the best value on the whole itinerary.",
         "The rail alternative is the default above if you would rather have the window."],
  legs=[("Takamatsu","Matsuyama","—","+2 h 50","Highway bus — ¥440 more than the all-local rail",4400)])],
 legs=[("Takamatsu","Matsuyama","—","+4.5–5 h, 2 changes","JR Yosan Line, all local trains",3960)]),

dict(date="2026-10-21", title="Matsuyama Castle, or a day out instead",
 do=["MATSUYAMA CASTLE — one of only twelve original keeps left in Japan, on a hill in the "
     "middle of the city, with a connected-keep layout whose walls you can walk. The views "
     "over the Inland Sea are the real point.",
     "NINOMARU GARDEN below it, built over the old lord's residence. ¥200, flat, and the "
     "quiet counterweight to the castle.",
     "DOGO ONSEN in the evening if you didn't get your fill of it, or the arcade for dinner.",
     "Be honest with yourself about the scale of this: the castle is a half-day. If that "
     "sounds thin, switch this day to one of the alternatives — that is what they are for."],
 travel="Trams around town, and a chair lift up the castle hill. Nothing today needs a timetable.",
 watch=["Take the CHAIR LIFT rather than the ropeway — same ticket, same price, much shorter "
        "queue, and it is the nicer ride.",
        "⚠️ You do NOT have to go inside the keep. It is steep narrow ladder-stairs climbed in "
        "socks, and the exterior, the walls and the view are what people come for. The "
        "grounds cost nothing; the keep is ¥520.",
        "Allow ~30 min from the lift station to the ticket window — the castle's own site "
        "says budget about an hour in total before you are actually inside.",
        "Buy water before going up; drinks cost more at the top.",
        "✅ Matsuyama accepts Suica — the one place in Shikoku that reliably does, and here "
        "it PAYS: Iyotetsu raised the tram to ¥250 flat on 1 April 2026, but the cashless "
        "discount takes ¥20 off, so tapping IC costs the old ¥230. Tap, don't pay cash."],
 sleep="Matsuyama",
 alt_label="Matsuyama Castle and the city",
 alts=MATSUYAMA_ALTS,
 legs=[("Castle hill","up and back","—","3 min each way","Chair lift",520),
       ("City trams","—","—","—","Iyotetsu tram, flat fare — ¥250 cash, ¥230 if you tap IC",250)]),

dict(date="2026-10-22", title="The Shimanami Kaido — island-hopping to Onomichi",
 flow=SHIMANAMI_BUS_FLOW,
 do=["Six islands and seven suspension bridges across the Inland Sea, back to Honshu. One of "
     "the great scenic routes in Japan even from a bus seat.",
     "OPTIONAL: bus out to one island, rent a bike, ride a bridge or two on the cycleway, "
     "ferry back. Bridge tolls waived for cyclists until 2028.",
     "Onomichi — a steep temple town of alleys and cats above a working strait."],
 travel="Local train up the coast, then bus across the islands with one change.",
 watch=["No direct Imabari–Onomichi bus — change at Innoshima Ōhashi, and the operator warns "
        "the connection can involve a long wait.",
        "Don't attempt all 70 km by bike; every bridge has a climbing ramp."],
 sleep="Onomichi — Guesthouse Yadocurly",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari","Onomichi","hourly connections","+1.5–2 h","Shimanami Liner + local bus",2390)]),

dict(date="2026-10-23", title="Rabbit island, then Hiroshima",
 flow=RABBIT_FLOW,
 do=["ŌKUNOSHIMA — around a thousand feral rabbits that mob you when you sit down, and a "
     "sober museum about the poison gas the island secretly made for the Imperial Army. "
     "Ruined batteries stand in the woods.",
     "Optional hour: Takehara, an Edo merchant town 12 minutes from its station."],
 travel="Two slow trains along the coast, then a 15-minute ferry.",
 watch=["BUY RABBIT FOOD BEFORE BOARDING — none sold on the island. ~¥200 at the shop by the "
        "station. PELLETS, not vegetables.",
        "Ferry is CASH ONLY.",
        "Don't pick the rabbits up — they panic and break bones, and there's no vet.",
        "Allow 4–5 hours.",
        "Bag storage ¥500 at the port."],
 strand=[
  _S("The last boat OFF Ōkunoshima — this plan's '18:30' does not match the operator",
     "UNVERIFIED",
     "大三島フェリー's timetable gives the last call at 大久野島 heading to 忠海 as ※17:16, "
     "arriving 17:30 — and the ※ means that sailing serves the island only FEBRUARY TO "
     "OCTOBER. The next boat, 18:40 from 盛, does NOT stop there at all. A SECOND operator "
     "(休暇村客船) also works the route and is probably where '18:30' and 'every 30–45 min' "
     "came from, but its site is behind a bot wall and could NOT be read.",
     check="ONLINE: the 大三島フェリー timetable below is readable now and gives 17:16 — take "
           "that as your working deadline. Its 運航情報 notices sit on the same page, so "
           "check them too (the second jetty has closed for repairs before). The second "
           "operator's page is bot-walled from here but may open in a normal browser — "
           "try it, and if it loads, read its last sailing.",
     who="NO PHONE CALL NEEDED IF YOU DO ONE THING: confirm the last sailing AT THE "
         "TADANOUMI TICKET WINDOW when you buy, and ask which operator it is — a "
         "face-to-face question with a printed timetable in front of you. Only if you "
         "want certainty in advance, have your hotel ring 休暇村大久野島 0846-26-0321.",
     by="On the morning, at the port, before you cross.",
     fallback="NONE. One hotel on the island and no other way off. The operator warns of "
              "delays at busy times and its second jetty has been closed for repairs before.",
     links=["omishima_time", "qkamura_ohkuno", "rabbit_island"]),
 ],
 sleep="Hiroshima — The Evergreen Hostel or J-Hoppers",
 legs=[("Onomichi","Mihara","not published","not published","JR Sanyo Line local train",None),
       ("Mihara","Tadanoumi","—","+22 min","JR Kure Line local train",320),
       ("Tadanoumi Port","Ōkunoshima and back","every 30–45 min, last out 18:30","+15 min each way","Ferry — CASH ONLY",720),
       ("Tadanoumi Port","bag storage","—","—","¥500 per bag per day",500),
       ("Tadanoumi","Hiroshima Bus Centre","4 round trips/day","+1h40","Geiyo Bus 'Kaguya-hime'",1500)]),

dict(date="2026-10-24", title="Miyajima",
 flow=MIYAJIMA_FLOW,
 do=["The floating torii at Itsukushima — in the sea at high tide, walkable across the seabed "
     "at low. Below 100 cm you can walk out, above 250 cm it floats. October tide table: "
     "https://www.miyajima.or.jp/sio/sio10.html",
     "Itsukushima Shrine, on stilts over the water since the 12th century.",
     "Ropeway up Mt Misen for the panorama; wild deer and Daishō-in temple on the way.",
     "Momiji manjū, made fresh in front of you along the main street."],
 travel="Tram to the pier, 10-minute ferry. One pass covers everything.",
 watch=["The Hiroden ¥1,000 day pass covers trams + ferry + the ¥100 visitor tax, and cuts "
        "the ropeway to ¥1,500.",
        "Ride the JR ferry out between 9:10 and 16:10 for the free close pass by the torii.",
        "The summit is ~30 min further up a steep stepped trail beyond the ropeway — optional.",
        "Last ascent 16:00.",
        "The Reikadō hall burned down in May 2026.",
        "Momijidani was recorded completely green on 12 October 2025."],
 sleep="Hiroshima",
 legs=[("Hiroshima","Miyajima + all city trams","—","—","Hiroden 1-day tram & ferry pass",1000),
       ("Momijidani","Shishiiwa (Mt Misen)","last ascent 16:00","+~20 min each way","Ropeway — ¥1,500 with the pass",1500)]),

dict(date="2026-10-25", title="Peace Memorial Park, then on to Kyushu",
 do=["The Peace Memorial Museum and the A-Bomb Dome. Allow more time than you think.",
     "Hiroshima-style okonomiyaki before you go."],
 travel="Everything central; trams are a flat ¥240.",
 watch=[],
 sleep="→ Kyushu",
 legs=[]),
])

OPTIONS = {"A": A, "B": B}

# ─────────────────────────────────────────────────────────────────────────────
# OPTION A2 — Option A with a second Tokushima night, bought for free.
#
# The traveller asked whether east Tokushima deserves two nights. The answer is
# yes, and for one dated reason: 14 October 2026 is a 大潮 SPRING TIDE at Naruto,
# with the operator's own viewing window running 12:30–16:30 — squarely inside
# Uzu-no-michi's October opening. That is as good as the whirlpools get, and
# Option A currently spends the day on a train instead.
#
# The night is NOT taken out of Iya. Option A's vine-bridge day carries
# 11:00–15:11 of forced dead time (the return buses are what they are), and its
# 17 October is a travel day with an empty morning. Fold the bridge into that
# morning and the whole block closes up one day shorter with nothing lost but
# loitering — and Kōchi's Sunday market, the reason Option A exists, stays on
# Sunday.
#
# Built by transforming A rather than copy-pasting it, so the two cannot drift.

def _make_A2():
    import copy
    a2 = copy.deepcopy(A)
    a2["key"] = "A2"
    a2["name"] = "Option A2 — Option A plus Naruto, on a spring tide"
    a2["verdict"] = (
        "Option A with a second night in Tokushima, spent on the Naruto whirlpools on "
        "the one date this trip touches a 大潮 spring tide. It costs no Iya day and no "
        "Kōchi Sunday market: the vine bridge moves into the 17th's empty morning, which "
        "was dead time anyway. ¥3,000 a head more than Option A in fares and tickets, "
        "plus ¥3,300 if you do the Ōtsuka Museum; the beds are a wash, since a Tokushima "
        "night replaces an Awa-Ikeda one. Take this unless you want the slower "
        "vine-bridge day more than you want the whirlpools.")
    days = a2["days"]
    i = next(n for n, d in enumerate(days) if d["date"] == "2026-10-14")
    assert "Ōboke" in days[i]["title"], days[i]["title"]
    assert "vine bridge" in days[i + 1]["title"], days[i + 1]["title"]
    assert "Tsurugi" in days[i + 2]["title"], days[i + 2]["title"]
    assert "Kōchi" in days[i + 3]["title"], days[i + 3]["title"]

    # The 13th stops being "the rest day before the mountains" — tomorrow is Naruto.
    d13 = days[i - 1]
    assert d13["date"] == "2026-10-13"
    d13["flow"] = [(w, t.replace("Nothing today is tight — this is the rest day before the "
                                "mountains.",
                                "Nothing today is tight. Do the DAYTIME show today and keep "
                                "the evening one for tomorrow, when you get back from Naruto."))
                   for w, t in d13["flow"]]
    d13["watch"] = ["Nothing tricky today — but read tomorrow's tide note tonight, because "
                    "tomorrow is built around it.",
                    "The 3-in-1 set (museum + day show + ropeway) is ¥2,640 against ¥3,300 "
                    "bought separately, per person."]

    # A's Ōboke-boat day slides one day later, unchanged in every other respect.
    oboke = copy.deepcopy(days[i])
    oboke["date"] = "2026-10-15"

    # 16 Oct keeps Mt Tsurugi, but gains Option A's ORIGINAL unhurried vine-bridge
    # day as a third choice — built from A's own day rather than rewritten, so the
    # two cannot drift. Taking it here means the 17th becomes one of its easy
    # variants, which is the point: the traveller decides how tight they want the
    # departure morning to be, on the night before, knowing the weather.
    vine = copy.deepcopy(days[i + 1])             # A's 15 Oct vine-bridge day
    tsurugi = copy.deepcopy(days[i + 2])          # 16 Oct
    tsurugi["alts"] = list(tsurugi.get("alts", [])) + [dict(
        vine,
        label="The vine bridge today instead — unhurried, and it frees the 17th",
        watch=["⭐ TAKE THIS IF YOU WANT AN EASY DEPARTURE MORNING. Doing the bridge today "
               "means the 17th becomes 'a slow morning at Ōboke' or the 08:15 straight to "
               "Kōchi — no bus deadline on a day you are also carrying luggage.",
               "The cost is Mt Tsurugi, which is the single best thing in the valley and "
               "the one day of the trip with foliage actually turning. Do not trade it "
               "away lightly.",
               "⚠️ THE LAST BUS BACK TO ŌBOKE IS 17:41. There is no later one and no taxi "
               "rank.",
               "⚠️ THE 15:11 BUS IS A TRAP. It reaches 大歩危駅前 at 15:32, fifteen minutes "
               "after the 15:17 train, so it costs you two hours on an unstaffed platform. "
               "The 14:16 gets you the 15:17.",
               "The buses take cash only — coins and ¥1,000 notes.",
               "This is a long, slow day: 11:00–15:11 in the valley with nothing timetabled. "
               "That is the trade for the unhurried version."])]


    naruto = dict(date="2026-10-14", title="Naruto — the whirlpools on a spring tide",
 do=["THE NARUTO WHIRLPOOLS from the glass-floored walkway slung under the Ōnaruto Bridge, "
     "and from a boat in among them if you want both.",
     "THE ŌTSUKA MUSEUM OF ART by the bridge — full-size ceramic reproductions of a "
     "thousand Western masterpieces, one of the strangest museums anywhere.",
     "Back in Tokushima for the Awa Odori EVENING show, generally rated above the daytime "
     "one, or Mt Bizan after dark."],
 flow=[
  ("why today, and not another day",
   "TODAY IS A 大潮 SPRING TIDE. Both of today's times are whirlpool windows — at Naruto, "
   "unlike a sandbar or a torii, the water level reveals nothing; what the tide sets is how "
   "hard the strait runs, and it runs hardest around BOTH turning points. The operator "
   "publishes 満潮 08:00 (北流, flowing north) and 干潮 14:30 (南流, flowing south), and its own "
   "rule is 「観潮には、この時刻を中心に、大潮は前後２時間、中潮は前後１時間半、小潮は前後１時間までが"
   "最適です」 — so the windows are 06:00–10:00 and 12:30–16:30. The afternoon one sits "
   "squarely inside Uzu-no-michi's October opening — the morning one overlaps it by an "
   "hour — which is why the day is shaped this way. It also happens to be the 南流, which "
   "local sources rate the stronger of the two, though the boat operator says neither is "
   "inherently bigger. Re-check your own date: https://www.uzunomichi.jp/tide-calendar/"),
  ("08:10 → 09:30",
   "THE BUS TO THE MUSEUM. 徳島駅前 to 大塚国際美術館前, ¥720. ⚠️ CASH ONLY — the operator's "
   "own fare sheet says IC cards do not work on board; the on-board changer takes ¥100 and "
   "¥500 coins and ¥1,000 notes only."),
  ("09:30 – 12:15",
   "THE ŌTSUKA MUSEUM OF ART, which opens at 09:30. ¥3,300 on the day, ¥3,160 bought in "
   "advance — the most expensive admission on the whole trip, per person. Travellers "
   "report about two hours as the average stay; it is a three-hour museum if you let it "
   "be. Closed Mondays, so today (a Wednesday) is fine."),
  ("12:18 → 12:31",
   "UP TO THE PARK. Thirteen minutes on the same bus line, ¥110. There is also a 13:00 → "
   "13:13 if the museum holds you."),
  ("12:30 – 16:30, the spring-tide window",
   "UZU-NO-MICHI — a 450-metre walkway slung under the road deck with glass floor panels "
   "45 metres directly above the churn. ¥510, 09:00–17:00 in October, last entry 16:30. "
   "Allow an hour. AND/OR THE BOAT: Wonder Naruto is ¥2,000, 12 sailings 09:00–16:20, no "
   "reservation needed, and puts you in among them rather than above them. The Aqua Eddy "
   "has an underwater window but DOES need booking."),
  ("your bags are not a problem",
   "Uzu-no-michi and the Eddy hall next door both have FREE coin lockers, open to closing "
   "time, and take cases too big for them at the counter for ¥400 a day."),
  ("16:25 → 17:51",
   "BACK TO TOKUSHIMA. ⚠️ Only EIGHT return runs a day come all the way through to "
   "徳島駅前; the rest stop at 鳴門駅前. The through departures from 鳴門公園 are 10:25, 12:45, "
   "13:25, 14:45, 15:45, 16:25, 17:00 and 17:45, and 17:45 → 19:18 is the last."),
  ("20:00, if you have the legs",
   "THE AWA ODORI EVENING SHOW, ¥1,600, a different famous troupe each night and generally "
   "rated above the daytime one. It ends about 20:50. The Bizan ropeway runs to 21:00 "
   "until 31 October if you would rather have the night view."),
 ],
 travel="One bus out along the coast and one back, about ninety minutes each way. Nothing "
        "else moves today.",
 watch=["⭐ THE TIDE IS THE DAY. 14 October is 大潮 — the strongest tide grade — with the "
        "afternoon window running 12:30–16:30. On a neap tide the same visit gives you an "
        "hour and much less to look at.",
        "⚠️ THE BUS IS CASH ONLY and there are only eight through-runs back to Tokushima. "
        "Last one leaves 鳴門公園 at 17:45.",
        "⚠️ ŌTSUKA IS ¥3,300 A HEAD and ticket sales stop at 16:00. If that is not your "
        "kind of museum, the alternative morning is TEMPLES 1–5 of the 88-temple "
        "pilgrimage — flat, fully signposted, free, and the classic first day for henro "
        "pilgrims. Then go out to Naruto after lunch for the same tide window.",
        "The Uzu-no-michi + Eddy combined ticket is ¥900 against ¥1,130 bought separately."],
 strand=[
  _S("The last bus back from Naruto Park to Tokushima",
     "CONFIRMED",
     "Read off Tokushima Bus's own timetable, revised 1 April 2026. Only EIGHT runs a "
     "day come through to 徳島駅前 — 鳴門公園 dep 10:25, 12:45, 13:25, 14:45, 15:45, 16:25, "
     "17:00 and 17:45. The 17:45 → 19:18 is the last. Every other run terminates at "
     "鳴門駅前, which is a different place and a different evening.",
     check="Re-read the PDF before you go; Tokushima Bus revises on 1 April and 1 October "
           "and you travel a fortnight after a revision date.",
     who="徳島バス 088-622-1826",
     by="Early October 2026.",
     fallback="If you miss the 17:45, get any bus to 鳴門駅前 and take JR from 鳴門 via "
              "池谷 into Tokushima — slower, but it exists. Do not rely on it after dark.",
     links=["tokubus_naruto", "tokubus_narutofare"]),
 ],
 sleep="Tokushima — Hostel PAQ, 8 min walk from the station",
 legs=[("徳島駅前 Tokushima Stn","大塚国際美術館前 Ōtsuka Museum","08:10","09:30","Tokushima Bus, Naruto Park line — CASH ONLY, no IC",720),
       ("大塚国際美術館前 Ōtsuka Museum","鳴門公園 Naruto Park","12:18 (or 13:00)","12:31 (or 13:13)","Same bus line — 13 min",110),
       ("鳴門公園 Naruto Park","渦の道 Uzu-no-michi glass walkway","—","—","Walkway under the bridge",510),
       ("亀浦観光港 Kameura Port","Whirlpool cruise","12 sailings 9:00–16:20","+~30 min","Wonder Naruto (no reservation needed)",2000),
       ("鳴門公園 Naruto Park","徳島駅前 Tokushima Stn","16:25 (last through-bus 17:45)","17:51 (19:18)","Tokushima Bus — only 8 through-runs a day",720)])

    bridge_kochi = dict(date="2026-10-17",
 title="The vine bridge in the morning, then down the gorge to Kōchi",
 do=["IYA KAZURABASHI and BIWA FALLS before lunch, then the Dosan Line south.",
     "The ride itself — the line below Ōboke is switchbacks, tunnels and river crossings, "
     "and you are on it for a couple of hours.",
     "Hirome Market in the evening: about sixty stalls, shared tables. Order katsuo no "
     "tataki, bonito seared over burning rice straw."],
 flow=[
  ("07:45 → 08:14",
   "DOWN TO ŌBOKE ON THE FIRST LOCAL, with the bags. Two ways to handle them, and they "
   "lead to different afternoons — pick one now, at the ticket machine, not at 12:30. "
   "EITHER stash them in Ōboke's lockers (⚠️ every one is ¥500, COINS ONLY, the station "
   "has been unstaffed since 2010 and there is no change machine — break a note at the "
   "Awa-Ikeda 7-Eleven first) OR leave them at Awa-Ikeda's ¥400 lockers and use the "
   "alternative return below."),
  ("08:58 → 09:19",
   "THE BUS TO KAZURABASHI, ¥670. Cash only — coins and ¥1,000 notes. There is nothing up "
   "the valley to break a note at."),
  ("09:20 – 11:45",
   "IYA KAZURABASHI — 45 metres of woven mountain vine hanging 14 metres above the river, "
   "rebuilt every three years, with the slats spaced wide enough to see straight down "
   "between them. Legend says the Heike built these so they could cut them behind "
   "themselves. Five minutes from the bus stop. Then BIWA FALLS, a 50-metre waterfall "
   "literally fifty metres to your left as you step off the bridge. Lunch at the "
   "michi-no-eki: Iya soba, which is what a valley too steep to grow rice eats instead."),
  ("12:11 → 12:32",
   "THE 12:11 BUS OUT, and take it rather than the 13:11. Both reach 大歩危駅前 in time for "
   "the 14:22, but the 13:11 arrives at 13:32 with no margin at all and the 14:22 is the "
   "last thing that gets you to Kōchi today."),
  ("14:22 →",
   "THE DOSAN LINE SOUTH. ⚠️ ONLY TWO LOCAL TRAINS A DAY RUN THROUGH TO KŌCHI — 08:15 and "
   "14:22. This leg IS the sightseeing; there is nothing to do but look out of the window."),
  ("the bags-at-Awa-Ikeda variant",
   "If you left the bags at Awa-Ikeda instead: same 12:11 bus, then 大歩危 12:58 → "
   "Awa-Ikeda, collect them, and take the 13:49 Awa-Ikeda → Kōchi local. Same evening in "
   "Kōchi, no coin problem, and one more train."),
  ("on arrival",
   "⚠️ KŌCHI DOES NOT TAKE NATIONAL IC CARDS — it has its own, Iruca. Cash from here on, "
   "for buses, trams and JR."),
 ],
 travel="First local down the valley, the one bus line that serves the vine bridge, back "
        "out by lunchtime, and then two hours south through the gorge.",
 watch=["⚠️ THE 14:22 IS THE DEADLINE, and the 12:11 bus is what protects it. The 13:11 "
        "reaches 大歩危駅前 at 13:32 and still works, but with no slack; the next bus after "
        "that is 14:16 → 14:37, which is fifteen minutes too late.",
        "⚠️ Miss the 14:22 and there is no later through-train — you are in the valley for "
        "the night.",
        "The valley buses are CASH ONLY — coins and ¥1,000 notes.",
        "What you give up against Option A: about two hours of loitering at the bridge and "
        "the flat 1 km Ōboke station lookout loop. That is the entire cost of the extra "
        "Naruto day.",
        "Kōchi does not accept national IC cards. Cash from here on.",
        "Hirome Market divides people: 'very crowded and loud', 'I got overstimulated'. The "
        "stalls just outside are calmer."],
 strand=[
  _S("The 14:22 out of Ōboke — the last through-train to Kōchi",
     "CONFIRMED",
     "JR Shikoku's Ōboke departure board: only TWO local trains a day run through to "
     "Kōchi, 08:15 and 14:22, and neither carries a 土休日運休 marker. The 12:11 bus off "
     "the vine bridge is what protects the 14:22 — it reaches 大歩危駅前 at 12:32. The "
     "13:11 also works, at 13:32, with no margin. The NEXT bus, 14:16 → 14:37, is "
     "fifteen minutes too late.",
     check="Re-read the Ōboke board after the 1 October 2026 revision.",
     who="Awa-Ikeda Bus Terminal (Shikoku Kotsu) 0883-72-1231 for the bus; JR Shikoku "
         "for the train",
     by="Early October 2026.",
     fallback="Miss the 14:22 and there is no later through-train — the 18:19 only "
              "reaches Tosa-Yamada. You would be in the valley for the night. Ōboke has "
              "been unstaffed since 2010.",
     links=["jr_oboke", "miyoshi_en"]),
 ],
 alt_label="The vine bridge, then the 14:22",
 alts=[
  dict(label="Skip the valley — the 08:15 straight to Kōchi, half a day extra there",
   do=["THE 08:15, the other of the day's two through-trains, putting you in Kōchi around "
       "lunchtime instead of late afternoon.",
       "KŌCHI CASTLE in the afternoon with time to spare — one of only twelve original "
       "keeps left in Japan, and the ONLY one where the lord's residence also survives.",
       "This is the honest choice if the weather is bad, if the vine bridge does not "
       "excite you, or if three days of Iya buses have been enough. The bridge is 45 m of "
       "woven vine over a river; it is lovely and it is also twenty minutes."],
   travel="One local train, 08:15 from Ōboke, no buses at all.",
   watch=["✅ THIS IS THE LOW-RISK VERSION OF TODAY. No bus chain, no 12:11 deadline, and "
          "the day cannot strand you.",
          "You still leave Awa-Ikeda on the 07:45 — the 08:15 from Ōboke IS that train "
          "continuing south, so there is no earlier start and no change.",
          "⚠️ Kōchi does NOT take national IC cards. Cash from here on.",
          "Doing this means you never see the vine bridge on this trip. Option A keeps it "
          "as a whole day if that is the wrong trade."],
   sleep="Kōchi — central, near Hirome Market",
   legs=[("Awa-Ikeda","Ōboke","07:45","08:14","JR Dosan Line local train",530),
         ("Ōboke","Kōchi","08:15","not published","JR Dosan Line local (2 through-trains a day)",1430)]),
  dict(label="A slow morning at Ōboke instead — no buses, no deadline",
   do=["A LATE START. Stay at Awa-Ikeda, take the 12:11 down, and give the morning to "
       "doing nothing — which after Mt Tsurugi is a real option, not a wasted one.",
       "THE ŌBOKE STATION LOOKOUT LOOP, a flat 1 km round trip above the gorge with its "
       "trailhead on the Walks tab, and lunch at the michi-no-eki (the YOKAI house is "
       "there too).",
       "Then the same 14:22 south."],
   travel="One local down at 12:11, a flat walk, and the 14:22 out. Nothing is timed but "
          "the last train.",
   watch=["✅ NO BUSES AT ALL TODAY, so nothing can go wrong except the 14:22 itself — and "
          "you are at the station from 12:50.",
          "⚠️ The 14:22 is still the last through-train to Kōchi. The 08:15 is the only "
          "other one.",
          "This is Option A's original shape for this day. Take it if the Tsurugi day "
          "wore you out."],
   sleep="Kōchi — central, near Hirome Market",
   legs=[("Awa-Ikeda","Ōboke","12:11","12:50","JR Dosan Line local train",530),
         ("Ōboke","Kōchi","14:22","not published","JR Dosan Line local (2 through-trains a day)",1430)]),
 ],
 sleep="Kōchi — central, near Hirome Market",
 legs=[("Awa-Ikeda","Ōboke","07:45","08:14","JR Dosan Line local train",530),
       ("大歩危駅前 Ōboke-ekimae (in front of JR Ōboke)","かずら橋夢舞台 Kazurabashi Yumebutai","08:58","09:19","Shikoku Kotsu, Iya line — CASH ONLY",670),
       ("かずら橋夢舞台 Kazurabashi Yumebutai","大歩危駅前 Ōboke-ekimae","12:11 (not the 13:11)","12:32","Shikoku Kotsu, Iya line — CASH ONLY",670),
       ("Ōboke","Kōchi","14:22","not published","JR Dosan Line local (2 through-trains a day)",1430)])

    days[i:i + 4] = [naruto, oboke, tsurugi, bridge_kochi]
    return a2

A2 = _make_A2()
OPTIONS["A2"] = A2


# ─────────────────────────────────────────────────────────────────────────────
# OPTION A3 — Option A with Kōchi swapped out for Kotohira.
#
# Kōchi is the most expensive and most fragile part of Option A: a ¥1,430 local
# that runs through only twice a day to get in, and a ¥4,000 reservation-only
# highway bus to get out, because the all-rail alternative is a ten-hour run on
# one daily 05:39 departure. Dropping it costs you the Sunday market — which is
# genuinely one of the best things in Shikoku — and buys back a day, several
# thousand yen, and the two sights Option A otherwise misses entirely.
#
# Built by transforming A rather than copy-pasting it, so the two can never
# drift. Everything after the swap shifts one day earlier.

def _make_A3():
    import copy, datetime
    a2 = copy.deepcopy(A)
    a2["key"] = "A3"
    a2["name"] = "Option A3 — Option A without Kōchi, via Kotohira instead"
    a2["verdict"] = (
        "Option A with its weakest link removed. You lose Kōchi's 300-year-old Sunday "
        "market and the castle, and you gain Konpira-san, the oldest kabuki theatre in "
        "Japan, a night in an onsen town, one day back and at least ¥3,100 a head. Take "
        "this unless the Sunday market is the thing you came for.")
    days = a2["days"]
    i = next(n for n, d in enumerate(days) if d["date"] == "2026-10-17")
    assert "Kōchi" in days[i]["title"] and "Kōchi" in days[i + 1]["title"]

    swap = [
dict(date="2026-10-17", title="North out of the gorge to Kotohira, and an onsen-town night",
 flow=[
  ("07:58 → 08:58",
   "阿波池田 Awa-Ikeda north out of the gorge to 琴平 Kotohira, about an hour on the Dosan "
   "Line. ⚠️ This fare is not published in any source I could reach — budget for it "
   "separately at the window."),
  ("09:00 – 12:00",
   "KONPIRA-SAN. 785 steps to the main hall, 1,368 to the inner shrine, up a stone stairway "
   "lined with shops selling walking sticks and sweets. The grounds are FREE and the climb "
   "is entirely optional — the town and the first stretch are the pleasant part, and the "
   "walking sticks are lent, not sold. See the Walks tab for what the stairway involves."),
  ("09:00–17:00, last entry 16:30",
   "KANAMARU-ZA — the oldest surviving kabuki theatre in Japan, built 1835. ¥500, and you go "
   "backstage and work the revolving stage and the trapdoors by hand. This is the thing "
   "Option A misses entirely."),
  ("open 1 Oct – 30 Nov",
   "THE TREASURE HOUSE is open on your dates and closed Tuesdays — but the shrine publishes "
   "no price for it. Ring 0877-75-2121 if it matters. The Takahashi Yuichi gallery is CLOSED "
   "in October."),
  ("evening",
   "AN ONSEN-TOWN NIGHT, which is the real reason to sleep here rather than pushing on."),
 ],
 do=["KONPIRA-SAN — the great sea-god shrine at the top of a stone stairway lined with "
     "shops selling walking sticks and sweets. 785 steps to the main hall, 1,368 to the "
     "inner shrine. The grounds are FREE, and the climb is entirely optional: the town and "
     "the first stretch of the stairway are the pleasant part.",
     "KANAMARU-ZA — the oldest surviving kabuki theatre in Japan, built 1835. You go "
     "backstage and work the revolving stage and the trapdoors by hand. ¥500, and it is the "
     "single most underrated thing in Kagawa.",
     "An onsen-town evening, which is what the night here is really for."],
 travel="One local train north out of the gorge, about an hour, and you are at the bottom "
        "of the stairway. Nothing today is timetable-critical after that.",
 watch=["The 785 steps are the only real climb on this itinerary and they are skippable — "
        "see the Walks tab for what the stairway actually involves.",
        "The palanquin carriers who used to haul people up have stopped operating.",
        "The Treasure House is open 1 Oct–30 Nov and closed Tuesdays, so it IS open today — "
        "but the shrine does not publish its price. Ring 0877-75-2121 if it matters.",
        "⚠️ The Awa-Ikeda → Kotohira fare is not published in any source I could reach. "
        "Budget for it separately; the ride is about an hour on the Dosan Line."],
 sleep="Kotohira — onsen ryokan (Kotohira Park Hotel, Onyado Shikishimakan)",
 legs=[("Awa-Ikeda","Kotohira","07:58","08:58","JR Dosan Line local train",None)]),

dict(date="2026-10-18", title="Right across to Matsuyama, on the west coast, and Dogo Onsen",
 flow=[
  ("leave early", "THE LONG TRANSFER OF THIS ITINERARY: across the top of Shikoku on the "
   "Yosan Line, 4.5–5 hours on locals with two changes. Treat it as a rest day and start it "
   "early rather than clawing at the evening."),
  ("before you board", "⚠️ BUY A PAPER TICKET. IC cards only work in the Takamatsu area on "
   "this line and you will not be able to exit at Matsuyama."),
  ("en route", "CONNECTION WAITS RUN 30–60 MINUTES and several changes are at stations with "
   "nothing at all. Carry food and something to read."),
  ("06:00–23:00 on arrival", "DOGO ONSEN HONKAN — one of the oldest hot springs in Japan, "
   "named in 8th-century chronicles, the model for the bathhouse in Spirited Away, and "
   "finally out of scaffolding since July 2025. ¥700 for the ground-floor Kami-no-Yu. Wash "
   "thoroughly at the taps FIRST, no swimwear, small towel out of the water."),
  ("if the queue is long", "飛鳥乃湯泉 ASUKA-NO-YU next door is ¥610, newer and much quieter."),
  ("evening", "The arcade between the tram stop and the bathhouse. The footbath outside is, "
   "in every account, 'blisteringly hot, always'."),
 ],
 do=["DOGO ONSEN — one of the oldest hot springs in Japan, named in 8th-century chronicles "
     "and the model for the bathhouse in Spirited Away. The restoration finished in July "
     "2025, so you see it without scaffolding for the first time in years. ¥700 for the "
     "ground-floor bath.",
     "The Botchan Train, a replica Meiji steam locomotive that still runs through the "
     "streets.",
     "The arcade between the tram stop and the bathhouse — the right place for dinner."],
 travel="The long transfer of this itinerary: across the top of Shikoku on the Yosan Line, "
        "4.5–5 hours on locals with two changes. Leave early and treat it as a rest day.",
 watch=["⚠️ IC cards only work in the Takamatsu area on this line. Buy a PAPER ticket or "
        "you will not be able to exit at Matsuyama.",
        "Connection waits run 30–60 minutes. Carry food — several changes are at stations "
        "with nothing.",
        "The footbath outside Dogo Onsen is, in every account, 'blisteringly hot, always'.",
        "Bathing etiquette: wash thoroughly at the taps first, no swimwear, small towel "
        "stays out of the water."],
 sleep="Matsuyama — Dogo Onsen area, or Guesthouse Casablanca near JR Matsuyama (¥2,500)",
 legs=[("Kotohira","Matsuyama","—","+4.5–5 h all-local, 2 changes","JR Yosan Line, all local trains",3960)]),
    ]
    days[i:i + 3] = swap
    # everything after the swap moves one day earlier
    for d in days[i + len(swap):]:
        d["date"] = (datetime.date.fromisoformat(d["date"])
                     - datetime.timedelta(days=1)).isoformat()
    return a2

A3 = _make_A3()
OPTIONS["A3"] = A3


# ─────────────────────────────────────────────────────────────────────────────
# OPTION C — a week in Shikoku, built on the two-base pattern.
#
# This is the shape four independent voices on the japan-guide forum converge
# on, and it is NOT a truncated version of A or B. It deletes both of Shikoku's
# awkward links at once: no Kōchi means no ¥4,000 reservation-only bus and no
# four-hour rail alternative; no Iya means no gamble on four buses a day. What
# it buys instead is Takamatsu's genuine advantage — it is the one place in
# Shikoku with a real spread of cheap, frequent day trips.
#
#   "I would divide it at least into two bases, like Matsuyama and Takamatsu."
#   "The time you spend backtracking every day will be a big waste that you
#    could have spent sightseeing."
#   "I absolutely love not dealing with hotel changes and luggage."
#
# The counter-argument, stated honestly: you will not see inland or southern
# Shikoku at all.

C = dict(
    key="C",
    name="Option C — one week, two bases, barely any packing",
    verdict=("Seven nights in three beds instead of seven. Takamatsu is the only city in "
             "Shikoku with a real spread of cheap frequent day trips, so you sit still and "
             "let the islands come to you. Cheapest of the three, and the least tiring — at "
             "the cost of never seeing inland or southern Shikoku."),
    days=[
dict(date="2026-10-09", title="Osaka → Kobe → the overnight boat to Shikoku",
 flow=[
  ("afternoon", "JR to 三宮 Sannomiya and an evening in Kobe — the Kitano foreign quarter and "
   "the harbour. Kobe beef if the budget stretches; it won't, but the cheap teppanyaki "
   "counters serve the same beef."),
  ("before the sailing", "THE FERRY TERMINAL BUS out to the Jumbo Ferry berth. Leave more "
   "time than feels necessary — this is a boat, and it will not wait."),
  ("23:30 → 05:15", "THE OVERNIGHT CROSSING to Takamatsu. It saves a night's accommodation "
   "and lands you with the whole day ahead. ⚠️ THE ¥1,990 HEADLINE IS THE BASE FARE: the "
   "overnight sailing adds a ¥340 midnight fee, there is a ¥340 high-season fee at busy "
   "times, and a fuel surcharge has been posted at +¥500 one way. Budget nearer ¥2,900. "
   "Booking online saves ¥100."),
  ("be honest with yourself",
   "IT IS NOT A COMFORTABLE NIGHT. Cabin-less — you sleep in a reclining seat or on the "
   "carpet, like everyone else. If sleep matters more than the money, take a daytime "
   "sailing and lose the morning instead."),
 ],
 do=["An evening in Kobe — the Kitano foreign quarter, the harbour, and Kobe beef if the "
     "budget stretches (it won't, but the cheap teppanyaki counters are the same beef).",
     "Then the overnight Jumbo Ferry, which saves you a night's accommodation and lands you "
     "in Takamatsu at 05:15 with the whole day ahead."],
 travel="Train to Kobe, then the ferry terminal bus, timed to the sailing. Cabin-less — you "
        "sleep in a reclining seat or on the carpet, like everyone else.",
 watch=["⚠️ A FARE REVISION IS ANNOUNCED FOR OCTOBER 2026, alongside a new ship and an "
        "online discount — trade press reported it, but I could not reach the operator's own "
        "fare page for the new figure. You sail on the 9th, so treat the numbers below as the "
        "OLD ones and re-check with the operator before booking.",
        "⚠️ The ¥1,990 headline is the BASE fare. The overnight sailing adds a ¥340 midnight "
        "fee, there is a ¥340 high-season fee at busy times, and a fuel surcharge has been "
        "posted at +¥500 one way. Budget nearer ¥2,900.",
        "Booking online saves ¥100 (¥1,890).",
        "It is not a comfortable night's sleep. If that matters more than the money, take a "
        "daytime sailing and lose the morning instead."],
 sleep="On the ferry (Kobe 23:30 → Takamatsu 05:15)",
 legs=[("Osaka","Kobe Sannomiya","frequent","+~30 min","JR Kobe Line rapid",None),
       ("Kobe","Takamatsu","23:30 dep","05:15 arr","Jumbo Ferry, overnight (+¥340 midnight fee)",1990)]),

dict(date="2026-10-10", title="Takamatsu — Ritsurin Garden, slowly",
 flow=[
  ("05:15", "YOU LAND BEFORE DAWN. Bags into the station lockers and take the morning gently "
   "— there is no prize for rushing today."),
  ("06:00 opening", "RITSURIN GARDEN, and give it the morning. A Takamatsu resident's advice "
   "is specifically to come early: it opens at 06:00 in October and that is the light it was "
   "designed for. 300 years old, six ponds, thirteen hills, a whole forested mountain "
   "borrowed as its backdrop. ¥500. ⚠️ Allow two hours minimum — one visitor said two "
   "'was not quite enough'."),
  ("lunch", "SANUKI UDON. Kagawa is the udon prefecture and the self-serve counters are often "
   "under ¥400. This is the place to eat it."),
  ("afternoon", "TAMAMO PARK, the seawater castle moat where they feed the bream — ¥300, and "
   "UNDER-18s FREE — then the 2.7 km shotengai arcade."),
  ("eat before 20:00", "⚠️ Takamatsu is 'virtually dead' by 21:30. Do not leave dinner late."),
 ],
 do=["RITSURIN GARDEN, and give it the morning: 300 years old, six ponds, thirteen hills, "
     "with a whole forested mountain borrowed as its backdrop. A Takamatsu resident's advice "
     "is to come in the morning specifically — it was designed for that light.",
     "Sanuki udon for lunch. Kagawa is the udon prefecture and the self-serve counters are "
     "often under ¥400.",
     "Tamamo Park, the seawater castle moat where they feed the bream, and the 2.7 km "
     "shotengai arcade."],
 travel="You arrive at 05:15, so bags into station lockers and take it gently. Ritsurin is "
        "seven minutes on the Kotoden.",
 watch=["Allow two hours minimum for Ritsurin — one visitor said two hours 'was not quite "
        "enough'.",
        "Takamatsu is 'virtually dead' by 21:30. Eat early.",
        "Foliage here peaks 3 December; you'll see it green."],
 sleep="Takamatsu — WeBase (dorm ¥3,500, or ¥2,600/night on the weekly backpacker plan)",
 legs=[("Takamatsu","Ritsurin Kōen","every 15 min","+7 min","Kotoden to Ritsurin — RAISED to ¥250 on 1 Oct 2026 (JR is ¥240)",250)]),

dict(date="2026-10-11", title="Naoshima — the art island",
 flow=[
  ("BOOKED WEEKS AGO", "⚠️ CHICHU AND TESHIMA ARE DATED, TIMED TICKETS with NO door sales "
   "once a slot is gone. If you have not booked, do that before reading further — see the "
   "banner above. Today is a Sunday, so the Monday closures do not bite."),
  ("08:12 → 09:02", "THE FIRST FERRY from 高松港 Takamatsu to 宮浦 Miyanoura. Five sailings a "
   "day each way. ⚠️ CASH — the ferries are cash only and so are some island shops."),
  ("¥100 flat, hourly", "THE ISLAND BUS loops between the two harbours and the museums, ten "
   "minutes end to end. Kusama's yellow pumpkin is on the pier as you land."),
  ("your booked slot", "CHICHU ART MUSEUM — Tadao Ando's galleries sunk into the hillside, "
   "10:00–17:00 with last entry 16:00. ¥2,700 on a weekend online. Then LEE UFAN (¥1,200) "
   "next door if you want it."),
  ("10:00–16:30", "THE ART HOUSE PROJECT at 本村 Honmura — whole abandoned houses given to "
   "individual artists. ¥1,200 for five sites. ⚠️ Minamidera and Kinza need their own booked "
   "slots; Kinza admits ONE PERSON EVERY 15 MINUTES."),
  ("17:00, or pay for the 19:45", "THE LAST BOAT BACK, and it is NOT the 17:00 ferry. "
   "Shikoku Kisen also runs a 高速旅客船 (high-speed passenger boat) at 19:45 that reaches "
   "Takamatsu at 20:15 in thirty minutes — ¥1,590 against the ferry's ¥680. ⚠️ Sold at the "
   "WINDOW only, CASH only, one-way tickets only, and it takes no bicycles. So a late "
   "finish costs ¥910, not a night on the island — but only if you have the cash."),
 ],
 book=["⚠️ CHICHU ART MUSEUM and TESHIMA ART MUSEUM are dated, timed tickets and there "
       "are NO door sales once a slot sells out. This is the only thing on the whole trip "
       "that can fail outright.",
       "Tickets open at 10:00 JST on the SECOND FRIDAY of the month two months ahead — "
       "for mid-October 2026 that was Friday 14 August 2026, so booking is ALREADY OPEN. "
       "Book before you read any further.",
       "Online is also ¥200–300 cheaper than the gate at every Benesse site."],
 do=["NAOSHIMA. A former industrial island turned over to contemporary art: Tadao Ando's "
     "concrete galleries sunk into the hillside, Yayoi Kusama's yellow pumpkin on the pier, "
     "and the Art House Project, where whole abandoned houses in the village have been given "
     "to individual artists.",
     "The ¥100 island bus loops between the two harbours and the museums.",
     "Even if you don't book a single gallery, the island itself — the coast road, the "
     "pumpkins, the bathhouse — is worth the crossing."],
 travel="Fifty minutes on the car ferry from Takamatsu port, ten minutes' walk from the "
        "station. Five sailings a day each way.",
 watch=["⚠️ BOOK THE GALLERIES AHEAD — several now use timed entry and turning up on the day "
        "may not work.",
        "⚠️ CASH. The ferries are cash only, and so are some of the island shops.",
        "First ferry out 08:12. The last FERRY back is 17:00 — but the 19:45 高速旅客船 gets "
       "you home at 20:15 for ¥1,590 against the ferry's ¥680, so a late finish costs "
       "money, not a night on the island. "
        "sleeping on the island."],
 strand=[
  _S("The last boat off Naoshima is NOT the 17:00 ferry",
     "CONFIRMED",
     "Shikoku Kisen: the last FERRY 宮浦 → 高松 is 17:00 (60 min, ¥680). But a 高速旅客船 "
     "leaves at 19:45 and reaches Takamatsu at 20:15 in thirty minutes for ¥1,590. So a "
     "late finish costs ¥910, not a night on the island. ⚠️ The fast boat is sold at the "
     "WINDOW only, CASH only, one-way tickets only, and takes NO bicycles — so if you hired "
     "one, the 17:00 ferry really is your deadline.",
     check="Confirm both timetables on the route page before you cross.",
     who="四国汽船 087-821-5100 · 直島（宮ノ浦）切符売り場 087-892-3104",
     by="On the morning, before you sail.",
     fallback="Naoshima has accommodation, but in October it books out — do not treat "
              "staying over as a plan.",
     links=["kisen_naoshima"]),
 ],
 sleep="Takamatsu — WeBase",
 legs=[("Takamatsu Port","Miyanoura, Naoshima","08:12","+50 min","Shikoku Kisen ferry (5 sailings/day)",680),
       ("Naoshima","island bus, all day","every hour","10 min end to end","Town bus, flat fare",100),
       ("Miyanoura","Takamatsu Port","17:00 (last FERRY)","+60 min","Shikoku Kisen ferry",680),
       ("Miyanoura","Takamatsu Port","19:45 (last boat of any kind)","20:15","Shikoku Kisen 高速旅客船 — window sales, CASH ONLY, no bikes",1590)]),

dict(date="2026-10-12", title="Shodoshima — Kankakei Gorge and the soy-sauce coast",
 do=["KANKAKEI GORGE by ropeway — one of Japan's three great gorges, a five-minute cable "
     "ride over red rock spires with the Inland Sea opening out behind you.",
     "YAMAROKU SOY SAUCE at Yasuda: a working brewery you walk straight into, free, no "
     "reservation. Cedar barrels two storeys high and over a century old, furred with the "
     "wild yeast that makes the flavour.",
     "Olive Park if the clock allows — Japan's first olive grove, flat, and the bus stops "
     "at the gate."],

 flow=[
  ("first ferry",
   "高松港 Takamatsu Port to 土庄港 Tonoshō, an hour on the car ferry. Take the ¥700 car "
   "ferry, NOT the ¥1,400 fast boat — you are not in a hurry and the deck is the point."),
  ("09:40 → 10:12", "土庄港 Tonoshō across the island to 草壁港 Kusakabe Port, Olive Bus "
   "Sakate line."),
  ("10:30 → 10:42", "THE FREE TOWN SHUTTLE up to 紅雲亭 Kouuntei, the ropeway base — 8 runs a "
   "day, every day in October, none at all in November."),
  ("10:45 – 12:30", "KANKAKEI GORGE by ropeway, ¥2,340 return, cars every 12 minutes. One of "
   "Japan's three great gorges. ⚠️ ¥2,700 from 1 November."),
  ("afternoon", "YAMAROKU SOY SAUCE at 安田 Yasuda — a working brewery, free, no reservation, "
   "open to 17:00. Or the Olive Park, Japan's first olive grove, flat, with the bus stopping "
   "at the gate. Not both: the island's buses are not frequent enough."),
  ("last 20:10 → 21:10",
   "土庄港 Tonoshō back to 高松港 Takamatsu. ⚠️ CHECK THIS BEFORE YOU SET OUT — it is the one "
   "thing today that can strand you on an island."),
 ],
 travel="An hour on the ferry from Takamatsu, then the island bus and the free town shuttle "
        "up to the ropeway.",
 watch=["⚠️ This is a long day trip. The last ferry back to Takamatsu leaves Tonoshō at 20:10, "
        "reaching Takamatsu at 21:10 "
        "— check it before you set out.",
        "The Kankakei shuttle is FREE, 8 runs a day, and runs every day in October — but "
        "stops completely for the whole of November.",
        "⚠️ From 1 October 2026 the ALL SHIKOKU pass no longer covers the Shodoshima ferry "
        "or the Olive Bus. Not that you should buy that pass on this itinerary.",
        "Foliage here peaks 27 November — about six weeks after you."],
 strand=[
  _S("The last ferry between Takamatsu and Shodoshima",
     "CONFIRMED",
     "Shikoku Ferry's own timetable, 15 sailings each way, 60 minutes, ¥700. LAST 高松発 "
     "20:20 → 土庄 21:20. LAST 土庄発 20:10 → 高松 21:10. ⚠️ AND A TRAP: the 土庄発 19:30 and "
     "the 高松発 15:10 are 危険物搭載車両の航送指定便 on WEEKDAYS — hazardous-cargo sailings that "
     "ORDINARY PASSENGERS CANNOT BOARD. On a weekday the real gap before the last boat is "
     "18:40 → 20:10.",
     check="Confirm both directions on the route page; ferry diagrams change with engine "
           "maintenance and the operator says so on the page.",
     who="Shikoku Ferry — ask at the Takamatsu or Tonoshō 乗り場",
     by="Before you set out that morning.",
     fallback="A high-speed boat (高速艇) also works this route and is a separate timetable. "
              "Otherwise it is a night on Shodoshima.",
     links=["sf_takamatsu"]),
 ],
 sleep="Takamatsu — WeBase",
 legs=[("Takamatsu Port","Tonoshō, Shodoshima","15 sailings/day","+60 min","Shodoshima ferry (car ferry, not the ¥1,400 fast boat)",700),
       ("Tonoshō Port","Kusakabe Port","09:40","10:12","Olive Bus, Sakate Line",500),
       ("Kusakabe Port","Kouuntei (ropeway base)","10:30","10:42","FREE town shuttle, 12 min",0),
       ("Kankakei base","Summit and back","every 12 min","~5 min each way","Ropeway",2340),
       ("Tonoshō Port","Takamatsu Port","15/day, last 20:10 → 21:10","+60 min","Shodoshima ferry",700)]),

dict(date="2026-10-13", title="Kotohira — the shrine on the stairs",
 flow=[
  ("every 30 min", "THE KOTODEN from Takamatsu, about an hour for ¥730 — cheaper than JR "
   "(¥980) and it drops you closer to the stairway. It is a private railway, so no JR pass."),
  ("morning", "KONPIRA-SAN. 785 steps to the main hall, 1,368 to the inner shrine, up a "
   "stairway lined with shops selling walking sticks and sweets. The grounds are FREE and "
   "the climb is optional — the town and the first stretch are the pleasant part. See the "
   "Walks tab. The palanquin carriers who used to haul people up have stopped."),
  ("09:00–17:00, last entry 16:30", "KANAMARU-ZA, the oldest surviving kabuki theatre in "
   "Japan (1835). ¥500, and you can work the revolving stage and trapdoors by hand."),
  ("timed to sunset, daily",
   "OPTIONAL AND THE BEST THING WITHIN REACH: CHICHIBUGAHAMA. A sunset shuttle runs DAILY "
   "from outside JR Kotohira, ¥1,500 one way / ¥2,000 return. Today's official mirror window "
   "is 16:30–17:45 against a 17:34 sunset — tight but it works. Check your date at "
   "https://www.mitoyo-kanko.com/chichibugahama/ ⚠️ Some October dates have NO window at all."),
  ("night", "AN ONSEN-TOWN EVENING, which is what the night here is really for."),
 ],
 do=["KONPIRA-SAN, the great sea-god shrine, reached by a stone stairway lined with shops "
     "selling walking sticks and sweets. 785 steps to the main hall, 1,368 to the inner one. "
     "Entirely optional — the town and the first stretch of the stairway are pleasant on "
     "their own, and the free walking sticks are lent, not sold.",
     "KANAMARU-ZA, the oldest surviving kabuki theatre in Japan (1835). You can go backstage "
     "and work the revolving stage and trapdoors by hand. ¥500, 09:00–17:00.",
     "OPTIONAL, AND THE BEST THING WITHIN REACH TODAY: CHICHIBUGAHAMA at sunset. A flat tidal "
     "beach that holds a film of water once the tide drops, turning the whole strand into a "
     "mirror. A sunset shuttle bus runs DAILY from outside JR Kotohira, timed to the light — "
     "¥1,500 one way, ¥2,000 return. Today's official mirror window is 16:30–17:45 and sunset "
     "is 17:34, so it is tight but it works.",
     "An onsen town evening, which is what the night here is really for."],
 travel="An hour from Takamatsu on the Kotoden for ¥730 — cheaper than JR and it drops you "
        "closer to the stairway. The beach, if you go, is a bus from the same station.",
 watch=["⚠️ TAKAYA SHRINE — the 'Gate in the Sky' — does NOT work on this itinerary. Its "
        "shuttle bus runs on Saturdays, Sundays and public holidays only, and the one day "
        "Option C is near Kan-onji is a Tuesday. Without the shuttle it is a ¥3,600 taxi each "
        "way or a 50-minute climb of 350 vertical metres. If you want the gate, take Option A, "
        "which catches it on the holiday Monday — the single best day of the month for it.",
        "The Chichibugahama mirror window shifts every day and some days have none at all "
        "(14–17 October, for instance). Check the official calendar before committing.",
        "785 steps is the only real climb on this entire itinerary, and it is skippable.",
        "The palanquin carriers who used to haul people up have stopped operating.",
        "The Kotoden is a private railway — no JR pass, but it's the cheaper option anyway."],
 sleep="Kotohira — onsen ryokan (Kotohira Park Hotel, Onyado Shikishimakan)",
 legs=[("Takamatsu","Kotohira","every 30 min","+~1 h","Kotoden to Kotohira — RAISED to ¥780 on 1 Oct 2026 (JR local is ¥980)",780),
       ("JR Kotohira","Chichibugahama and back","timed to sunset, runs daily","—","OPTIONAL: Chichibugahama sunset shuttle bus, return",2000)]),

dict(date="2026-10-14", title="Right across to Matsuyama, on the west coast, and Dogo Onsen",
 do=["DOGO ONSEN — one of the oldest hot springs in Japan, named in 8th-century chronicles, "
     "and the model for the bathhouse in Spirited Away. The restoration finished in July "
     "2025, so you see it without scaffolding for the first time in years.",
     "The Botchan Train, a replica Meiji steam locomotive that still runs through the streets.",
     "The arcade between the tram stop and the bathhouse — the right place for dinner."],
 travel="The long transfer of the week: across the top of Shikoku on the Yosan Line, about "
        "two and a half hours by limited express or four and a half on locals with two changes.",
 watch=["⚠️ This is the one day where the limited express is arguably worth it — the "
        "all-local run is 4.5–5 hours with two changes and 30–60 minute waits.",
        "⚠️ IC cards only work in the Takamatsu area on this line. Buy a PAPER ticket or you "
        "cannot exit at Matsuyama.",
        "The footbath outside Dogo Onsen is, in every account, 'blisteringly hot, always'.",
        "Bathing etiquette: wash thoroughly at the taps first, no swimwear, small towel out "
        "of the water."],
 sleep="Matsuyama — Dogo Onsen area, or Guesthouse Casablanca near JR Matsuyama (¥2,500)",
 alt_label="All-local rail — cheapest, 4.5–5 h, two changes",
 alts=[dict(label="Pay for the limited express — about 2 h 30",
  do=["The one day on this whole itinerary where the express surcharge is arguably worth "
      "paying. Two and a half hours instead of four and a half to five, no changes, and no "
      "30–60 minute waits at stations with nothing.",
      "On a seven-day trip that is a meaningful fraction of the whole thing — you arrive with "
      "an afternoon rather than an evening.",
      "DOGO ONSEN in daylight, and the arcade for dinner without watching the clock."],
  travel="One limited express across the top of Shikoku. Reserve or ride unreserved; either "
         "way it is the surcharge you are paying for, on top of the same basic fare.",
  watch=["⚠️ The surcharge is per person and roughly doubles the fare. If the budget is the "
         "binding constraint, the all-local version above is the default for a reason.",
         "⚠️ IC cards still only work in the Takamatsu area on this line. Buy a PAPER ticket "
         "either way or you cannot exit at Matsuyama.",
         "The exact limited-express surcharge for this pair is not published in the sources "
         "I could reach — the basic fare is ¥3,960 and the surcharge is on top. Ask at the "
         "window; do not budget from the figure below alone.",
         "⚠️ JR Shikoku has announced that しおかぜ／南風 go all-reserved from spring 2027. "
         "Mid-October 2026 is unaffected, but a later trip would be."],
  legs=[("Kotohira","Matsuyama","—","+~2 h 30","JR Yosan Line limited express — basic fare, surcharge on top",3960)])],
 legs=[("Kotohira","Matsuyama","—","+4.5–5 h all-local, 2 changes","JR Yosan Line — or the LEX in ~2h30",3960)]),

dict(date="2026-10-15", title="Matsuyama Castle, and a day that isn't a travel day",
 do=["MATSUYAMA CASTLE — one of only twelve original keeps left in Japan, on a hill in the "
     "middle of the city, with connected walls you can walk and the Inland Sea beyond.",
     "Ninomaru garden below it, built over the old lord's residence.",
     "This is a half-day at most. If that sounds thin, switch the whole day to one of the "
     "alternatives — Uchiko and Ōzu, or the Iyonada coast."],
 travel="Trams around town, and a chair lift up the castle hill.",
 watch=["Take the CHAIR LIFT rather than the ropeway — same price, much shorter queue.",
        "The keep is an original: steep narrow stairs climbed in socks, no lifts. The grounds "
        "and the view don't require it.",
        "Buy water before going up — drinks cost more at the top.",
        "✅ Matsuyama accepts Suica, the one place in Shikoku that reliably does — and here it "
        "PAYS: the tram went to ¥250 flat on 1 April 2026, but tapping IC gets the ¥20 "
        "cashless discount, so it is still ¥230."],
 sleep="Matsuyama",
 alt_label="Matsuyama Castle and the city",
 alts=MATSUYAMA_ALTS,
 legs=[("Castle hill","up and back","—","3 min each way","Chair lift",520),
       ("City trams","—","—","—","Iyotetsu tram, flat fare — ¥250 cash, ¥230 if you tap IC",250)]),

dict(date="2026-10-16", title="The ferry to Hiroshima",
 flow=[
  ("allow the time", "THE PORT IS NOT CENTRAL. Iyotetsu shuttle or suburban train out to "
   "松山観光港 Matsuyama Kanko Port, about 20 minutes and ¥750. A traveller who tried to do "
   "this with luggage found it was 'two bus rides and then a tram ride' and took a taxi "
   "instead for about ¥4,000 — worth knowing if there are two of you and it is raining."),
  ("10 sailings/day", "THE CRUISE FERRY, 2 h 40 threading between the islands. This is a "
   "sightseeing trip rather than a transfer, and the deck is the point. ⚠️ ¥6,000 since the "
   "1 September 2026 revision, up from "
   "¥4,500 in 2022 — the single biggest transport cost of the week. The fast Linear Jet is "
   "¥9,000 for 70 minutes and buys you nothing but time."),
  ("check before you commit", "⚠️ A reduced weekday timetable ran to 30 September 2026 with "
   "some sailings suspended. Confirm the October schedule."),
  ("every 12 min", "HIRODEN TRAM LINE 5 from 広島港 Hiroshima Port into the city, 29 minutes, "
   "flat ¥240. You arrive with the afternoon intact."),
 ],
 do=["A slow crossing of the Inland Sea — two hours and forty minutes threading between the "
     "islands, which is a sightseeing trip rather than a transfer.",
     "Arrive in Hiroshima with the afternoon intact."],
 travel="Iyotetsu shuttle or suburban train out to Matsuyama Kanko Port, then the Cruise "
        "Ferry. The port is not central — allow the time.",
 watch=["⚠️ FARES ROSE AGAIN ON 1 SEPTEMBER 2026, weeks before you travel: the Cruise Ferry "
        "went ¥5,800 → ¥6,000 and the Linear Jet ¥8,800 → ¥9,000. For scale it was ¥4,500 "
        "in 2022. Anything you read quoting ¥5,800 predates the revision. The slow boat is "
        "still the better value and much the better view.",
        "⚠️ A reduced weekday timetable ran to 30 September 2026 with some sailings suspended "
        "— check the October schedule before you commit.",
        "At the Hiroshima end, tram line 5 runs from the port into the city.",
        "This is the single biggest transport cost of the week. The alternative is the "
        "Shimanami Kaido from Imabari — see the Shimanami toggle on options A and B."],
 sleep="Hiroshima — The Evergreen Hostel or J-Hoppers",
 legs=[("JR Matsuyama Stn","Matsuyama Kanko Port","—","+20 min","Iyotetsu port shuttle bus",750),
       ("Matsuyama","Hiroshima","10 sailings/day","+2 h 40","Setonaikai Kisen Cruise Ferry — RAISED to ¥6,000 on 1 Sep 2026",6000),
       ("Hiroshima Port","city centre","every 12 min","+29 min","Hiroden tram line 5, flat fare",240)]),

dict(date="2026-10-17", title="Rabbit island",
 flow=RABBIT_FLOW,
 do=["ŌKUNOSHIMA — around a thousand feral rabbits that mob you the moment you sit down, and "
     "a sober museum about the poison gas the island secretly made for the Imperial Army. "
     "Ruined batteries stand in the woods.",
     "Optional hour on the way: Takehara, an Edo salt-and-sake merchant town twelve minutes' "
     "walk from its station."],
 travel="Out along the coast by bus or local train, then a fifteen-minute ferry.",
 watch=["⚠️ BUY RABBIT FOOD BEFORE BOARDING — none is sold on the island. About ¥200 at the "
        "shop by Tadanoumi station. PELLETS, not vegetables.",
        "⚠️ The ferry is CASH ONLY.",
        "Don't pick the rabbits up — they panic and break bones, and there's no vet.",
        "Allow 4–5 hours. A couple who budgeted three ended up running for the boat."],
 strand=[
  _S("The last boat OFF Ōkunoshima — this plan's '18:30' does not match the operator",
     "UNVERIFIED",
     "大三島フェリー's timetable gives the last call at 大久野島 heading to 忠海 as ※17:16, "
     "arriving 17:30 — and the ※ means that sailing serves the island only FEBRUARY TO "
     "OCTOBER. The next boat, 18:40 from 盛, does NOT stop there at all. A SECOND operator "
     "(休暇村客船) also works the route and is probably where '18:30' and 'every 30–45 min' "
     "came from, but its site is behind a bot wall and could NOT be read.",
     check="ONLINE: the 大三島フェリー timetable below is readable now and gives 17:16 — take "
           "that as your working deadline. Its 運航情報 notices sit on the same page, so "
           "check them too (the second jetty has closed for repairs before). The second "
           "operator's page is bot-walled from here but may open in a normal browser — "
           "try it, and if it loads, read its last sailing.",
     who="NO PHONE CALL NEEDED IF YOU DO ONE THING: confirm the last sailing AT THE "
         "TADANOUMI TICKET WINDOW when you buy, and ask which operator it is — a "
         "face-to-face question with a printed timetable in front of you. Only if you "
         "want certainty in advance, have your hotel ring 休暇村大久野島 0846-26-0321.",
     by="On the morning, at the port, before you cross.",
     fallback="NONE. One hotel on the island and no other way off. The operator warns of "
              "delays at busy times and its second jetty has been closed for repairs before.",
     links=["omishima_time", "qkamura_ohkuno", "rabbit_island"]),
 ],
 sleep="Hiroshima",
 legs=[("Hiroshima Bus Centre","Tadanoumi Stn","4 round trips/day","+1h40","Geiyo Bus 'Kaguya-hime'",1500),
       ("Tadanoumi Port","Ōkunoshima and back","every 30–45 min","+15 min each way","Ferry — CASH ONLY",720),
       ("Tadanoumi Port","bag storage","—","—","¥500 per bag per day",500),
       ("Tadanoumi Stn","Hiroshima","4 round trips/day","+1h40","Geiyo Bus 'Kaguya-hime'",1500)]),

dict(date="2026-10-18", title="Miyajima",
 flow=MIYAJIMA_FLOW,
 do=["The floating torii at Itsukushima — in the sea at high tide, walkable across the "
     "seabed at low. Below 100 cm you can walk out, above 250 cm it floats. October tide "
     "table: https://www.miyajima.or.jp/sio/sio10.html",
     "Itsukushima Shrine, on stilts over the water since the 12th century.",
     "The ropeway up Mt Misen, plus wild deer and the Daishō-in temple complex.",
     "Momiji manjū, maple-leaf cakes made in front of you along the main street."],
 travel="Tram out to the pier and a ten-minute ferry. One pass covers the lot.",
 watch=["⭐ The Hiroden ¥1,000 day pass covers all trams + the ferry + the ¥100 visitor tax, "
        "and cuts the ropeway from ¥2,000 to ¥1,500.",
        "⭐ Ride the JR ferry out between 9:10 and 16:10 for the free close pass by the torii.",
        "The summit is ~30 min beyond the ropeway up a steep stepped trail — optional. Last "
        "ascent 16:00.",
        "⚠️ The Reikadō 'eternal flame' hall burned down in May 2026."],
 sleep="Hiroshima",
 legs=[("Hiroshima","Miyajima + all city trams","—","—","Hiroden 1-day tram & ferry pass",1000),
       ("Momijidani","Shishiiwa (Mt Misen)","last ascent 16:00","+~20 min each way","Ropeway — ¥1,500 with the pass",1500)]),

dict(date="2026-10-19", title="Peace Memorial Park, then on to Kyushu",
 do=["The Peace Memorial Museum and the A-Bomb Dome. Allow more time than you think.",
     "Hiroshima-style okonomiyaki — layered rather than mixed, with noodles — before you go."],
 travel="Everything central; trams are a flat ¥240.",
 watch=[],
 sleep="→ Kyushu",
 legs=[]),
])

OPTIONS["C"] = C

# switcher order: A, then its Kōchi-free sibling, then B, then the one-week plan
for _k in ("A", "A2", "A3", "B", "C"):
    OPTIONS[_k] = OPTIONS.pop(_k)


# ─────────────────────────────────────────────────────────────────────────────
# SHIMANAMI KAIDO — three ways to do the same crossing.
#
# What the evidence says (see research/shimanami.md):
#   · The route is ~80 km, not the 70 km everyone quotes — bridge approach
#     spirals and the run into Imabari add ~10 km (GPS-measured log).
#   · The rental operator itself rates recreational riders at 10 km/h and the
#     full route at ~8 hours, and explicitly encourages 2 or 3 days.
#   · Mid-October sunset is ~17:20–17:40 and the bridge cycleways are UNLIT,
#     so a beginner's 8–10 h day has essentially no margin.
#   · NOBODY reputable says one day is right for casual riders. Two independent
#     accounts who did it in two days said that felt rushed.
#   · Imabari → Onomichi (our direction) is the correct one: tailwind on
#     strong-wind days, and both hills done while fresh.
#
# Variants are spliced in place of the single Shimanami day; later dates shift.
SHIMANAMI_VARIANTS = {

"nobike": [
dict(title="Across the Shimanami by boat and bus — no bicycle at all",
 do=["You still cross all six islands and see all seven bridges — from a bus window and "
     "then from the deck of a boat, which is arguably the better view anyway.",
     "ŌYAMAZUMI SHRINE on Ōmishima: a 2,600-year-old shrine in a grove of ancient camphor "
     "trees, holding the largest collection of medieval Japanese arms and armour in the "
     "country. Warlords came here to dedicate their weapons before battle. It is the single "
     "best thing on the route that has nothing to do with cycling.",
     "SETODA on Ikuchijima: the Shiomachi arcade, gelato on the seafront, and Kōsanji — a "
     "1930s temple where a businessman built replicas of the finest temple buildings in "
     "Japan, then topped the hill with the Hill of Hope, 5,000 tonnes of Carrara marble.",
     "The 40-minute ferry into Onomichi at the end, threading between the islands."],
 travel="Local train to Imabari, the Shimanami Liner bus out to Ōmishima, the same bus on to "
        "Setoda, then the Setouchi Cruising boat into Onomichi. No bike, no bridges on foot, "
        "and one seat to the next the whole way.",
 watch=["⚠️ The island bus stops sit ON the expressway, usually with a stair or ramp down to "
        "the island road. Check the descent before you commit, especially with packs.",
        "Kōsanji is ¥1,800 a head — the steepest admission on the whole trip. The Hill of "
        "Hope and the Kongō hall are included. 09:00–17:00, last entry 16:30. If that feels "
        "like a lot, the Shiomachi arcade and the seafront cost nothing.",
        "Ferries from Setoda to Onomichi leave 07:50 / 10:00 / 11:25 / 13:25 / 15:00 / 17:00 "
        "— the 15:00 is the sensible one. Cash, cards and IC all accepted.",
        "Imabari-side Shimanami Liner fares are not published online. The Fukuyama-side "
        "equivalents run ¥2,000–2,800, so expect that range. Pay at the counter or on board.",
        "No reservations on the Liner — it is first-come at the stop."],
 sleep="Onomichi — Guesthouse Yadocurly (¥2,800), Fuji Hostel (¥2,500) or Anago no Nedoko (¥3,000)",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari","Ōmishima BS","~16 per day, no reservation","+~50 min","Shimanami Liner highway bus",None),
       ("Ōmishima BS","Setoda BS","~16 per day","+~25 min","Shimanami Liner highway bus",None),
       ("Setoda Port","Onomichi","15:00","+40 min","Setouchi Cruising ferry",1500)]),
],

"1day": [
dict(title="Across the Shimanami Kaido to Onomichi — by bus",
 do=["Six islands and seven of the most elegant suspension bridges in the world, crossing "
     "the Inland Sea back to Honshu. Even from a bus seat it is one of Japan's great "
     "scenic routes.",
     "OPTIONAL: bus out to one island, rent a bike there, ride a bridge or two on the "
     "dedicated cycleway, and bus or ferry onward.",
     "Onomichi — a steep temple town of alleys and cats above a working shipping strait."],
 travel="Local train up the coast to Imabari, then bus across the islands with one change.",
 watch=["There is NO direct Imabari–Onomichi bus — that route was abolished in 2005. You "
        "change at Innoshima Ōhashi, and the operator warns the connection 'may not be smooth'.",
        "Don't try to ride all 80 km in a day. The rental operator itself rates recreational "
        "riders at 10 km/h and the full route at about eight hours.",
        "A rental bike CANNOT go on the bus unless it's bagged — the service that took "
        "assembled bikes ended in June 2020."],
 sleep="Onomichi — Guesthouse Yadocurly (¥2,800 dorm) or Fuji Hostel (¥2,500)",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari","Onomichi","hourly connections","+1.5–2 h","Shimanami Liner + local bus",2390)]),
],

"2day": [
dict(title="Shimanami day 1 — Imabari to Ōmishima, the two big bridges",
 do=["THE KURUSHIMA KAIKYŌ BRIDGE — 4 km, the longest triple suspension bridge in the "
     "world, and the single most spectacular thing on the route. You get it in the first "
     "hour, while your legs are fresh.",
     "Ōshima's Miyakubo Pass (~70 m) — the one real climb of the day.",
     "Lunch on Hakatajima: the island is famous for its salt, and the salt ramen is the "
     "thing to order.",
     "Ōmishima and Ōyamazumi Shrine, which holds the largest collection of medieval "
     "arms and armour in Japan."],
 travel="Collect bikes at Imabari station or Sunrise Itoyama, ride about 40 km with both "
        "hills done early, and sleep on the island at the exact midpoint.",
 watch=["E-BIKES: yes, you CAN rent them — electric-assist ¥4,000/day, full e-bike ¥8,000/day. "
        "BUT they must be returned to the terminal they came from and are one-day rentals "
        "only, so they CANNOT do a one-way crossing. For Imabari→Onomichi the only workable "
        "bike is a cross bike, ¥3,000/day plus ¥1,000 for the one-way drop-off. If you want "
        "electric assist, do an out-and-back day ride from one terminal instead and move "
        "between towns by bus or ferry.",
        "Send the big bags ahead: Sagawa's Hands-Free Cycling is ¥2,200 a bag, SAME day, "
        "between Onomichi, the islands and Imabari. Drop by 10:00 at island and Imabari "
        "properties, and reserve the night before.",
        "Sleep at Inokuchi (I-Link ¥4,270 dorm, or WAKKA ¥6,500 with breakfast) — both are "
        "ON the route. The Miyaura guesthouses are cheaper but sit over a 76 m pass you'd "
        "climb at the end of the day and again in the morning.",
        "Bail-outs today: Ōshima and Hakatajima bus stops, or the Ōmishima Blue Line ferry "
        "back to Imabari (¥980 + ¥250 a bike)."],
 sleep="Ōmishima, Inokuchi — I-Link Hostel (¥4,270 dorm) or WAKKA (¥6,500 w/ breakfast)",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari Stn","Sunrise Itoyama","—","6 km, 30–40 min","Rented cross bike, ¥3,000/day × 2 days",6000),
       ("Bikes","one-way drop-off fee","—","—","Shimanami rental cycle, one-way surcharge",1000),
       ("Big bags","Imabari → Ōmishima","drop by 10:00","same day","Sagawa Hands-Free Cycling, per bag",2200)]),

dict(title="Shimanami day 2 — Tatara Bridge, Setoda, and on to Onomichi",
 do=["THE TATARA BRIDGE — the route's signature cable-stayed span, and the flattest, "
     "prettiest leg of the whole ride.",
     "Ikuchijima's Lemon Valley and Setoda Sunset Beach.",
     "SETODA — Kōsanji temple, a riotous 1930s replica of temples from all over Japan, "
     "with a marble Hill of Hope on top. Gelato at Dolce on the seafront.",
     "Innoshima, then the little ¥100 ferry across into Onomichi."],
 travel="About 40 flat kilometres, then a five-minute ferry hop into town.",
 watch=["Leave by 09:00. Mid-October sunset is around 17:20–17:40 and the bridge cycleways "
        "are UNLIT.",
        "⭐ BUILT-IN ESCAPE VALVE: if the day is going badly, stop at Setoda Port (~32 km in) "
        "and take the Setouchi Cruising boat to Onomichi — ¥1,500 plus ¥500 for the bike, "
        "which rolls straight aboard. Sailings 11:25 / 13:25 / 15:00 / 17:00. That turns "
        "today into a flat 20 km with the best bridge still included.",
        "Drop the bikes at the Onomichi Station terminal — note it MOVED in October 2025."],
 sleep="Onomichi — Guesthouse Yadocurly (¥2,800), Fuji Hostel (¥2,500) or Anago no Nedoko (¥3,000)",
 legs=[("Ōmishima","Setoda (Ikuchijima)","leave by 09:00","~18 km, flat","Cycling — the Tatara Bridge leg",None),
       ("Mukaishima","Onomichi","every few minutes","+5 min","Kaneyoshi ferry (+¥10 bike)",100),
       ("Setoda","Onomichi","11:25 / 13:25 / 15:00 / 17:00","+40 min","INSTEAD, if you bail: Setouchi Cruising ferry ¥1,500 +¥500 bike — replaces the ¥100 hop above",None)]),
],

"3day": [
dict(title="Shimanami day 1 — Imabari to Ōshima, the Kurushima bridge",
 do=["THE KURUSHIMA KAIKYŌ BRIDGE — 4 km, the longest triple suspension bridge in the "
     "world. A short first day means you cross it unhurried and can stop for the view.",
     "Ōshima: the Murakami Kaizoku Museum, about the pirate clans who ran these straits "
     "for four centuries.",
     "Yoshiumi Rose Park and the tidal whirlpools in the strait below the bridge."],
 travel="A deliberately short ~20 km first afternoon. Pick the bikes up at Imabari station "
        "and take your time.",
 watch=["Cross bike only. Electric-assist (¥4,000/day) and e-bikes (¥8,000/day) exist and "
        "are lovely on the bridge ramps, but MUST go back to the terminal they came from — "
        "so they cannot cross one-way.",
        "Ōshima has both of the route's real hills (Miyakubo ~70 m, Taura ~78 m). Doing "
        "them on a short day is the whole point of the three-day split.",
        "お宿ぽんぽこ (¥6,500~) offers a rider rescue pickup if it goes wrong."],
 sleep="Ōshima — お宿ぽんぽこ (¥6,500~), which offers a rescue pickup",
 legs=[("Matsuyama","Imabari","~1 per hour","+71 min","JR Yosan Line local train",1080),
       ("Imabari Stn","Ōshima","—","~20 km","Rented cross bike, ¥3,000/day × 3 days",9000),
       ("Bikes","one-way drop-off fee","—","—","Shimanami rental cycle, one-way surcharge",1000),
       ("Big bags","Imabari → Ōshima","drop by 10:00","same day","Sagawa Hands-Free Cycling, per bag",2200)]),

dict(title="Shimanami day 2 — the Tatara Bridge and Setoda, mostly flat",
 do=["THE TATARA BRIDGE, the route's signature span, on the flattest leg of the whole ride.",
     "Tatara Shimanami Park, and Ōyamazumi Shrine on Ōmishima with its medieval armour.",
     "Ikuchijima's Lemon Valley — this island grows most of Japan's lemons.",
     "SETODA: Kōsanji temple and the marble Hill of Hope, then gelato on the seafront. "
     "Half a day of riding leaves a real half-day here, which is the point."],
 travel="About 20–25 km, almost all flat, with the afternoon free.",
 watch=["This is the leg to protect if anything gets cut — it has the best scenery per "
        "kilometre and the fewest hills on the whole route."],
 sleep="Setoda — Cycle Guest House Shiokaze (¥3,500~) or Shima Yado NEST (¥4,800~)",
 legs=[("Ōshima","Setoda (Ikuchijima)","—","~25 km via the Tatara Bridge","Cycling — the flat highlight leg",None)]),

dict(title="Shimanami day 3 — Setoda to Onomichi, or take the boat",
 do=["Innoshima and its Hassaku orange groves, then the ¥100 ferry into Onomichi.",
     "OR skip the riding entirely: the Setoda boat lands you in Onomichi in 40 minutes "
     "and buys you the whole day for the town's temple walk and the Senkōji ropeway.",
     "Onomichi itself — cat alley, the Path of Literature, and ramen."],
 travel="Either ride the last ~32 km, or put the bikes on the boat and arrive by lunchtime.",
 watch=["The Setouchi Cruising ferry is ¥1,500 plus ¥500 for a bike, and the bike rolls "
        "aboard as-is. Sailings from Setoda at 11:25 / 13:25 / 15:00 / 17:00.",
        "Either way, drop the bikes at the Onomichi Station terminal."],
 sleep="Onomichi — Guesthouse Yadocurly (¥2,800), Fuji Hostel (¥2,500) or Anago no Nedoko (¥3,000)",
 legs=[("Mukaishima","Onomichi","every few minutes","+5 min","Kaneyoshi ferry (+¥10 bike)",100),
       ("Setoda","Onomichi","11:25 / 13:25 / 15:00 / 17:00","+40 min","INSTEAD, if you skip the last leg: Setouchi Cruising ferry ¥1,500 +¥500 bike",None)]),
],
}

SHIMANAMI_LABELS = {
 "nobike": "No cycling — one day, boat and bus",
 "1day": "1 day — bus across",
 "2day": "2 days — ride it, sleep on Ōmishima",
 "3day": "3 days — the relaxed version",
}
SHIMANAMI_VERDICT = {
 "nobike": "If the ride sounds like a chore, this is the honest alternative — and it is not a "
         "consolation prize. You cross every island, see every bridge, and get the two best "
         "non-cycling sights on the route (Ōyamazumi Shrine and Kōsanji) plus a 40-minute "
         "boat into Onomichi. One day, no saddle, and the cheapest of the four.",
 "1day": "By bus this is fine and takes an afternoon. Riding all 80 km in one day is not "
         "sensible for casual cyclists — the operator itself rates recreational riders at "
         "8 hours, and mid-October gives you about 11 hours of light on unlit bridges.",
 "2day": "Enough to COMPLETE the route, only just, and only if nothing goes wrong. Both "
         "travellers who did exactly this said it felt rushed. Ōmishima splits it evenly "
         "at 40 km a day; sleeping at Setoda instead makes day 1 much harder.",
 "3day": "What I'd actually book for two people who don't cycle. One extra hostel night and "
         "one extra day of rental turns it from an endurance task into a holiday — and the "
         "Setoda ferry is a built-in opt-out for the last day.",
}
