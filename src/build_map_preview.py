"""Render the My Maps export as a reviewable page.

Google My Maps has no write API, so the KMZ has to be imported by hand — which
makes reviewing 120 entries a chore, because checking one means importing all
of them. This renders the SAME spec file as a page: every pin plotted at its
real coordinate, every entry shown exactly as it will read in My Maps.

Generated from out/shikoku-mymaps.json, so it cannot drift from the KMZ.

    python -m src.build_map_preview
"""
import base64
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
SPEC = os.path.join(OUT, "shikoku-mymaps.json")
SKILL = os.path.expanduser("~/projects/japan-trip-planner/.claude/skills/japan-my-maps")
GLYPH_DIR = os.path.join(SKILL, "assets", "glyphs")

FOLDER_COLOUR = {
    "Attractions": "795548",
    "Nature views & Hikes": "DB4436",
    "Shrines and Temples": "9C27B0",
    "Food and Markets": "E65100",
    "Accommodation": "AFB42B",
    "Stations, Ports and Stops": "0288D1",
}


ICON_CACHE = os.path.join(HERE, "refs", "map_icons.json")


def icon_data_uris(spec, refresh=False):
    """Recolour each stock glyph to its folder colour and inline it.

    The artifact CSP blocks every external request, so the icons must travel
    with the page. They are small — 27 come to about 90 KB.

    The result is cached in refs/map_icons.json and only regenerated with
    --refresh, so the ordinary build needs no image library. The recolouring
    depends on the icon set, not on the trip, and the icon set almost never
    changes.
    """
    if not refresh and os.path.exists(ICON_CACHE):
        cached = json.load(open(ICON_CACHE))
        needed = {p["icon"] for f in spec["folders"] for p in f["places"]}
        missing = needed - set(cached)
        if not missing:
            return cached
        print(f"  {len(missing)} icon(s) not cached, regenerating: "
              f"{', '.join(sorted(missing))}")
    from PIL import Image  # only needed when (re)generating
    out = {}
    needed = {p["icon"] for f in spec["folders"] for p in f["places"]}
    for icon in sorted(needed):
        if icon.startswith("custom:"):
            im = Image.open(os.path.join(
                SKILL, "assets", "icons", icon.split(":", 1)[1] + ".png")).convert("RGBA")
        else:
            glyph, hexrgb = icon.split("-")
            r0, g0, b0 = (int(hexrgb[i:i + 2], 16) for i in (0, 2, 4))
            im = Image.open(os.path.join(GLYPH_DIR, f"{glyph}.png")).convert("RGBA")
            px = im.load()
            for y in range(im.size[1]):
                for x in range(im.size[0]):
                    r, g, b, a = px[x, y]
                    if a == 0:
                        continue
                    # distance from white keeps the antialiased glyph edge
                    w = min(r, g, b) / 255.0
                    px[x, y] = (int(r0 + (255 - r0) * w),
                                int(g0 + (255 - g0) * w),
                                int(b0 + (255 - b0) * w), a)
        im.thumbnail((40, 40))
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        out[icon] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    json.dump(out, open(ICON_CACHE, "w"))
    return out


def build(refresh_icons=False):
    spec = json.load(open(SPEC))
    icons = icon_data_uris(spec, refresh_icons)

    pins = []
    for f in spec["folders"]:
        for p in f["places"]:
            pins.append({**p, "folder": f["name"]})

    lats = [p["lat"] for p in pins]
    lons = [p["lon"] for p in pins]
    payload = {
        "title": spec["name"],
        "note": spec["description"],
        "bounds": {"minLat": min(lats), "maxLat": max(lats),
                   "minLon": min(lons), "maxLon": max(lons)},
        "folders": [{"name": f["name"], "colour": FOLDER_COLOUR[f["name"]],
                     "count": len(f["places"])} for f in spec["folders"]],
        "pins": pins,
        "icons": icons,
    }

    body = TEMPLATE.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False))

    # Two files from one render, because each channel rejects the other's form.
    # The full document is the normal case, so it gets the plain name; the
    # fragment is for a host that supplies its own <head>. Publishing the full
    # document nests it inside the host's body and the browser discards the
    # inner <head>, taking the VIEWPORT tag with it. Opening the fragment
    # locally has no charset — and this page is full of Japanese and ¥.
    # Lift the <title> into the real <head> rather than leaving the browser to
    # hoist it from the body.
    m = re.match(r"\s*(<title>.*?</title>)\n?", body, re.S)
    title_tag, rest = (m.group(1), body[m.end():]) if m else ("<title>Map preview</title>", body)
    shell = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        "<meta name=\"color-scheme\" content=\"light dark\">\n"
        + title_tag + "\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n"
    )
    full = os.path.join(OUT, "map-preview.html")
    frag = os.path.join(OUT, "map-preview-artifact.html")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(shell)
    with open(frag, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"{len(pins)} pins, {len(icons)} icons")
    print(f"  {full} ({os.path.getsize(full)/1024:.0f} KB)  <- open this one")
    print(f"  {frag} ({os.path.getsize(frag)/1024:.0f} KB)  <- body only, for publishing")
    return full


