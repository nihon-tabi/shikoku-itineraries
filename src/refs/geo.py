"""Places, Google Maps deep links, and inline linkification.

Every place named in the itinerary prose resolves to a lat/lng + place_id deep link,
geocoded once into places_geo.json. A plain text query would open a directions form
instead of the pin, which is the bug this file exists to prevent.
"""

# ── Google Maps links, by day ───────────────────────────────────────────────
_GEO = None


def _geo():
    """Lazy-load the geocode cache built by build/geocode_places.py."""
    global _GEO
    if _GEO is None:
        import json, os
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "places_geo.json")
        try:
            _GEO = json.load(open(p, encoding="utf-8"))
        except FileNotFoundError:
            _GEO = {}
    return _GEO


def gmap(q):
    """A Maps URL that always opens the PLACE, never a directions form.

    A name-only query is ambiguous — Google resolves it, but the app can drop the
    result into whatever mode it was last in. Passing resolved coordinates plus
    the place_id pins it to one specific place card. Falls back to a name search
    only where geocoding found nothing.
    """
    from urllib.parse import quote
    g = _geo().get(q)
    if g:
        url = (f"https://www.google.com/maps/search/?api=1"
               f"&query={g['lat']}%2C{g['lng']}")
        if g.get("place_id"):
            url += f"&query_place_id={g['place_id']}"
        return url
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)


MAPS = {
 "2026-10-09A": [("Himeji Castle", "姫路城 Himeji Castle"), ("Koko-en Garden", "好古園 Koko-en Himeji"),
                 ("Himeji Port", "姫路港 Himeji Port"), ("Fukuda Port", "福田港 Fukuda Port Shodoshima")],
 "2026-10-10A": [("Kankakei Ropeway", "寒霞渓ロープウェイ Kankakei Ropeway"),
                 ("Kusakabe Port", "草壁港 Kusakabe Port Shodoshima"),
                 ("Shodoshima Olive Park", "小豆島オリーブ公園 Olive Park")],
 "2026-10-11A": [("Angel Road", "エンジェルロード Angel Road Shodoshima"),
                 ("Tonoshō Port", "土庄港 Tonosho Port"), ("Takamatsu Port", "高松港 Takamatsu Port")],
 "2026-10-12A": [("Ritsurin Garden", "栗林公園 Ritsurin Garden Takamatsu")],
 "2026-10-13A": [("Awa Odori Kaikan", "阿波おどり会館 Tokushima"), ("Mt Bizan ropeway", "眉山ロープウェイ")],
 "2026-10-14A": [("Ōboke Station", "大歩危駅 Oboke Station"),
                 ("Ōboke gorge boat pier", "大歩危峡観光遊覧船"), ("Awa-Ikeda Station", "阿波池田駅")],
 "2026-10-15A": [("Iya Kazurabashi vine bridge", "祖谷のかずら橋"), ("Biwa Falls", "琵琶の滝 祖谷"),
                 ("Hotel Iya Onsen cable car", "ホテル祖谷温泉")],
 "2026-10-16A": [("Nagoro scarecrow village", "名頃かかしの里 Nagoro"),
                 ("Oku-Iya double vine bridges", "奥祖谷二重かずら橋"),
                 ("Mt Tsurugi chairlift", "剣山観光登山リフト 見ノ越")],
 "2026-10-17A": [("Hirome Market", "ひろめ市場 Kochi")],
 "2026-10-18A": [("Kōchi Sunday Market", "高知日曜市 Sunday Market"), ("Kōchi Castle", "高知城"),
                 ("Katsurahama", "桂浜 Katsurahama"), ("Makino Botanical Garden", "牧野植物園")],
 "2026-10-19A": [("Dogo Onsen Honkan", "道後温泉本館")],
 "2026-10-20A": [("Matsuyama Castle", "松山城 Matsuyama Castle")],
 "2026-10-21A": [("Imabari Station", "今治駅"), ("Onomichi Station", "尾道駅"),
                 ("Sunrise Itoyama cycle terminal", "サンライズ糸山")],
 "2026-10-22A": [("Tadanoumi Port", "忠海港 Tadanoumi Port"), ("Ōkunoshima", "大久野島 Rabbit Island"),
                 ("Takehara old town", "竹原町並み保存地区")],
 "2026-10-23A": [("Itsukushima Shrine torii", "厳島神社 大鳥居"),
                 ("Miyajima Ropeway", "宮島ロープウエー 紅葉谷"), ("Mt Misen", "弥山 宮島")],
 "2026-10-24A": [("Peace Memorial Museum", "広島平和記念資料館"), ("A-Bomb Dome", "原爆ドーム")],

 "2026-10-09B": [("Akashi Port", "明石港 淡路ジェノバライン"), ("Iwaya Port", "岩屋港 淡路島"),
                 ("Sumoto Bus Center", "洲本バスセンター")],
 "2026-10-10B": [("Awaji Yumebutai", "淡路夢舞台"), ("Izanagi Shrine", "伊弉諾神宮")],
 "2026-10-11B": [("Uzu-no-michi", "渦の道 鳴門"), ("Naruto Park", "鳴門公園"),
                 ("Ōtsuka Museum of Art", "大塚国際美術館")],
 "2026-10-12B": [("Awa Odori Kaikan", "阿波おどり会館 Tokushima"), ("Ryōzen-ji, Temple 1", "霊山寺 一番札所")],
 "2026-10-13B": [("Ōboke Station", "大歩危駅 Oboke Station"), ("Ōboke gorge boat pier", "大歩危峡観光遊覧船")],
 "2026-10-14B": [("Iya Kazurabashi vine bridge", "祖谷のかずら橋"), ("Biwa Falls", "琵琶の滝 祖谷")],
 "2026-10-15B": [("Nagoro scarecrow village", "名頃かかしの里 Nagoro"),
                 ("Oku-Iya double vine bridges", "奥祖谷二重かずら橋"),
                 ("Mt Tsurugi chairlift", "剣山観光登山リフト 見ノ越")],
 "2026-10-16B": [("Konpira-san", "金刀比羅宮 Kotohira"), ("Kanamaru-za kabuki theatre", "旧金毘羅大芝居 金丸座")],
 "2026-10-17B": [("Ritsurin Garden", "栗林公園 Ritsurin Garden Takamatsu"), ("Tonoshō Port", "土庄港")],
 "2026-10-18B": [("Kankakei Ropeway", "寒霞渓ロープウェイ"), ("Shodoshima Olive Park", "小豆島オリーブ公園")],
 "2026-10-19B": [("Angel Road", "エンジェルロード Angel Road Shodoshima")],
 "2026-10-20B": [("Dogo Onsen Honkan", "道後温泉本館")],
 "2026-10-21B": [("Matsuyama Castle", "松山城 Matsuyama Castle")],
 "2026-10-22B": [("Imabari Station", "今治駅"), ("Onomichi Station", "尾道駅")],
 "2026-10-23B": [("Tadanoumi Port", "忠海港"), ("Ōkunoshima", "大久野島 Rabbit Island")],
 "2026-10-24B": [("Itsukushima Shrine torii", "厳島神社 大鳥居"), ("Miyajima Ropeway", "宮島ロープウエー 紅葉谷")],
 "2026-10-25B": [("Peace Memorial Museum", "広島平和記念資料館"), ("A-Bomb Dome", "原爆ドーム")],
}


