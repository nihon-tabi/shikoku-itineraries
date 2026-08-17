# Autumn foliage (紅葉) timing for the 9 Oct – 1 Nov 2026 window

**Blunt summary: this is not an autumn-foliage trip. It is a *pre-foliage* trip with
exactly one real koyo destination — the Mt Tsurugi massif — plus a marginal taste at
Iya-kei and the top of Kankakei in the final days.**

## How this was sourced

n-kishou's 紅葉ナビ is now a JS single-page app; the public URLs return an empty shell.
The researcher reverse-engineered the bundle and pulled n-kishou's own JSON endpoints:

- `other-api-prod.n-kishou.co.jp/list-jr-points?type=koyo&filter_mode=forecast&area_mode=pref&area_code=<PP>` — per-spot 見頃 start/peak/end
- `tennavi-data-prod.n-kishou.co.jp/koyo/static_info/<code>.json` — species, 例年の見頃
- `tennavi-data-prod.n-kishou.co.jp/koyo/observation/<code>.json` — **observed** state
  (0=青葉 green, 1=始め, 2=見頃, 3=色あせ, 4=落ち葉)
- `tennavi-data-prod.n-kishou.co.jp/koyo/jma_sample/koyo_past_observation.json` —
  **observed** all-time earliest/latest per city

Spot data is the 2025 season's **revised forecast (第3回)**, stamped `2025-11-04`.
Fallbacks where n-kishou has no coverage: WalkerPlus 紅葉 (which usefully publishes
**色づき始め and 見頃 separately**) and the Kankakei operator's own dated reports.

---

## 1. n-kishou spot data — 2025 season, revised 2025-11-04

All dates are **見頃 (best viewing)**, not 色づき始め.

| Spot | 見頃 start | **peak** | end | 例年の見頃 | Species |
| --- | --- | --- | --- | --- | --- |
| **好古園** Koko-en, Himeji | 11/27 | **11/30** | 12/05 | 11月中旬～下旬 | イタヤカエデ, ヤマモミジ, ハウチワカエデ |
| **寒霞渓** Kankakei, Shodoshima | 11/20 | **11/27** | 12/08 | 11月上旬～下旬 | イロハカエデ, ヤマモミジ, アカシデ (50+ spp.) |
| **栗林公園** Ritsurin, Takamatsu | 11/28 | **12/03** | 12/10 | 11月中旬～12月上旬 | カエデ, ハゼノキ |
| **⭐ 剣山** Mt Tsurugi | **10/25** | **11/01** | 11/12 | **10月中旬～11月上旬** | カエデ, ブナ, ナナカマド |
| **中津渓谷** Nakatsu-keikoku, Kōchi | 11/24 | **11/27** | 12/02 | 11月中旬～下旬 | モミジ |
| **松山城** Matsuyama Castle | 12/04 | **12/07** | 12/12 | 11月下旬～12月上旬 | カエデ |
| **耕三寺** Kōsanji, Ikuchijima (Shimanami) | 11/26 | **12/01** | 12/09 | 11月中旬～12月上旬 | カエデ, イチョウ |
| **宮島 紅葉谷公園** Momijidani | 11/21 | **11/26** | 12/03 | 11月中旬～下旬 | イロハカエデ, オオモミジ |

