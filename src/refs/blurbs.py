"""One standalone line per place, for the map export.

These are written to be read on a phone in Google Maps with NO itinerary around
them: what the place is, and the one thing worth knowing before you go. They
deliberately repeat nothing from the day plans — a pin has to stand on its own.
"""

BLURBS = {
 # ── Kagawa ──────────────────────────────────────────────────────────────────
 "Ritsurin Garden": "300-year-old daimyo garden — six ponds, thirteen hills, a forested "
   "mountain borrowed as the backdrop. Widely called the finest garden in Japan. Flat "
   "paths throughout, and it opens at dawn.",
 "Tamamo Park": "The remains of Takamatsu Castle, whose moat is filled with SEAWATER — "
   "they feed sea bream in it. Small, flat, and right by the station and port.",
 "Kankakei Gorge": "One of Japan's three great gorges, on Shodoshima. A five-minute cable "
   "car over red rock spires with the Inland Sea opening out behind you. Autumn colour "
   "peaks around 27 November.",
 "Angel Road": "A sandbar linking four islets that surfaces at low tide, twice a day, for "
   "about six hours each time. Free. Check the tide table before you come — at high water "
   "there is nothing to walk on.",
 "Olive Park": "Japan's first olive grove, on Shodoshima, with a Greek windmill and a view "
   "over the Inland Sea. Flat, and the bus stops at the gate.",
 "Yamaroku": "A working soy-sauce brewery you walk straight into — free, no reservation. "
   "Cedar barrels two storeys high and over a century old, furred with the wild yeast that "
   "makes the flavour. One of the last places in Japan still doing it this way.",
 "Nakabu-an": "Hand-stretched somen: you do the 箸分け step yourself, pulling dough between "
   "two chopsticks until it becomes hair-thin noodles, then eat what you made. Their "
   "nama-somen (fresh, un-dried) is essentially island-only. BOOK BY PHONE THE DAY BEFORE.",
 "Konpira-san": "The great sea-god shrine, up a stone stairway lined with shops. 785 steps "
   "to the main hall, 1,368 to the inner shrine. The grounds are free and the climb is "
   "optional — the town and the first stretch are the pleasant part.",
 "Kanamaru-za": "The oldest surviving kabuki theatre in Japan, built 1835. You go BACKSTAGE "
   "and work the revolving stage and the trapdoors by hand. Wildly underrated.",
 "Takaya Shrine": "The 天空の鳥居 — a vermilion torii alone on a 404 m summit with nothing "
   "behind it but the Inland Sea. The shuttle bus up runs SATURDAYS, SUNDAYS AND PUBLIC "
   "HOLIDAYS ONLY; on a weekday it is a taxi or a 50-minute climb.",
 "Zenigata Sunae": "A 122-metre Edo coin raked into the beach at Kotohiki Park and re-raked "
   "by the town since 1633. Free, open 24 hours, floodlit until 22:00.",
 "Chichibugahama": "A flat tidal beach that holds a film of water after the tide drops, "
   "turning the whole strand into a mirror. Needs LOW TIDE AT SUNSET plus still air — the "
   "tourism board publishes a per-date calendar, and some days have no window at all.",
 "Shikoku Mura": "An open-air museum of old Shikoku buildings moved here and rebuilt — "
   "farmhouses, a kabuki stage, a vine bridge. Closed Tuesdays.",
 "Yashima": "A flat-topped plateau above Takamatsu with a temple, a 1185 battlefield and a "
   "long view over the Inland Sea.",

 # ── Naoshima / Teshima ──────────────────────────────────────────────────────
 "Chichu Art Museum": "Tadao Ando's galleries sunk into a Naoshima hillside, lit almost "
   "entirely by daylight. DATED, TIMED TICKETS ONLY — if the slot sells out there are no "
   "door sales. Closed Mondays.",
 "Teshima Art Museum": "A single concrete shell open to the sky, with water seeping through "
   "the floor. No exhibits — the building is the work. Dated timed tickets, closed Tuesdays.",
 "Benesse House Museum": "Museum and hotel in one, above the sea. Open 08:00–21:00, far "
   "later than anything else on the island, and open year-round.",
 "Lee Ufan Museum": "Stone, steel and empty space, between a hill and the sea. Small, quiet "
   "and quick. Closed Mondays.",
 "Art House Project, Honmura": "Abandoned houses in a Naoshima village given to individual "
   "artists. Minamidera and Kinza need their own slots — Kinza admits ONE PERSON EVERY "
   "15 MINUTES. Closed Mondays.",

 # ── Tokushima ───────────────────────────────────────────────────────────────
 "Awa Odori Kaikan": "The museum of Tokushima's dance festival, with live performances "
   "daily and a chance to be taught the steps. The evening show at 20:00 is by a different "
   "famous troupe each night.",
 "Mt Bizan": "The hill above Tokushima, by ropeway from the Awa Odori Kaikan building. "
   "Runs until 21:00 from April to October, so the night view over the delta is easy.",
 "Uzu-no-michi": "A 450-metre walkway slung UNDER the road deck of the Ōnaruto Bridge with "
   "glass floor panels 45 metres above the whirlpools. The vortices only form around peak "
   "tidal flow — check the tide calendar and come in that window.",
 "Naruto Park": "The headland beside the Ōnaruto Bridge, and the access point for the "
   "whirlpool walkway and the boats.",
 "Ōtsuka Museum": "A thousand Western masterpieces reproduced full-size in ceramic, "
   "underground. Genuinely strange and genuinely enormous — allow three hours. The most "
   "expensive admission in the region. Closed Mondays.",
 "Iya Kazurabashi": "A 45-metre bridge woven from mountain vine, hanging 14 metres above "
   "the river, rebuilt every three years. The slats are spaced wide enough to see straight "
   "down between them.",
 "Biwa Falls": "A 50-metre waterfall fifty metres to your left as you step off the "
   "Kazurabashi vine bridge. No walk required.",
 "Oku-Iya double vine bridges": "The 'husband and wife' pair of vine bridges deep in East "
   "Iya, with a hand-hauled cable cart slung across the river beside them. Far quieter than "
   "the famous one. Bus access is seasonal — daily only 1 Oct–3 Nov.",
 "Nagoro": "The scarecrow village: one resident has made life-size straw figures of every "
   "neighbour who died or moved away. Around 300 of them, and about 20 living people. "
   "Strange and quietly moving.",
 "Mt Tsurugi": "The second-highest peak in western Japan, and unusually easy — a chairlift "
   "lifts you from 1,420 m to 1,750 m and the ridge walk from the top station is gentle. "
   "Autumn colour arrives here in late October, weeks before the lowlands.",

 # ── Kōchi ───────────────────────────────────────────────────────────────────
 "Kōchi Castle": "One of only twelve original keeps left in Japan, and the ONLY one that "
   "still has both its main keep and its lord's residence standing. Ladder-stairs inside; "
   "the grounds are free.",
 "Sunday Market": "A 300-year-old street market, a kilometre of stalls running up Ōtesuji "
   "to the castle. SUNDAYS ONLY, and it is a morning market — go early.",
 "Hirome Market": "A covered hall of about sixty stalls: you buy from whichever you like "
   "and eat at shared tables. Order katsuo no tataki, bonito seared over burning rice "
   "straw. Loud and crowded; the stalls just outside are calmer.",
 "Katsurahama": "A pine-backed crescent of beach facing the open Pacific, with the statue "
   "of Sakamoto Ryōma looking out to sea. NO SWIMMING — the current is dangerous.",
 "Makino Botanical Garden": "A large botanical garden on Godaisan. Note it is on the side "
   "of a mountain, so it is not the flat stroll a botanical garden usually implies.",

 # ── Ehime ───────────────────────────────────────────────────────────────────
 "Matsuyama Castle": "One of only twelve original keeps in Japan, on a hill in the middle "
   "of the city, with connected walls you can walk. Take the CHAIR LIFT rather than the "
   "ropeway — same ticket, much shorter queue.",
 "Ninomaru Garden": "The garden below Matsuyama Castle, laid out over the old lord's "
   "residence. Flat, quiet, and cheap.",
 "Dogo Onsen": "One of the oldest hot springs in Japan, named in 8th-century chronicles and "
   "the model for the bathhouse in Spirited Away. Restoration finished July 2025. Wash "
   "thoroughly at the taps FIRST, no swimwear, towel out of the water.",
 "Asuka-no-Yu": "The modern annexe beside Dogo Onsen Honkan — cheaper, newer and much less "
   "crowded, with the same water.",
 "Botchan Train": "A replica Meiji-era steam locomotive that still runs through Matsuyama's "
   "streets, named after the Sōseki novel.",
 "Uchiko": "A merchant town that got rich on wax, with a preserved street of ochre-plastered "
   "townhouses and Uchiko-za, a 1916 wooden playhouse you can walk into, revolving stage "
   "and all.",
 "Ōzu": "A castle town on a river bend whose keep was rebuilt in WOOD in 2004 using the "
   "original techniques rather than concrete — rare, and you can tell.",

 # ── Setouchi / Hiroshima ────────────────────────────────────────────────────
 "Kōsanji": "A 1930s temple where a businessman built replicas of the finest temple "
   "buildings in Japan, all in one place. Riotous rather than restrained.",
 "Hill of Hope": "5,000 tonnes of Carrara marble carved into a hilltop above Kōsanji, on "
   "Ikuchijima. Included with Kōsanji admission.",
 "Ōkunoshima": "The rabbit island — around a thousand feral rabbits that mob you the moment "
   "you sit down. BUY PELLETS BEFORE YOU BOARD; none are sold on the island, and vegetables "
   "spoil and draw crows. Do not pick the rabbits up. The island also made poison gas for "
   "the Imperial Army, and the museum about it is unflinching.",
 "Takehara": "An Edo-era salt-and-sake merchant town of preserved streets, twelve minutes' "
   "walk from its station. Birthplace of Nikka Whisky's founder.",
 "Itsukushima Shrine": "Built on stilts over the water since the 12th century, with the "
   "great vermilion torii standing in the sea. Below 100 cm of tide you can walk out to the "
   "gate; above 250 cm it appears to float.",
 "Daishō-in": "The temple complex on the slope below Mt Misen — free, full of small "
   "sculptures, and far quieter than the shrine below it.",
 "Momijidani, Miyajima": "'Maple valley' — the park at the foot of the Mt Misen ropeway. "
   "Autumn colour arrives around 21–26 November, so in October it is simply a green valley "
   "with deer in it.",
 "Mt Misen": "The 535 m peak of Miyajima. A ropeway does most of the climbing; the summit "
   "is a further ~30 minutes of steep steps beyond the top station. LAST ASCENT 16:00.",
 "Mt Misen ropeway top": "Shishiiwa observatory, the ropeway's upper station — the Inland "
   "Sea panorama without the summit climb. This is where most people stop, and it is enough.",
 "Peace Memorial Museum": "The museum of the 1945 atomic bombing. Allow more time than you "
   "think, and expect to want quiet afterwards. Opens at 07:30 in autumn — the best-value "
   "early start anywhere on this route.",
 "A-Bomb Dome": "The skeletal remains of the Industrial Promotion Hall, left standing as it "
   "was. Free, outdoors, and floodlit at night.",

 # ── Awaji / Himeji ──────────────────────────────────────────────────────────
 "Himeji Castle": "The finest surviving castle in Japan — white plaster, six storeys, never "
   "bombed and never burned. The keep is capped at 1,000 entries an hour, so come early. "
   "Inside is six floors of steep ladder-stairs climbed in socks.",
 "Koko-en": "Nine walled Edo gardens beside Himeji Castle, on the site of the old samurai "
   "residences — a carp pond, a bamboo grove, a tea house and a flat gravel circuit. The "
   "combined castle ticket makes it almost free.",
 "Awaji Yumebutai": "A vast Tadao Ando concrete complex built into a scarred hillside, with "
   "a hundred stepped flower gardens. Free to walk through.",
 "Izanagi Shrine": "Said to be the oldest shrine in Japan — the creation myth has Awaji as "
   "the first island made, before the rest of the country.",
}