def maps_for(date, key):
    return MAPS.get(date + key, [])


MAPS["2026-10-09A"] = [("Himeji Castle","姫路城 Himeji Castle"),("Koko-en Garden","好古園 Koko-en Himeji"),
  ("Himeji Port","姫路港 Himeji Port"),("Fukuda Port","福田港 小豆島"),
  ("Hirokiya Ryokan, Yasuda","ひろきや旅館 小豆島"),("Yamaroku Soy Sauce","ヤマロク醤油"),
  ]


MAPS["2026-10-10A"] = [("Nakabu-an somen","なかぶ庵 小豆島"),("Kusakabe Port","草壁港"),
  ("Kouuntei ropeway base","紅雲亭 小豆島"),("Kankakei Ropeway","寒霞渓ロープウェイ"),
  ("Tonoshō Port","土庄港")]


MAPS["2026-10-18B"] = [("Kusakabe Port","草壁港"),("Kankakei Ropeway","寒霞渓ロープウェイ"),
  ("Kouuntei ropeway base","紅雲亭 小豆島"),
  ("Yamaroku Soy Sauce","ヤマロク醤油"),("Nakabu-an somen","なかぶ庵 小豆島")]


# ── Every named place, auto-detected from the day text ──────────────────────
# key = the exact string as it appears in the itinerary prose
PLACES = {
 # Himeji
 "Himeji Castle":"姫路城 Himeji Castle", "Koko-en":"好古園 Koko-en Himeji",
 "Himeji Port":"姫路港 Himeji Port", "JR Himeji Stn":"姫路駅 Himeji Station",
 # Shodoshima
 "Fukuda Port":"福田港 小豆島", "Yasuda":"安田 小豆島", "Hirokiya":"ひろきや旅館 小豆島",
 "Yamaroku":"ヤマロク醤油", "Marukin":"マルキン醤油記念館", "Nakabu-an":"なかぶ庵 小豆島",
 "Kankakei":"寒霞渓ロープウェイ", "Kusakabe Port":"草壁港", "Kouuntei":"紅雲亭 小豆島",
 "Tonoshō":"土庄港 Tonosho Port", "Angel Road":"エンジェルロード 小豆島",
 "Olive Park":"小豆島オリーブ公園", "Chigusa":"千種旅館 小豆島",
 # Kagawa
 "Takamatsu Port":"高松港 Takamatsu Port", "Ritsurin Garden":"栗林公園 Ritsurin Garden",
 "Ritsurin":"栗林公園 Ritsurin Garden", "Konpira-san":"金刀比羅宮 Kotohira",
 "Kanamaru-za":"旧金毘羅大芝居 金丸座", "Kotohira":"琴平駅 Kotohira Station",
 # Tokushima
 "Awa Odori Kaikan":"阿波おどり会館 徳島", "Mt Bizan":"眉山ロープウェイ 徳島",
 "Ryōzen-ji":"霊山寺 一番札所 徳島", "Awa-Ikeda":"阿波池田駅 Awa-Ikeda Station",
 "Ōboke":"大歩危駅 Oboke Station", "Iya Kazurabashi":"祖谷のかずら橋",
 "Kazurabashi":"祖谷のかずら橋", "Biwa Falls":"琵琶の滝 祖谷",
 "Hotel Iya Onsen":"ホテル祖谷温泉", "Ochiai village":"落合集落 三好市",
 "Nagoro":"名頃かかしの里 Nagoro", "Oku-Iya double vine bridges":"奥祖谷二重かずら橋",
 "Mt Tsurugi":"剣山 見ノ越 Mt Tsurugi", "Minokoshi":"見ノ越 剣山登山リフト",
 "Nishijima":"西島駅 剣山リフト", "Kubo":"久保 バス停 三好市",
 # Kōchi
 "Hirome Market":"ひろめ市場 高知", "Sunday Market":"高知日曜市",
 "Kōchi Castle":"高知城", "Katsurahama":"桂浜 高知", "Makino":"牧野植物園 高知",
 # Ehime
 "Dogo Onsen":"道後温泉本館", "Matsuyama Castle":"松山城",
 "Ninomaru":"松山城二之丸史跡庭園", "Botchan Train":"坊っちゃん列車 松山",
 "Uchiko":"内子座 内子町", "Ōzu":"大洲城 愛媛", "Imabari":"今治駅 Imabari Station",
 "Shimonada":"下灘駅 Shimonada Station",
 # Setouchi / Hiroshima
 "Onomichi":"尾道駅 Onomichi Station", "Innoshima Ōhashi":"因島大橋",
 "Shimanami Kaido":"しまなみ海道 サンライズ糸山", "Mihara":"三原駅 Mihara Station",
 "Ōkunoshima":"大久野島 Rabbit Island", "Tadanoumi":"忠海港 Tadanoumi Port",
 "Takehara":"竹原町並み保存地区", "Itsukushima":"厳島神社 大鳥居",
 "floating torii":"厳島神社 大鳥居", "Miyajima":"宮島口駅 Miyajimaguchi",
 "Mt Misen":"弥山 宮島 Mt Misen", "Shishiiwa":"獅子岩展望台 宮島",
 "Daishō-in":"大聖院 宮島", "Momijidani":"紅葉谷公園 宮島",
 "Peace Memorial":"広島平和記念資料館", "A-Bomb Dome":"原爆ドーム",
 # Awaji / Naruto
 "Akashi Port":"明石港 淡路ジェノバライン", "Iwaya Port":"岩屋港 淡路島",
 "Sumoto":"洲本バスセンター 淡路島", "Awaji Yumebutai":"淡路夢舞台",
 "Izanagi Shrine":"伊弉諾神宮 淡路島", "Uzu-no-michi":"渦の道 鳴門",
 "Naruto Park":"鳴門公園", "Ōtsuka Museum":"大塚国際美術館",
 "Kameura":"亀浦観光港 鳴門",
}