**Elevations** (from n-kishou's separate mountain dataset):
剣山 **1,955 m** · 次郎笈 1,930 m · 三嶺 1,894 m · 祖谷渓 **403 m** ·
大歩危・小歩危 **305 m** · 星ヶ城山 (above Kankakei) 816 m.

> **n-kishou's own description of Tsurugi is the single most useful line in the dataset:**
> 「10月上旬、剣山(標高1955m)頂上部から紅葉が始まり、段々と里まで色づいてきます。」
> *From early October, foliage begins at the summit of Mt Tsurugi (1,955 m) and
> gradually colours down to the villages.*

⚠️ **Not in n-kishou's spot database at all:** Himeji Castle grounds, 大歩危/小歩危,
祖谷渓, かずら橋, 奥祖谷, Kōchi city, Dogo, Onomichi/千光寺, Takehara, 弥山 Mt Misen,
縮景園 Shukkeien. They have only 4 spots in all of Tokushima.

---

## 2. The two pieces of hard *observed* data that settle it

### (a) Miyajima was **completely green** on 12 October 2025

From n-kishou's own observation feed, via the Wayback Machine:

```
34360005 (宮島 紅葉谷公園)  @ 2025-10-12 → observation_state "0" = 青葉 (green)
34360015 (極楽寺山, 693 m)  @ 2025-10-12 → observation_state "0" = 青葉 (green)
```
<https://web.archive.org/web/20251012233941id_/https://tennavi-data-prod.n-kishou.co.jp/koyo/observation/34360005.json>

**Even the 693 m mountain above Hiroshima Bay was green on 12 October.**

### (b) In ~65 years of JMA record, no city on this route has EVER had full kaede colour in October

Observed, not forecast:

| City | 2024 observed | **All-time earliest** | All-time latest |
| --- | --- | --- | --- |
| 高松 Takamatsu | 12/8 | **11/3** (1982) | 12/8 (2024) |
| 松山 Matsuyama | 12/16 | **11/3** (1966) | 12/18 (1998) |
| 広島 Hiroshima | 12/2 | **11/8** (1976) | 12/8 (1961) |
| 高知 Kōchi | 12/12 | **11/8** (1983) | 12/13 (2000) |
| 神戸 Kobe (proxy for Himeji) | 12/2 | **11/11** (1974) | 12/11 (2011) |
| 徳島 Tokushima | 12/5 | **11/19** (2012) | 12/9 (1993) |

*Caveat: JMA's criterion is a single sample tree fully turned, systematically later than
a tourist spot's 見頃. But the earliest-ever column is unambiguous — not one October
date, ever.*

### (c) Year-to-year variance is small

| City | 2019 | 2021 | 2022 | 2023 | 2024 | 2025 | 平年 | Spread |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 広島 kaede | 11/26 | 11/26 | 11/26 | 11/28 | 12/2 | 11/30 | 11/22 | **7 d** |
| 高知 kaede | 12/07 | 12/06 | 12/7 | 12/9 | 12/12 | 12/13 | 12/2 | **8 d** |

**~7–8 days of spread for kaede.** Even a record-early year does not pull lowland peak
into October; 2024 and 2025 both ran 6–13 days *late*.

---

## 3. ⭐ Kankakei — first-party observed reports, three years

The operator runs a dated 紅葉情報 series at <https://kankakei.co.jp/pickup/koyo.html>.
This is the best real-world record on the route, and it demonstrates the altitude
gradient directly. **Summit station 612 m, 四方指大観峰 777 m, base 紅雲亭 ~250 m.**

**2025:** 10/30 「全体的な紅葉の見頃はもう少し先」 · 11/05 summit + 777 m 「まもなく見頃」 ·
11/11 「山頂から中腹にかけて…見ごろ」 · 11/20 「最盛期」 · 11/24 見頃 reaches the base
**2024:** **10/24 「寒霞渓山頂の紅葉は、一部分が色づき始めました」** ← 色づき始め, summit only ·
10/30 only the cherries have advanced · 11/17 「寒霞渓全域にて紅葉が見ごろ」
**2023:** 10/31 the 777 m viewpoint progressing · **11/05 「山頂から約1ヵ月をかけて…山麓まで
紅葉が広がりはじめそう」** ← their own statement that summit→base takes about a month ·
11/18 全域見頃

> **全域見頃 fell 11/17 (2024), 11/18 (2023), 11/20 (2025) — a 3-day spread across three
> years. Extremely stable. And in all three years, 30 October was still "not yet".**

---

## 4. Verdict per spot, 9 Oct – 1 Nov 2026

| Spot | Verdict |
| --- | --- |
| **Himeji — Koko-en** | ❌ **FAR too early.** Peak 11/30; observed 11/25–12/01 in 2024. 6–8 weeks early. |
| **Kankakei, Shodoshima** | ⚠️ **Too early at the base — the summit is the exception.** Their own reports had the 777 m viewpoint 色づき始め on **10/24 (2024)**. A ropeway ride ~28 Oct–1 Nov may catch *partial early colour at the top only*. |
| **Ritsurin Garden** | ❌ **The worst miss on the route.** Peak **12/03**; Takamatsu's all-time-earliest is 11/3. Dead green. |
| **Iya-kei 祖谷渓 (403 m)** | ⚠️ **The one marginal lowland win.** 色づき始め **10月下旬**, 見頃 10月下旬～11月中旬; 2025 window 10/21–11/20. The last ~5 days clip the very start. |
| **Ōboke / Koboke (305 m)** | ❌ Too early. 色づき始め 11月初旬, 見頃 11月中旬～下旬. |
| **Kazurabashi かずら橋** | ❌ Too early. WalkerPlus separates it explicitly: 色づき始め **11月上旬**. Just misses. |
| **⭐ Mt Tsurugi 剣山 (1,955 m)** | ✅ **THIS IS THE ONE — on time in the BACK HALF of the window.** n-kishou 2025: 見頃 **10/25 → peak 11/01 → 11/12**. WalkerPlus 例年: 色づき始め 10月上旬, 見頃 **10月中旬～下旬**, 2025 window 10/11–10/31. **Both agree peak lands 25 Oct – 1 Nov.** |
| **Kōchi city / 中津渓谷** | ❌ Too early. Nakatsu peak 11/27; city forecast 12/13. |
| **Matsuyama Castle / Dogo** | ❌ **Second-worst miss.** 見頃 starts **12/04**, peak **12/07**. ~6 weeks early. |
| **Onomichi / Shimanami** | ❌ Too early. 耕三寺 peaks **12/01**. |
| **Takehara** | ❌ No published data; same lowland Setouchi climate. Assume too early. |
| **Miyajima 紅葉谷公園** | ❌ **Too early — and this one is measured, not guessed.** Observed **green on 12 Oct 2025**. Peak 11/26; observed 11/26–12/06 in 2024. ~6 weeks early. |
| **Miyajima 弥山 Mt Misen (535 m)** | ❌ Not stated — but 極楽寺山 (693 m, 8 km away) was also **green on 12 Oct 2025**. Will not be in colour. |
| **Hiroshima 縮景園** | ❌ Not stated. City kaede 11/30 (2025), all-time-earliest 11/8. |

---

## 5. The altitude gradient, quantified

| Site | Elevation | 2025 見頃 peak | Days later than Tsurugi |
| --- | --- | --- | --- |
| **剣山 Mt Tsurugi summit** | **1,955 m** | **11/01** | — |
| 氷ノ山 (Hyogo) | 1,510 m | 11/07 | +6 |
| 天狗高原 (Kōchi) | ~1,400 m | 11/09 | +8 |
| 宮島 紅葉谷公園 | ~50 m | 11/26 | +25 |
| 寒霞渓 Kankakei (whole gorge) | 250–816 m | 11/27 | **+26** |
| 好古園 Koko-en | ~15 m | 11/30 | +29 |
| 栗林公園 Ritsurin | ~10 m | 12/03 | **+32** |
| 松山城 Matsuyama Castle | ~130 m | 12/07 | **+36** |

> **The gap between the top of Mt Tsurugi and the lowland gardens of Shikoku is roughly
> one full month — 26 to 36 days.** Kankakei's operator says the same about their own
> 566 m of relief: 「山頂から約1ヵ月をかけて…山麓まで紅葉が広がりはじめそう」.

---

## 6. What WILL be in colour — and the one itinerary implication

1. **⭐ Mt Tsurugi (1,955 m) — the only reliable hit.** Colour starts at the summit in
   **early October**; 見頃 runs **10/25–11/12**. **Go in the last week and you hit peak;
   go 9–15 Oct and you get early summit colour, not peak.**
2. **Iya-kei (403 m) — marginal, last few days only.** 色づき始め 10月下旬.
   The neighbouring 1,600–1,900 m peaks (次郎笈 1,930 m, 三嶺 1,894 m, 丸笹山 1,712 m)
   are the same band as Tsurugi and will be turning — visible from the ridge, though
   none publishes dates.
3. **Kankakei's summit only, in the last few days** (~29 Oct – 1 Nov). Nothing at the base.
4. **雲辺寺 Unpenji (927 m, near Ōboke)** — 例年 見頃 11月上旬; the very end of the
   window touches its start.

### The trade, stated plainly

**Tsurugi peaks 25 Oct – 1 Nov. Kankakei, Miyajima and Koko-en peak 17–30 November.**
Those two targets are **~4 weeks apart and cannot both be caught on one three-week
pass.** Shifting the trip ~3 weeks later (start ~1 Nov) would catch the famous lowland
sites at the cost of Tsurugi, whose colour is gone by mid-November.

⚠️ **With a fixed 9 October departure and a westward exit, Iya necessarily lands
mid-October** — Tsurugi will be at 色づき始め on the summit, not peak. That is still
worth doing; it is simply not the postcard.