TEMPLATE = r"""<title>Shikoku, Setouchi and Hiroshima — map preview</title>
<style>
/* The six category colours ARE the data, so the chrome stays neutral and lets
   them be the only saturated thing on the page. */
:root{
  --paper:#F7F5F1; --surface:#FFFFFF; --sunk:#EFEBE4;
  --ink:#1B1F26; --ink-soft:#5A6472; --ink-faint:#8B94A2;
  --line:#DED8CE; --line-soft:#EAE5DC;
  --accent:#2C3A4B;
  --sea:#E4E9EC; --land:#F2EEE7;
  --radius:10px;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Noto Sans JP",sans-serif;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#14171C; --surface:#1B1F26; --sunk:#0F1216;
  --ink:#E9E6E1; --ink-soft:#A2ACBA; --ink-faint:#6C7686;
  --line:rgb(255 255 255/12%); --line-soft:rgb(255 255 255/7%);
  --accent:#9FB4CE;
  --sea:#171C22; --land:#1E242B;
}}
:root[data-theme="dark"]{
  --paper:#14171C; --surface:#1B1F26; --sunk:#0F1216;
  --ink:#E9E6E1; --ink-soft:#A2ACBA; --ink-faint:#6C7686;
  --line:rgb(255 255 255/12%); --line-soft:rgb(255 255 255/7%);
  --accent:#9FB4CE;
  --sea:#171C22; --land:#1E242B;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--serif);font-weight:600;text-wrap:balance;margin:0}
a{color:var(--accent)}
.wrap{max-width:1400px;margin:0 auto;padding:28px 20px 64px}

header{margin-bottom:22px}
h1{font-size:clamp(1.5rem,3.2vw,2.1rem);letter-spacing:-.015em}
.sub{color:var(--ink-soft);margin-top:6px;max-width:62ch}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:99px;
  padding:5px 12px;font-size:.8rem;color:var(--ink-soft);
  font-variant-numeric:tabular-nums}
.stat b{color:var(--ink);font-weight:600}

.layout{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:22px;align-items:start}
@media(max-width:960px){.layout{grid-template-columns:1fr}}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  box-shadow:inset 0 1px 0 0 rgb(255 255 255/45%)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .panel{
  box-shadow:inset 0 1px 0 0 rgb(255 255 255/6%)}}

.mapwrap{position:sticky;top:18px;padding:14px}
@media(max-width:960px){.mapwrap{position:static}}
svg.map{width:100%;height:auto;display:block;border-radius:6px;background:var(--sea);
  touch-action:manipulation}
.legend{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.leg{display:flex;align-items:center;gap:7px;border:1px solid var(--line);
  background:var(--paper);border-radius:99px;padding:5px 11px 5px 8px;cursor:pointer;
  font-size:.78rem;color:var(--ink-soft);transition:.15s cubic-bezier(.4,0,.2,1)}
.leg:hover{border-color:var(--ink-faint)}
.leg[aria-pressed="false"]{opacity:.4}
.leg .dot{width:11px;height:11px;border-radius:50%;flex:0 0 auto}
.leg b{color:var(--ink);font-variant-numeric:tabular-nums;font-weight:600}
.leg:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.tools{display:flex;gap:9px;margin-bottom:12px}
input[type=search]{flex:1;font:inherit;font-size:.9rem;padding:9px 12px;color:var(--ink);
  background:var(--surface);border:1px solid var(--line);border-radius:8px}
input[type=search]:focus-visible{outline:2px solid var(--accent);outline-offset:1px;border-color:transparent}

.list{max-height:none}
.grp{padding:0}
.grp h2{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;
  font-family:var(--sans);font-weight:700;color:var(--ink-faint);
  padding:16px 16px 8px;display:flex;gap:9px;align-items:center}
.grp h2 .dot{width:9px;height:9px;border-radius:50%}
.grp h2 .n{margin-left:auto;font-variant-numeric:tabular-nums;color:var(--ink-faint)}

.pin{border-top:1px solid var(--line-soft)}
.pin>summary{list-style:none;cursor:pointer;padding:10px 16px;display:flex;gap:11px;
  align-items:center;transition:background .15s cubic-bezier(.4,0,.2,1)}
.pin>summary::-webkit-details-marker{display:none}
.pin>summary:hover{background:var(--sunk)}
.pin>summary:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.pin img{width:22px;height:22px;flex:0 0 auto}
.pin .nm{font-weight:500;min-width:0}
.pin .mc{margin-left:auto;font-family:var(--mono);font-size:.72rem;color:var(--ink-faint);
  white-space:nowrap;font-variant-numeric:tabular-nums}
.pin[open]>summary{background:var(--sunk)}
.body{padding:2px 16px 18px 49px;font-size:.86rem;color:var(--ink-soft);
  white-space:pre-wrap;overflow-wrap:anywhere}
.body a{overflow-wrap:anywhere}
.pin.hit{background:color-mix(in srgb,var(--accent) 8%,transparent)}

.pindot{cursor:pointer}
.pindot circle{transition:r .15s cubic-bezier(.4,0,.2,1)}
.pindot:hover circle.hitbox,.pindot.sel circle.hitbox{r:9}
.pindot.sel circle.ring{stroke:var(--ink);stroke-width:2}
.empty{padding:26px 16px;color:var(--ink-faint);font-size:.86rem}
.foot{margin-top:26px;color:var(--ink-faint);font-size:.78rem;max-width:70ch}
</style>

<div class="wrap">
<header>
  <h1 id="ttl"></h1>
  <p class="sub" id="note"></p>
  <div class="stats" id="stats"></div>
</header>

<div class="layout">
  <div class="panel mapwrap">
    <svg class="map" id="map" viewBox="0 0 1000 560" role="img" aria-label="Map of every pin"></svg>
    <div class="legend" id="legend"></div>
  </div>

  <div>
    <div class="tools">
      <input type="search" id="q" placeholder="Search names, addresses, prices, map codes…" aria-label="Search pins">
    </div>
    <div class="panel list" id="list"></div>
  </div>
</div>

<p class="foot" id="foot"></p>
</div>

<script>
const D = __PAYLOAD__;
const $ = s => document.querySelector(s);

document.title = D.title;
$('#ttl').textContent = D.title;
$('#note').textContent = D.note;

const hidden = new Set();
let selected = null;

/* Equirectangular, with longitude squeezed by cos(lat) so the Inland Sea keeps
   its real proportions rather than being stretched east-west. */
const PAD = 34, W = 1000, H = 560;
const b = D.bounds, midLat = (b.minLat + b.maxLat) / 2;
const kx = Math.cos(midLat * Math.PI / 180);
const spanX = (b.maxLon - b.minLon) * kx, spanY = (b.maxLat - b.minLat);
const scale = Math.min((W - PAD * 2) / spanX, (H - PAD * 2) / spanY);
const offX = (W - spanX * scale) / 2, offY = (H - spanY * scale) / 2;
const px = p => offX + (p.lon - b.minLon) * kx * scale;
const py = p => offY + (b.maxLat - p.lat) * scale;

const stats = [
  ['pins', D.pins.length],
  ['folders', D.folders.length],
  ['with a map code', D.pins.filter(p => /Map code: (?!not stated)/.test(p.description)).length],
  ['with a phone', D.pins.filter(p => !/Phone number: not stated/.test(p.description)).length],
  ['with sourced hours', D.pins.filter(p => p.description.includes('Hours & Admission')).length],
];
$('#stats').innerHTML = stats.map(([k, v]) => `<span class="stat"><b>${v}</b> ${k}</span>`).join('');

$('#legend').innerHTML = D.folders.map(f =>
  `<button class="leg" aria-pressed="true" data-f="${esc(f.name)}">
     <span class="dot" style="background:#${f.colour}"></span>${esc(f.name)} <b>${f.count}</b>
   </button>`).join('');

function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

/* Entries are stored as My Maps HTML (<br> and bare URLs). Render them the way
   My Maps will, so what you review is what you get. */
function bodyHtml(desc){
  return esc(desc)
    .replace(/&lt;br&gt;/g, '\n')
    .replace(/(https?:\/\/[^\s<]+)/g, u => `<a href="${u}" target="_blank" rel="noopener">${u}</a>`);
}

function drawMap(){
  const parts = [`<rect width="${W}" height="${H}" fill="var(--land)"/>`];
  for (const [i, p] of D.pins.entries()){
    if (hidden.has(p.folder)) continue;
    const c = D.folders.find(f => f.name === p.folder).colour;
    parts.push(
      `<g class="pindot${selected===i?' sel':''}" data-i="${i}" transform="translate(${px(p).toFixed(1)},${py(p).toFixed(1)})">
         <title>${esc(p.name)}</title>
         <circle class="hitbox" r="6" fill="#${c}" fill-opacity=".9"/>
         <circle class="ring" r="6" fill="none" stroke="var(--surface)" stroke-width="1.5"/>
       </g>`);
  }
  $('#map').innerHTML = parts.join('');
}

function drawList(){
  const q = $('#q').value.trim().toLowerCase();
  let html = '', shown = 0;
  for (const f of D.folders){
    if (hidden.has(f.name)) continue;
    const items = D.pins.map((p, i) => ({p, i}))
      .filter(({p}) => p.folder === f.name)
      .filter(({p}) => !q || (p.name + ' ' + p.description).toLowerCase().includes(q));
    if (!items.length) continue;
    shown += items.length;
    html += `<section class="grp"><h2><span class="dot" style="background:#${f.colour}"></span>
      ${esc(f.name)}<span class="n">${items.length}</span></h2>`;
    for (const {p, i} of items){
      const mc = (p.description.match(/Map code: ([\d\s*]+)/) || [,''])[1].trim();
      html += `<details class="pin" id="pin-${i}" data-i="${i}">
        <summary><img src="${D.icons[p.icon]}" alt=""><span class="nm">${esc(p.name)}</span>
        <span class="mc">${esc(mc)}</span></summary>
        <div class="body">${bodyHtml(p.description)}</div></details>`;
    }
    html += `</section>`;
  }
  $('#list').innerHTML = html || `<p class="empty">Nothing matches “${esc(q)}”.</p>`;
}

function select(i, scroll){
  selected = i;
  drawMap();
  document.querySelectorAll('.pin.hit').forEach(e => e.classList.remove('hit'));
  const el = document.getElementById('pin-' + i);
  if (!el) return;
  el.open = true;
  el.classList.add('hit');
  if (scroll) el.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'auto' : 'smooth', block: 'center'});
}

$('#map').addEventListener('click', e => {
  const g = e.target.closest('.pindot');
  if (g) select(+g.dataset.i, true);
});
$('#list').addEventListener('click', e => {
  const d = e.target.closest('.pin');
  if (d) select(+d.dataset.i, false);
});
$('#legend').addEventListener('click', e => {
  const btn = e.target.closest('.leg');
  if (!btn) return;
  const f = btn.dataset.f;
  hidden.has(f) ? hidden.delete(f) : hidden.add(f);
  btn.setAttribute('aria-pressed', String(!hidden.has(f)));
  drawMap(); drawList();
});
$('#q').addEventListener('input', drawList);

$('#foot').textContent =
  'Generated from the same data file as the .kmz, so the two cannot disagree. '
  + 'Pins sit at their real coordinates — no basemap, because a published page '
  + 'cannot fetch map tiles. Every figure is quoted from the operator that '
  + 'charges it; anything unpublished says so rather than being estimated.';

drawMap(); drawList();
</script>
"""

if __name__ == "__main__":
    import sys
    build("--refresh-icons" in sys.argv)