# Option A2 shares Option A's dates everywhere except 14–17 October, so inherit
# A's manual pins wholesale and then override the four days that differ. (A3
# re-dates everything after 17 October, so it cannot inherit this way and
# relies on auto-detection from its prose.)
for _d, _v in [(k[:-1], v) for k, v in list(MAPS.items()) if k.endswith("A")]:
    MAPS[_d + "A2"] = _v

MAPS["2026-10-14A2"] = [("Ōtsuka Museum of Art", "大塚国際美術館"), ("Uzu-no-michi", "渦の道 鳴門"),
                        ("Naruto Park", "鳴門公園"), ("Kameura", "亀浦観光港 鳴門"),
                        ("Awa Odori Kaikan", "阿波おどり会館 Tokushima")]
MAPS["2026-10-15A2"] = MAPS["2026-10-14A"]
MAPS["2026-10-16A2"] = MAPS["2026-10-16A"]
MAPS["2026-10-17A2"] = [("Iya Kazurabashi vine bridge", "祖谷のかずら橋"), ("Biwa Falls", "琵琶の滝 祖谷"),
                        ("Ōboke Station", "大歩危駅 Oboke Station"),
                        ("Hirome Market", "ひろめ市場 Kochi")]

def places_in(text):
    """Return [(name, mapurl)] for every PLACES key appearing in `text`,
    longest first so 'Iya Kazurabashi' wins over 'Kazurabashi'."""
    low = text.lower()
    found, used = [], []
    for k in sorted(PLACES, key=len, reverse=True):
        # case-insensitive: the prose SHOUTS a headline place ("ZENIGATA SUNAE")
        # and the pin list must still find it
        if k.lower() in low and not any(k.lower() in u for u in used):
            used.append(k.lower())
            found.append((k, gmap(PLACES[k])))
    return found


def day_places(day, key):
    """All places for a day: auto-detected from its prose, plus any manual pins."""
    blob = " ".join([day["title"], " ".join(day["do"]), day["travel"],
                     " ".join(day["watch"]), day["sleep"]])
    out, urls = [], set()
    for n, u in places_in(blob) + [(n, gmap(q)) for n, q in MAPS.get(day["date"] + key, [])]:
        if u in urls:          # two aliases of one place ("Ritsurin" / "Ritsurin Garden")
            continue           # resolve to the same pin — show it once
        urls.add(u)
        out.append((n, u))
    return out


def linkify(text, key=None):
    """Wrap the first mention of each place in `text` in a Maps link.

    - case-INSENSITIVE, because the itinerary writes some names in caps
    - longest-first, so "Iya Kazurabashi" wins over "Kazurabashi"
    - one link per TARGET, not per dictionary key, so two names for the same
      place don't both light up
    - the matched text is preserved exactly as written

    Input must already be HTML-escaped.
    """
    import re
    spans, taken, linked_targets = [], [], set()
    for name in sorted(PLACES, key=len, reverse=True):
        target = PLACES[name]
        if target in linked_targets:
            continue
        m = re.search(re.escape(name), text, re.IGNORECASE)
        if not m:
            continue
        a, b = m.span()
        if any(a < tb and ta < b for ta, tb in taken):
            continue
        taken.append((a, b))
        linked_targets.add(target)
        spans.append((a, b))
    if not spans:
        return text
    out, last = [], 0
    for a, b in sorted(spans):
        out.append(text[last:a])
        # find which place this span belongs to
        frag = text[a:b]
        target = next(PLACES[n] for n in sorted(PLACES, key=len, reverse=True)
                      if n.lower() == frag.lower())
        out.append(f'<a class="ml" href="{gmap(target)}" target="_blank" '
                   f'rel="noopener">{frag}</a>')
        last = b
    out.append(text[last:])
    return "".join(out)


PLACES.update({
 "Takaya Shrine":"高屋神社 本宮 天空の鳥居",
 "Gate in the Sky":"高屋神社 本宮 天空の鳥居",
 "lower shrine":"高屋神社 下宮 観音寺市",
 "Ariake Ground":"有明グラウンド 琴弾公園 観音寺市",
 "Kan-onji":"観音寺駅 Kanonji Station",
 "Kotohiki Park":"琴弾公園 観音寺市",
 "Zenigata Sunae":"銭形展望台 観音寺市",
 "Zenigata":"銭形展望台 観音寺市",
 "Chichibugahama":"父母ヶ浜 三豊市",
 "Takuma":"詫間駅 Takuma Station",
 "Tamamo Park":"玉藻公園 高松城跡",
 "Shikoku Mura":"四国村ミウゼアム 屋島",
 "Yashima":"屋島山上 高松市",
})


# ── Places that only appear as leg endpoints, bed names or attraction rows ───
# Until now these rendered as plain text: the transport table, the "Sleep in"
# line and the attractions panel had no pins at all. Anything genuinely not a
# place ("up and back", "Big bags", "City trams") is deliberately absent.
PLACES.update({
 # cities and hubs
 "Osaka":"大阪駅 Osaka Station", "Kobe Sannomiya":"三宮駅 Sannomiya Station",
 "Kobe":"神戸三宮フェリーターミナル", "Himeji":"姫路駅 Himeji Station",
 "Akashi":"明石駅 Akashi Station", "Takamatsu":"高松駅 Takamatsu Station",
 "Tokushima Stn":"徳島駅 Tokushima Station", "Tokushima":"徳島駅 Tokushima Station",
 "Kōchi":"高知駅 Kochi Station", "Matsuyama":"松山市駅 Matsuyama",
 "JR Matsuyama Stn":"松山駅 JR Matsuyama Station",
 "Matsuyama Kanko Port":"松山観光港 Matsuyama Kanko Port",
 "Hiroshima Bus Centre":"広島バスセンター", "Hiroshima Port":"広島港 宇品",
 "Hiroshima":"広島駅 Hiroshima Station",
 "Iwaya":"岩屋港 淡路島",
 "Naruto-kōen-guchi":"鳴門公園口バス停",
 # Setouchi islands
 "Miyanoura":"宮浦港 直島", "Naoshima":"直島 宮浦港",
 "Setoda Port":"瀬戸田港 生口島", "Setoda BS":"瀬戸田バスストップ",
 "Setoda":"瀬戸田港 生口島", "Ōmishima BS":"大三島バスストップ",
 "Ōmishima":"大三島 井口港", "Ōshima":"大島 今治市 宮窪",
 "Mukaishima":"向島 兼吉渡船場", "Sunrise Itoyama":"サンライズ糸山 今治",
 # the Ōboke boat pier — the cruise had NO pin, only the station 4 min away
 "Ōboke-kyō boat pier":"大歩危峡まんなか 遊覧船乗り場",
 "gorge cruise":"大歩危峡まんなか 遊覧船乗り場",
 # beds
 "Hirokiya Ryokan":"ひろきや旅館 小豆島", "WeBase":"WeBase高松",
 "Hostel PAQ":"ホステルパク 徳島", "4S STAY":"4S STAY 阿波池田駅前",
 "Guesthouse Yadocurly":"ゲストハウス ヤドカーリー 尾道",
 "Fuji Hostel":"フジホステル 尾道", "Anago no Nedoko":"あなごのねどこ 尾道",
 "The Evergreen Hostel":"The Evergreen Hostel Hiroshima",
 "J-Hoppers":"J-Hoppers Hiroshima Guesthouse",
 "Guesthouse Casablanca":"ゲストハウス カサブランカ 松山",
 "Kotohira Park Hotel":"琴平パークホテル",
 "Awaji Tourist Trophy House":"淡路島公園 ツーリストトロフィーハウス",
 "I-Link Hostel":"I-Link Hostel 大三島", "WAKKA":"WAKKA 大三島",
 "Cycle Guest House Shiokaze":"シクロの家 しまなみ 瀬戸田",
 # attractions with no pin of their own
 "Chichu Art Museum":"地中美術館 直島", "Teshima Art Museum":"豊島美術館",
 "Benesse House Museum":"ベネッセハウス ミュージアム 直島",
 "Lee Ufan Museum":"李禹煥美術館 直島", "Honmura":"家プロジェクト 本村 直島",
 "Kōsanji":"耕三寺博物館 生口島", "Hill of Hope":"未来心の丘 生口島",
 "Asuka-no-Yu":"道後温泉別館 飛鳥乃湯泉",
 "Wonder Naruto":"亀浦観光港 うずしお観潮船",
 "Matsuyama ropeway":"松山城ロープウェイ東雲口駅舎",
})


def pin(label):
    """Map URL for a SHORT label (a leg endpoint, an attraction name, a bed).

    Returns None when the label names no place — "up and back", "Big bags",
    "City trams", "—". Those must stay unlinked rather than link to something
    plausible-looking and wrong.
    """
    if not label:
        return None
    found = places_in(label)
    return found[0][1] if found else None


_URL_RE = None
def autolink(html):
    """Turn a bare http(s) URL in already-escaped text into a real link.

    Tide tables, mirror calendars and tide-grade pages are quoted by URL in the
    day text so the traveller can check their own date. Printing the URL and not
    linking it makes them retype it on a phone.
    """
    global _URL_RE
    import re
    if _URL_RE is None:
        _URL_RE = re.compile(r'(?<![">])(https?://[^\s<>"\')]+[^\s<>"\').,;:])')
    return _URL_RE.sub(
        lambda m: f'<a class="ml" href="{m.group(1)}" target="_blank" rel="noopener">'
                  f'{m.group(1).split("//")[-1][:46]}\u2197</a>', html)
