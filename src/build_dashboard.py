"""Generate dashboard.html (artifact source) and dashboard-standalone.html
from src/itineraries.py, so the sheets and the dashboard can never drift apart.

Run from the project root:  python -m src.build_dashboard

Run:  python3 build/make_dashboard.py
"""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from .itineraries import OPTIONS, GLOSSARY, FOLIAGE, SHIMANAMI_LABELS, SHIMANAMI_VERDICT
from .variants import all_variants
from .refs import resolve, gmap, pin, autolink, TRAILHEADS, walks_for, DWELL, SOURCES, ADMISSIONS, TIDES, day_places, linkify, price_unit, PRICE_BODY, ATTRACTIONS, BOOKINGS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
TITLE = "Shikoku — three routes, Oct 2026"

def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def _days(opt, k):
        days = []
        for d in opt["days"]:
            dt = datetime.date.fromisoformat(d["date"])
            legs=[]
            for l in d["legs"]:
                src = resolve(l[4])
                # [6] source, [7] charged-unit, [8] From pin, [9] To pin
                legs.append(list(l) + [list(src) if src else None,
                                       price_unit(l[4]) if l[5] is not None else "",
                                       pin(l[0]), pin(l[1])])
            def _alt(src, label):
                al = []
                for l in src["legs"]:
                    sc = resolve(l[4])
                    al.append(list(l) + [list(sc) if sc else None,
                                         price_unit(l[4]) if l[5] is not None else "",
                                         pin(l[0]), pin(l[1])])
                probe = dict(d, do=src["do"], travel=src["travel"],
                             watch=src["watch"], legs=src["legs"],
                             flow=src.get("flow", []))
                return dict(label=label,
                            walks=walks_for(probe),
                            flow=[[w, autolink(linkify(_esc(x)))] for w, x in src.get("flow", [])],
                            do=[autolink(linkify(_esc(x))) for x in src["do"]],
                            travel=autolink(linkify(_esc(src["travel"]))),
                            watch=[autolink(linkify(_esc(x))) for x in src["watch"]],
                            legs=al,
                            maps=[[n, u] for n, u in day_places(probe, k)])

            # alternative 0 is always the day as written; extras follow
            alts = [_alt(d, d.get("alt_label", "As planned"))]
            for a in d.get("alts", []):
                alts.append(_alt(a, a["label"]))

            days.append(dict(
                d=d["date"], dow=dt.strftime("%a"), dnum=dt.day,
                mon=dt.strftime("%b"), t=d["title"],
                sleep=linkify(_esc(d["sleep"])),
                book=[autolink(linkify(_esc(x))) for x in d.get("book", [])],
                alts=alts,
                flow=alts[0]["flow"], do=alts[0]["do"], travel=alts[0]["travel"],
                watch=alts[0]["watch"], legs=alts[0]["legs"], maps=alts[0]["maps"],
            ))
        return days

def payload():
    out = {}
    for k, opt in OPTIONS.items():
        out[k] = dict(name=opt["name"], verdict=opt["verdict"],
                      sk={v: _days(o, k) for v, o in all_variants(opt).items()})
    return out

CSS = """
:root{
  --paper:#F6F7F9; --card:#FFFFFF; --sunk:#EFF1F4;
  --ink:#14171D; --ink-2:#454C58; --ink-3:#737C8B;
  --rail:#E1E5EA; --rail-2:#CDD3DB;
  --accent:#C0392B; --warn-bg:#8A64101A; --warn:#8A6410;
  --ok:#26624A; --ok-bg:#26624A14;
  --r:10px;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0E1116; --card:#171B22; --sunk:#12161C;
  --ink:#E7EBF1; --ink-2:#A8B1BF; --ink-3:#79838f;
  --rail:#ffffff17; --rail-2:#ffffff2b;
  --accent:#E8705E; --warn:#D9A93F; --warn-bg:#D9A93F1F;
  --ok:#67B893; --ok-bg:#67B8931A;
}}
:root[data-theme="dark"]{
  --paper:#0E1116; --card:#171B22; --sunk:#12161C;
  --ink:#E7EBF1; --ink-2:#A8B1BF; --ink-3:#79838f;
  --rail:#ffffff17; --rail-2:#ffffff2b;
  --accent:#E8705E; --warn:#D9A93F; --warn-bg:#D9A93F1F;
  --ok:#67B893; --ok-bg:#67B8931A;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px 96px}
.mast{padding:52px 0 26px;border-bottom:1px solid var(--rail)}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 14px}
h1{font-size:clamp(30px,6.2vw,50px);line-height:1.03;letter-spacing:-.025em;font-weight:800;
  margin:0 0 14px;text-wrap:balance}
h1 em{font-style:normal;color:var(--accent)}
.dek{max-width:64ch;color:var(--ink-2);margin:0;font-size:16px;text-wrap:pretty}
.bar{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--rail);
  padding:12px 0;margin-bottom:26px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.seg{position:relative;display:flex;background:var(--sunk);border:1px solid var(--rail);
  border-radius:var(--r);padding:3px;gap:2px}
.seg button{position:relative;z-index:1;appearance:none;border:0;background:none;cursor:pointer;
  font-family:var(--sans);font-size:13.5px;font-weight:650;color:var(--ink-2);padding:7px 15px;
  border-radius:7px;white-space:nowrap;outline:none;-webkit-tap-highlight-color:transparent;
  transition:color .15s cubic-bezier(.4,0,.2,1),font-weight .15s}
/* The sliding pill IS the selection indicator. Suppress the browser's own focus
   ring, which is a rounded outline easily mistaken for a second selection, and
   replace it with a keyboard-only ring in the accent colour so the two can
   never be confused. */
.seg button[aria-selected="true"]{color:var(--ink);font-weight:750}
.seg button:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.pill{position:absolute;top:3px;bottom:3px;left:3px;border-radius:7px;background:var(--card);
  border:1px solid var(--rail-2);
  transition:transform .34s cubic-bezier(.16,1,.3,1),width .34s cubic-bezier(.16,1,.3,1)}
.fx{display:flex;align-items:center;gap:7px;margin-left:auto;font-family:var(--mono);
  font-size:12px;color:var(--ink-3)}
.fx input{width:84px;font-family:var(--mono);font-size:12px;padding:6px 8px;
  border:1px solid var(--rail-2);border-radius:7px;background:var(--card);color:var(--ink);
  text-align:right}
.fx input:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.seg.sk button,.seg.pax button{font-size:12.5px;padding:6px 12px}
.unit{font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.unit.bag{color:var(--warn);font-weight:700}
.pricenote{border:1px solid var(--rail);border-left:3px solid var(--warn);background:var(--card);
  border-radius:var(--r);padding:11px 14px;margin:0 0 22px;font-size:13px;color:var(--ink-2);
  text-wrap:pretty}
.skverdict{border:1px solid var(--rail);border-left:3px solid var(--ok);background:var(--card);
  border-radius:var(--r);padding:12px 15px;margin:0 0 14px;font-size:13.5px;color:var(--ink-2);
  text-wrap:pretty}
.skverdict b{color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--rail);
  border:1px solid var(--rail);border-radius:var(--r);overflow:hidden;margin-bottom:14px}
.stat{background:var(--card);padding:15px 16px}
.stat dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 5px}
.stat dd{margin:0;font-family:var(--mono);font-size:20px;font-weight:600;letter-spacing:-.02em;
  font-variant-numeric:tabular-nums}
.stat dd small{font-size:12px;font-weight:400;color:var(--ink-3)}
.verdict{border:1px solid var(--rail);border-left:3px solid var(--accent);background:var(--card);
  border-radius:var(--r);padding:14px 16px;margin-bottom:30px;font-size:14.5px;color:var(--ink-2);
  text-wrap:pretty}
.day{display:grid;grid-template-columns:92px 1fr;border:1px solid var(--rail);
  border-radius:var(--r);background:var(--card);margin-bottom:10px;overflow:hidden}
.railcol{background:var(--sunk);border-right:1px solid var(--rail);padding:15px 12px;position:relative}
.railcol::before{content:"";position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--rail)}
.node{position:relative;z-index:1;width:9px;height:9px;background:var(--accent);margin:0 auto 9px;
  border-radius:2px}
.dow{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);text-align:center}
.dnum{font-family:var(--mono);font-size:19px;font-weight:650;text-align:center;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.dmon{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);text-align:center;
  text-transform:uppercase;letter-spacing:.1em}
.body{padding:16px 18px 16px;min-width:0}
.dtitle{font-size:17.5px;font-weight:700;letter-spacing:-.015em;margin:0 0 4px;text-wrap:balance}
.sleep{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin:0 0 15px}
.sleep b{color:var(--ink-2);font-weight:600}
.sec{margin:0 0 14px}
.lbl{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 6px;display:flex;align-items:center;gap:7px}
.lbl::after{content:"";flex:1;height:1px;background:var(--rail)}
.sec ul{margin:0;padding-left:17px}
.sec li{margin-bottom:5px;color:var(--ink-2);text-wrap:pretty}
.sec li::marker{color:var(--accent)}
.sec p{margin:0;color:var(--ink-2);text-wrap:pretty}
.warnbox{background:var(--warn-bg);border-radius:8px;padding:10px 12px 10px 0}
.warnbox ul{padding-left:28px}
.warnbox li{color:var(--ink-2);font-size:14px}
.warnbox li::marker{color:var(--warn)}
details{border-top:1px solid var(--rail);margin-top:2px}
summary{cursor:pointer;list-style:none;padding:11px 0 0;font-family:var(--mono);font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);display:flex;align-items:center;gap:7px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:14px;color:var(--ink-3);margin-left:auto}
details[open] summary::after{content:"\\2212"}
summary:hover{color:var(--ink-2)}
summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.tw{overflow-x:auto;margin-top:10px;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:560px;font-family:var(--mono);font-size:12px}
th{text-align:left;font-weight:600;color:var(--ink-3);font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;padding:0 10px 7px 0;border-bottom:1px solid var(--rail);white-space:nowrap}
td{padding:7px 10px 7px 0;border-bottom:1px solid var(--rail);vertical-align:top;color:var(--ink-2)}
tr:last-child td{border-bottom:0}
td.t{white-space:nowrap;color:var(--ink);font-variant-numeric:tabular-nums}
td.y,th.y{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;
  padding-right:14px}
th.src{padding-left:6px}
td.y{color:var(--ink);font-weight:600}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--ink-3);
  padding-right:22px;border-right:1px solid var(--rail)}
.route{color:var(--ink);font-weight:600}
.panel{margin-top:38px;border-top:1px solid var(--rail);padding-top:26px}
.panel h2{font-size:13px;font-family:var(--mono);letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);font-weight:600;margin:0 0 6px}
.panel .sub{color:var(--ink-3);font-size:13.5px;margin:0 0 16px}
.gl{display:grid;grid-template-columns:repeat(auto-fill,minmax(292px,1fr));gap:10px}
.gterm{border:1px solid var(--rail);border-radius:var(--r);background:var(--card);padding:13px 15px}
.gterm h3{margin:0 0 2px;font-size:14.5px;font-weight:700}
.gterm .jp{font-size:12px;color:var(--ink-3);margin:0 0 7px;font-family:var(--mono)}
.gterm p{margin:0 0 7px;font-size:13.5px;color:var(--ink-2);text-wrap:pretty}
.gterm .why{color:var(--accent);font-size:13px;margin:0}
.fol{overflow-x:auto}
.fol table{min-width:640px;font-size:12px}
.fol td.spot{color:var(--ink);font-weight:600;font-family:var(--sans);font-size:13px}
.fol .v-ok{color:var(--ok);font-weight:700}
.fol .v-no{color:var(--accent);font-weight:700}
.fol tr.hit{background:var(--ok-bg)}
.ml{color:inherit;text-decoration:none;border-bottom:1px solid var(--rail-2);
  transition:border-color .15s,color .15s}
.ml:hover{color:var(--accent);border-bottom-color:var(--accent)}
.ml:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
.ml::after{content:"\2197";font-size:.72em;vertical-align:super;margin-left:1px;
  color:var(--ink-3)}
.pins{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 13px}
.pin{font-size:12px;text-decoration:none;color:var(--ink-2);border:1px solid var(--rail);
  border-radius:999px;padding:4px 11px 4px 9px;background:var(--sunk);
  transition:border-color .15s,color .15s}
.pin:hover{color:var(--ink);border-color:var(--rail-2)}
.pin::before{content:"📍";margin-right:5px;font-size:11px}
.pin:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
td.src{padding-left:16px}
td.src a{color:var(--ink-3);text-decoration:none;border-bottom:1px dotted var(--rail-2)}
td.src a:hover{color:var(--accent)}
.tier{font-size:9px;letter-spacing:.08em;text-transform:uppercase;padding:1px 5px;
  border-radius:4px;margin-left:6px;white-space:nowrap}
.t-operator,.t-official{color:var(--ok);background:var(--ok-bg)}
.t-third-party,.t-traveller{color:var(--warn);background:var(--warn-bg)}
/* Deliberately NOT `scroll-behavior:smooth` — its duration is set by the
   browser and on a page this long it either whips or crawls. The JS below
   scales the duration to the distance and clamps it. */
#totop{position:fixed;right:18px;bottom:18px;z-index:50;width:44px;height:44px;
  border-radius:50%;border:1px solid var(--rail-2);background:var(--card);color:var(--ink-2);
  font-size:17px;line-height:1;cursor:pointer;display:flex;align-items:center;
  justify-content:center;opacity:0;pointer-events:none;transform:translateY(8px);
  box-shadow:inset 0 1px 0 0 rgb(255 255 255 / .5);
  transition:opacity .22s cubic-bezier(.4,0,.2,1),transform .22s cubic-bezier(.4,0,.2,1),
             color .15s,border-color .15s}
#totop.on{opacity:1;pointer-events:auto;transform:translateY(0)}
#totop:hover{color:var(--accent);border-color:var(--accent)}
#totop:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){#totop{transition:none}}
.jump{display:flex;flex-wrap:wrap;align-items:center;gap:7px;margin:0 0 18px;
  padding:11px 13px;border:1px solid var(--rail);border-radius:var(--r);background:var(--sunk)}
.jump span{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-right:2px}
.jump a{font-family:var(--mono);font-size:11.5px;text-decoration:none;color:var(--ink-2);
  border:1px solid var(--rail-2);border-radius:999px;padding:4px 11px;background:var(--card);
  transition:color .15s cubic-bezier(.4,0,.2,1),border-color .15s cubic-bezier(.4,0,.2,1)}
.jump a:hover{color:var(--accent);border-color:var(--accent)}
.jump a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.panel{scroll-margin-top:14px}
.walklink{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:11px;
  text-decoration:none;color:var(--accent);border:1px solid var(--accent);border-radius:6px;
  padding:3px 9px;margin:0 0 12px}
.walklink:hover{background:#C0392B12}
.walklink:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.filt{margin:0 0 14px}
.filt input{width:100%;max-width:420px;font-family:var(--sans);font-size:14px;padding:9px 12px;
  border:1px solid var(--rail-2);border-radius:8px;background:var(--card);color:var(--ink)}
.filt input:focus-visible{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{font-family:var(--mono);font-size:11px;padding:4px 10px;border-radius:999px;cursor:pointer;
  border:1px solid var(--rail-2);background:var(--card);color:var(--ink-2);
  transition:background .15s cubic-bezier(.4,0,.2,1),color .15s cubic-bezier(.4,0,.2,1)}
.chip:hover{color:var(--ink)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.acount{margin:9px 0 0;font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
.flow{margin:0 0 16px;padding:0;list-style:none;counter-reset:fl}
.flow li{position:relative;padding:0 0 11px 30px;counter-increment:fl}
.flow li:before{content:counter(fl);position:absolute;left:0;top:1px;width:20px;height:20px;
  border-radius:50%;background:var(--accent);color:#fff;font-family:var(--mono);font-size:10.5px;
  font-weight:700;display:flex;align-items:center;justify-content:center}
.flow li:after{content:"";position:absolute;left:9.5px;top:23px;bottom:1px;width:1px;
  background:var(--rail-2)}
.flow li:last-child:after{display:none}
.flow .w{font-family:var(--mono);font-size:11px;color:var(--accent);font-weight:700;
  margin-right:7px}
.flow .x{font-size:14px;line-height:1.6;color:var(--ink)}
.bookban{border:1px solid var(--accent);border-left:4px solid var(--accent);
  background:#C0392B0E;border-radius:var(--r);padding:11px 14px;margin:0 0 14px}
.bookban p.h{margin:0 0 5px;font-family:var(--mono);font-size:10.5px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.bookban ul{margin:0;padding-left:17px}
.bookban li{font-size:13.5px;line-height:1.55;color:var(--ink);margin:3px 0}
.altsw{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 14px;padding:4px;border-radius:8px;
  background:var(--sunk);border:1px solid var(--rail)}
.altb{font-family:var(--mono);font-size:11px;letter-spacing:.02em;border:0;cursor:pointer;
  padding:5px 10px;border-radius:6px;background:transparent;color:var(--ink-3);
  transition:background .15s cubic-bezier(.4,0,.2,1),color .15s cubic-bezier(.4,0,.2,1)}
.altb:hover{color:var(--ink)}
.altb.on{background:var(--card);color:var(--ink);font-weight:700;
  box-shadow:inset 0 1px 0 0 rgb(255 255 255 / .5);border:1px solid var(--rail-2);padding:4px 9px}
.altb:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.walk{border:1px solid var(--rail);border-radius:var(--r);padding:13px 15px;margin-bottom:10px;
  scroll-margin-top:14px;
  background:var(--card)}
.walk h3{margin:0 0 2px;font-size:15px;font-weight:700}
.walk .where{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 9px}
.walk .facts{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 9px}
.walk .facts span{font-family:var(--mono);font-size:11px;background:var(--sunk);
  border:1px solid var(--rail);border-radius:5px;padding:2px 7px;color:var(--ink-2)}
.vd{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.06em;
  border-radius:5px;padding:2px 8px;text-transform:uppercase}
.vd-easy{background:var(--ok-bg);color:var(--ok)}
.vd-mod{background:var(--warn-bg);color:var(--warn)}
.vd-hard{background:#C0392B18;color:var(--accent)}
.walk .apps{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px}
.walk .apps a,.walk .apps span{font-family:var(--mono);font-size:11px;border-radius:5px;
  padding:3px 9px;border:1px solid var(--rail);text-decoration:none}
.walk .apps a{color:var(--accent);border-color:var(--accent)}
.walk .apps span{color:var(--ink-3)}
.walk .note{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.55}
.tide{border:1px solid var(--rail);border-left:3px solid var(--accent);border-radius:var(--r);
  background:var(--card);padding:14px 16px;margin-bottom:10px}
.tide h3{margin:0 0 3px;font-size:15.5px;font-weight:700}
.tide .when{font-family:var(--mono);font-size:11.5px;color:var(--accent);margin:0 0 8px}
.tide p.rule{margin:0 0 10px;font-size:14px;color:var(--ink-2);text-wrap:pretty}
.tide a.tt{display:inline-block;font-size:13px;text-decoration:none;color:var(--ink);
  border:1px solid var(--rail-2);border-radius:8px;padding:6px 12px;margin:0 6px 6px 0;
  background:var(--sunk);transition:border-color .15s}
.tide a.tt:hover{border-color:var(--accent);color:var(--accent)}
.dw{width:100%;border-collapse:collapse;font-size:13.5px;min-width:520px}
.dw th{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3);text-align:left;padding:0 12px 8px 0;border-bottom:1px solid var(--rail)}
.dw td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rail);vertical-align:top;
  color:var(--ink-2)}
.dw td.pl{color:var(--ink);font-weight:650;white-space:nowrap}
.dw td.hrs{font-family:var(--mono);color:var(--accent);font-weight:600;white-space:nowrap}
.rv{opacity:0;transform:translateY(14px);filter:blur(4px)}
.rv.in{opacity:1;transform:none;filter:none;
  transition:opacity .5s cubic-bezier(.16,1,.3,1),transform .5s cubic-bezier(.16,1,.3,1),
             filter .5s cubic-bezier(.16,1,.3,1)}
@media (prefers-reduced-motion:reduce){.rv,.rv.in{opacity:1;transform:none;filter:none;
  transition:none}.pill{transition:none}}
@media (max-width:640px){
  .wrap{padding:0 14px 72px}
  .mast{padding:34px 0 22px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .day{grid-template-columns:1fr}
  .railcol{border-right:0;border-bottom:1px solid var(--rail);display:flex;align-items:center;
    gap:9px;padding:9px 15px}
  .railcol::before{display:none}
  .node{margin:0}
  .dnum{font-size:15px}
  .dow,.dmon{font-size:10px}
  .body{padding:14px 15px 15px}
  .fx{margin-left:0;width:100%}
  .gl{grid-template-columns:1fr}
}
"""

JS = """
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
let cur="A", sk="nobike", pax=1;
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
/* label + optional map pin. No url -> plain text, because "up and back" and
   "Big bags" are not places and must not link to something plausible. */
const mp=(t,u)=>u?`<a class="ml" href="${u}" target="_blank" rel="noopener">${esc(t)}</a>`:esc(t);
const rate=()=>parseFloat($("#fx").value)||0;
const yen=n=>"\\u00a5"+Math.round(n*pax).toLocaleString("en-US");
const nis=n=>"\\u20aa"+(n*rate()*pax).toFixed(2);
const dayss=()=>D[cur].sk[sk];
const total=k=>D[k].sk[sk].reduce((s,d)=>s+curAlt(d).legs.reduce((a,l)=>a+(typeof l[5]==="number"?l[5]:0),0),0);

function stats(k){
  const t=total(k), legs=D[k].sk[sk].reduce((a,d)=>a+curAlt(d).legs.length,0);
  const rows=[["Nights",D[k].sk[sk].length-1,""],
              ["Transport, "+(pax===1?"1 person":"2 people"),yen(t),nis(t)],
              ["Legs planned",legs,""],["Longest day",k==="A"?"5h52":"5h00","all-local"]];
  $("#stats").innerHTML=rows.map(([a,b,c])=>
    `<div class="stat"><dt>${a}</dt><dd>${b}${c?` <small>${c}</small>`:""}</dd></div>`).join("");
}

/* A day can be spent more than one way. Alternative 0 is the day as planned;
   picking another swaps the WHOLE card — highlights, getting there, warnings and
   the transport table with it. Choice is remembered per day, per option. */
let altSel={};
const altKey=d=>cur+"|"+sk+"|"+d.d;
const curAlt=d=>d.alts[altSel[altKey(d)]||0];

function dayBody(d){
  const a=curAlt(d);
  const sw=d.alts.length>1?`<div class="altsw" data-day="${d.d}">${d.alts.map((x,j)=>
    `<button class="altb${(altSel[altKey(d)]||0)===j?" on":""}" data-alt="${j}">${esc(x.label)}</button>`
    ).join("")}</div>`:"";
  /* A day with a declared flow is one where the ORDER is forced — by a tide, a
     bus that runs four times, closing time or the light. Days without one are
     genuinely pick-your-own and stay as a list. */
  const doList=a.flow&&a.flow.length
    ?`<div class="sec"><p class="lbl">The order that works, and why</p><ol class="flow">${
       a.flow.map(([w,x])=>`<li><span class="w">${esc(w)}</span><span class="x">${x}</span></li>`
       ).join("")}</ol></div>`
    :`<div class="sec"><p class="lbl">What you'll actually do &mdash; any order you like</p><ul>${
       a.do.map(x=>`<li>${x}</li>`).join("")}</ul></div>`;
  const trav=`<div class="sec"><p class="lbl">Getting there</p><p>${a.travel}</p></div>`;
  const warn=a.watch.length?`<div class="sec"><p class="lbl">Watch out for</p>
    <div class="warnbox"><ul>${a.watch.map(x=>`<li>${x}</li>`).join("")}</ul></div></div>`:"";
  const tbl=a.legs.length?`<details><summary>Transport detail · ${a.legs.length} leg${
    a.legs.length>1?"s":""}, times &amp; fares</summary>
    <div class="tw"><table><thead><tr><th>From</th><th>To</th><th>Dep</th><th>Arr</th>
    <th>How</th><th class="y">¥</th><th class="y">₪</th><th>Charged</th>
    <th class="src">Price source</th></tr></thead><tbody>
    ${a.legs.map(l=>`<tr><td class="route">${mp(l[0],l[8])}</td><td class="route">${mp(l[1],l[9])}</td>
      <td class="t">${esc(l[2])}</td><td class="t">${esc(l[3])}</td><td>${esc(l[4])}</td>
      <td class="y">${typeof l[5]==="number"?yen(l[5]):"n/s"}</td>
      <td class="n">${typeof l[5]==="number"?nis(l[5]):"—"}</td>
      <td><span class="unit${l[7]==="per bag"?" bag":""}">${esc(l[7]||"")}</span></td>
      <td class="src">${l[6]?`<a href="${l[6][1]}" target="_blank" rel="noopener">${esc(l[6][0])}</a>`
        +`<span class="tier t-${l[6][2].replace(/ /g,"-")}">${l[6][2]}</span>`
        :`<span style="color:var(--ink-3)">no published figure</span>`}</td></tr>`).join("")}
    </tbody></table></div></details>`:"";
  const wl=(a.walks&&a.walks.length)?`<div>${a.walks.map(i=>
    `<a class="walklink" href="#w-${i}">\U0001f97e ${esc(TH[i][0])} \u2014 trailhead, ${esc(TH[i][5])}</a>`
    ).join(" ")}</div>`:"";
  const bb=(d.book&&d.book.length)?`<div class="bookban"><p class="h">Book this before the day</p>
    <ul>${d.book.map(x=>`<li>${x}</li>`).join("")}</ul></div>`:"";
  return `<h3 class="dtitle">${esc(d.t)}</h3>
    <p class="sleep">Sleep in · <b>${d.sleep}</b></p>${bb}${sw}
    ${a.maps.length?`<div class="pins">${a.maps.map(m=>
      `<a class="pin" href="${m[1]}" target="_blank" rel="noopener">${esc(m[0])}</a>`).join("")}</div>`:""}
    ${doList}${trav}${wl}${warn}${tbl}`;
}

function dayCard(d,i){
  return `<article class="day rv" data-day="${d.d}" style="transition-delay:${Math.min(i,10)*45}ms">
    <div class="railcol"><div class="node"></div><div class="dow">${d.dow}</div>
      <div class="dnum">${d.dnum}</div><div class="dmon">${d.mon}</div></div>
    <div class="body">${dayBody(d)}</div></article>`;
}

/* Swap one card in place rather than re-rendering the list, so the page does
   not jump under the reader's thumb. */
document.addEventListener("click",e=>{
  const b=e.target.closest(".altb"); if(!b) return;
  const dd=b.closest(".altsw").dataset.day;
  const d=D[cur].sk[sk].find(x=>x.d===dd); if(!d) return;
  altSel[cur+"|"+sk+"|"+dd]=+b.dataset.alt;
  const art=document.querySelector(`.day[data-day="${dd}"]`);
  art.querySelector(".body").innerHTML=dayBody(d);
  stats(cur);
});

function render(k){
  cur=k;
  $("#verdict").innerHTML="<b>"+esc(D[k].name)+"</b> \\u2014 "+esc(D[k].verdict);
  const hasSK=D[k].sk[sk].some(d=>/Shimanami/.test(d.t));
  $("#sk").style.display=hasSK?"":"none";
  $("#skverdict").style.display=hasSK?"":"none";
  $("#pricenote").innerHTML="<b>All prices are per person.</b> "+esc(PN);
  $("#skverdict").innerHTML="<b>"+esc(SKL[sk])+".</b> "+esc(SKV[sk]);
  $("#days").innerHTML=D[k].sk[sk].map((d,i)=>dayCard(d,i)).join("");
  stats(k);
  requestAnimationFrame(()=>document.querySelectorAll(".rv").forEach(e=>e.classList.add("in")));
}

/* ---- animated in-page navigation -------------------------------------- */
const REDUCE=matchMedia("(prefers-reduced-motion: reduce)");
const easeInOutCubic=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;

/* Scroll the WHOLE distance from wherever the reader is. An earlier version cut
   most of the way instantly and animated only the last stretch — which read as a
   teleport followed by a scroll, and was worse than either. The duration grows
   with the SQUARE ROOT of the distance, so a short hop is quick and a full-page
   trip takes noticeably longer without ever becoming a wait. */
function glide(toY,done){
  toY=Math.max(0,Math.round(toY));
  const start=window.scrollY, dist=toY-start;
  if(REDUCE.matches||Math.abs(dist)<2){window.scrollTo(0,toY);done&&done();return;}
  const dur=Math.min(2200,Math.max(420,14*Math.sqrt(Math.abs(dist))));
  const t0=performance.now();
  let cancelled=false;
  /* If the reader grabs the page mid-flight, stop fighting them. */
  const stop=()=>{cancelled=true;};
  const OPTS={passive:true,once:true};
  addEventListener("wheel",stop,OPTS);
  addEventListener("touchstart",stop,OPTS);
  addEventListener("keydown",stop,OPTS);
  (function step(now){
    if(cancelled) return;
    const t=Math.min(1,(now-t0)/dur);
    window.scrollTo(0,start+dist*easeInOutCubic(t));
    if(t<1){requestAnimationFrame(step);}
    else{removeEventListener("wheel",stop);removeEventListener("touchstart",stop);
         removeEventListener("keydown",stop);done&&done();}
  })(t0);
}

document.addEventListener("click",e=>{
  const a=e.target.closest('a[href^="#"]'); if(!a) return;
  const id=a.getAttribute("href").slice(1), t=id&&document.getElementById(id);
  if(!t) return;
  e.preventDefault();
  glide(t.getBoundingClientRect().top+window.scrollY-14,()=>{
    history.replaceState(null,"","#"+id);
    /* move keyboard focus too, or the next Tab starts from the old place */
    t.setAttribute("tabindex","-1"); t.focus({preventScroll:true});
  });
});

const toTop=$("#totop");
toTop.addEventListener("click",()=>glide(0,()=>{
  history.replaceState(null,"",location.pathname+location.search);
  document.querySelector("h1").setAttribute("tabindex","-1");
  document.querySelector("h1").focus({preventScroll:true});
}));
let ticking=false;
addEventListener("scroll",()=>{
  if(ticking) return; ticking=true;
  requestAnimationFrame(()=>{toTop.classList.toggle("on",window.scrollY>600);ticking=false;});
},{passive:true});

$("#gloss").innerHTML=G.map(([t,jp,what,why])=>
  `<div class="gterm"><h3>${esc(t)}</h3><p class="jp">${esc(jp)}</p>
   <p>${esc(what)}</p><p class="why">${esc(why)}</p></div>`).join("");

$("#book").innerHTML=BK.map(([what,how,when,key])=>
  `<div class="tide"><h3>${esc(what)}</h3><p class="when">${esc(how)}</p>
   <p class="rule">${esc(when)}</p>
   <a class="tt" href="${S[key][1]}" target="_blank" rel="noopener">${esc(S[key][0])} \u2197</a></div>`).join("");

/* The table is 50 rows. Finding "is Ritsurin open on a Monday" by scrolling is
   the wrong job for a phone, so it filters: free text over every column, plus
   one-tap chips for the region and the two things people actually hunt for. */
let aq="", achip="";
const AREAS=[...new Set(AT.map(r=>r[1]))].sort();
$("#achips").innerHTML=[["","Everything"],["$free","Free"],["$book","Must be booked"]]
  .concat(AREAS.map(a=>[a,a])).map(([v,l])=>
   `<button class="chip${v===""?" on":""}" data-v="${esc(v)}">${esc(l)}</button>`).join("");

function drawAttr(){
  const q=aq.trim().toLowerCase();
  const rows=AT.filter(r=>{
    if(achip==="$free"&&!/^FREE/i.test(r[2])) return false;
    if(achip==="$book"&&!/^YES/i.test(r[5])) return false;
    if(achip&&!achip.startsWith("$")&&r[1]!==achip) return false;
    return !q||r.slice(0,6).join(" ").toLowerCase().includes(q);
  });
  $("#attr").innerHTML=rows.map(([n,w,p,h,c,b,k,u])=>{
    const free=/^FREE/i.test(p), must=/^YES/i.test(b);
    return `<tr><td class="pl">${mp(n,u)}</td><td>${mp(w,null)}</td>
      <td class="hrs" style="${free?"color:var(--ok)":""}">${esc(p)}</td>
      <td>${esc(h)}</td><td>${esc(c)}</td>
      <td style="${must?"color:var(--accent);font-weight:700":"color:var(--ink-3)"}">${esc(b)}</td></tr>`;
  }).join("")||`<tr><td colspan="6" style="padding:18px;color:var(--ink-3)">Nothing matches that.</td></tr>`;
  $("#acount").textContent=rows.length===AT.length
    ?`All ${AT.length} places.`:`${rows.length} of ${AT.length} places.`;
}
$("#afind").addEventListener("input",e=>{aq=e.target.value;drawAttr();});
$("#achips").addEventListener("click",e=>{
  const b=e.target.closest(".chip"); if(!b) return;
  achip=(achip===b.dataset.v)?"":b.dataset.v;
  document.querySelectorAll("#achips .chip").forEach(c=>
    c.classList.toggle("on", c.dataset.v===achip || (achip===""&&c.dataset.v==="")));
  drawAttr();
});
drawAttr();

$("#walks").innerHTML=TH.map(([n,where,ll,yamap,at,dist,time,verdict,note,key,tu])=>{
  const cls=/EASY/i.test(verdict)?"vd-easy":/SKIP|STEEP|HARD/i.test(verdict)?"vd-hard":"vd-mod";
  return `<div class="walk" id="w-${TH.findIndex(x=>x[0]===n)}"><h3>${esc(n)}</h3><p class="where">${esc(where)}</p>
    <div class="facts"><span>${esc(dist)}</span><span>${esc(time)}</span>
      <span class="vd ${cls}">${esc(verdict)}</span></div>
    <div class="apps">
      <a href="${tu}" target="_blank" rel="noopener">📍 Trailhead ${esc(ll)}</a>
      ${at?`<a href="${at}" target="_blank" rel="noopener">AllTrails \u2197</a>`
          :`<span>AllTrails \u2014 no matching route</span>`}
      ${yamap?`<a href="${yamap}" target="_blank" rel="noopener">YAMAP \u2197</a>`
          :`<span>YAMAP \u2014 none</span>`}
      <a href="${S[key][1]}" target="_blank" rel="noopener">${esc(S[key][0])} \u2197</a>
    </div><p class="note">${esc(note)}</p></div>`;
}).join("");

$("#tides").innerHTML=T.map(([what,when,rule,key,extra])=>{
  const links=[key].concat(extra).map(k=>
    `<a class="tt" href="${S[k][1]}" target="_blank" rel="noopener">${esc(S[k][0])} \u2197</a>`).join("");
  return `<div class="tide"><h3>${esc(what)}</h3><p class="when">${esc(when)}</p>
    <p class="rule">${esc(rule)}</p>${links}</div>`;}).join("");

$("#dwbody").innerHTML=W.map(([pl,hrs,key,basis])=>{
  const s=S[key];
  return `<tr><td class="pl">${esc(pl)}</td><td class="hrs">${esc(hrs)}</td>
    <td>${esc(basis)}${s?` <a href="${s[1]}" target="_blank" rel="noopener"
    style="color:var(--ink-3)">\u2014 source \u2197</a>`:""}</td></tr>`;}).join("");

$("#folbody").innerHTML=F.map(r=>{
  const hit=r[5].startsWith("ON TIME")||r[5].startsWith("MARGINAL");
  return `<tr class="${hit?"hit":""}"><td class="spot">${esc(r[0])}</td>
    <td class="t">${esc(r[1])}</td><td class="t">${esc(r[2])}</td><td class="t">${esc(r[3])}</td>
    <td class="t">${esc(r[4])}</td><td class="${hit?"v-ok":"v-no"}">${esc(r[5])}</td>
    <td>${esc(r[6])}</td></tr>`;}).join("");

function movePill(){
  for(const [wrap,pill,sel] of [["#seg","#pill",`[data-k="${cur}"]`],
                                ["#sk","#skpill",`[data-v="${sk}"]`],
                                ["#pax","#paxpill",`[data-p="${pax}"]`]]){
    const b=$(wrap+" button"+sel), w=$(wrap), p=$(pill);
    if(!b||!w||!p) continue;
    const br=b.getBoundingClientRect(), wr=w.getBoundingClientRect();
    if(!br.width) continue;                    // not laid out yet
    p.style.width=br.width+"px";
    p.style.transform=`translateX(${br.left-wr.left-3}px)`;
  }
}
document.querySelectorAll("#seg button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#seg button").forEach(x=>x.setAttribute("aria-selected",String(x===b)));
  render(b.dataset.k); movePill();
}));
document.querySelectorAll("#sk button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#sk button").forEach(x=>x.setAttribute("aria-selected",String(x===b)));
  sk=b.dataset.v; render(cur); movePill();
}));
document.querySelectorAll("#pax button").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll("#pax button").forEach(x=>x.setAttribute("aria-selected",String(x===b)));
  pax=+b.dataset.p; render(cur); movePill();
}));
$("#fx").addEventListener("input",()=>{render(cur);movePill();});
window.addEventListener("resize",movePill);
render("A"); movePill();
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(movePill);}
window.addEventListener("load",movePill);
"""

BODY = """
<div class="wrap">
  <header class="mast">
    <p class="eyebrow">Car-free &middot; local trains &middot; from 9 Oct 2026</p>
    <h1>Shikoku, three ways.<br><em>Two weeks the long way, or one week sitting still.</em></h1>
    <p class="dek">Every time and fare here comes from a published operator timetable or a
    named traveller who actually made the trip. Nothing is estimated &mdash; where an operator
    publishes no figure, it says so. Unfamiliar words are explained in the glossary at the
    bottom.</p>
  </header>

  <button id="totop" aria-label="Back to the top" title="Back to the top">&#8593;</button>

  <nav class="jump" aria-label="Jump to a reference table">
    <span>Reference:</span>
    <a href="#p-book">Book ahead</a>
    <a href="#p-cost">Costs &amp; hours</a>
    <a href="#p-walks">🥾 Walks &amp; trailheads</a>
    <a href="#p-tides">Tides</a>
    <a href="#p-fol">Foliage</a>
    <a href="#p-dwell">How long</a>
    <a href="#p-gloss">Glossary</a>
  </nav>

  <nav class="bar">
    <div class="seg" id="seg" role="tablist" aria-label="Choose route">
      <div class="pill" id="pill"></div>
      <button role="tab" aria-selected="true" data-k="A">A &middot; Himeji &amp; Shodoshima</button>
      <button role="tab" aria-selected="false" data-k="A2">A2 &middot; A without Kōchi</button>
      <button role="tab" aria-selected="false" data-k="B">B &middot; Awaji &amp; whirlpools</button>
      <button role="tab" aria-selected="false" data-k="C">C &middot; One week, two bases</button>
    </div>
    <div class="seg sk" id="sk" role="tablist" aria-label="Shimanami Kaido length">
      <div class="pill" id="skpill"></div>
      <button role="tab" aria-selected="true" data-v="nobike">Shimanami: no cycling</button>
      <button role="tab" aria-selected="false" data-v="1day">1 day</button>
      <button role="tab" aria-selected="false" data-v="2day">2 days</button>
      <button role="tab" aria-selected="false" data-v="3day">3 days</button>
    </div>
    <div class="seg pax" id="pax" role="tablist" aria-label="How many travellers">
      <div class="pill" id="paxpill"></div>
      <button role="tab" aria-selected="true" data-p="1">1 person</button>
      <button role="tab" aria-selected="false" data-p="2">2 people</button>
    </div>
    <label class="fx">JPY&rarr;&#8362;
      <input id="fx" type="number" step="0.00001" value="0.01858" aria-label="Yen to shekel rate">
      <span>16 Aug 26</span>
    </label>
  </nav>

  <p class="skverdict" id="skverdict"></p>
  <p class="pricenote" id="pricenote"></p>
  <dl class="stats" id="stats"></dl>
  <p class="verdict" id="verdict"></p>
  <main id="days"></main>

  <section class="panel" id="p-book">
    <h2>Book these in advance</h2>
    <p class="sub">Everything else on this trip you can simply turn up to.</p>
    <div id="book"></div>
  </section>

  <section class="panel" id="p-cost">
    <h2>What it costs and when it's open</h2>
    <p class="sub">Adult prices, per person. Where an operator publishes no figure it says
      so rather than being guessed at.</p>
    <div class="filt">
      <input id="afind" type="search" placeholder="Filter &mdash; type a name, a town, an hour&hellip;"
             aria-label="Filter the attractions table">
      <div id="achips" class="chips"></div>
      <p id="acount" class="acount"></p>
    </div>
    <div class="fol"><table class="dw"><thead><tr><th>Attraction</th><th>Where</th>
      <th>Adult</th><th>Hours</th><th>Closed</th><th>Book?</th></tr></thead>
      <tbody id="attr"></tbody></table></div>
  </section>

  <section class="panel" id="p-walks">
    <h2>Every walk, with its trailhead</h2>
    <p class="sub">Where each walk actually STARTS &mdash; the hardest thing to work out on
      the ground &mdash; plus the matching AllTrails and YAMAP route so your phone can track
      you offline. Distance, ascent and time are the app&rsquo;s figures or the operator&rsquo;s,
      never mine. YAMAP has far better coverage of Japanese trails than AllTrails does.</p>
    <div id="walks"></div>
  </section>

  <section class="panel" id="p-tides">
    <h2>Tide tables &mdash; check these before fixing the hour</h2>
    <p class="sub">Three things on this route only work at the right water level. All are
      free to look up, and all three are easy to get wrong.</p>
    <div id="tides"></div>
  </section>

  <section class="panel" id="p-fol">
    <h2>Autumn foliage</h2>
    <p class="sub">2025-season dates from Nihon Kishou's own data. Year-to-year spread is only
      about 7&ndash;8 days, so these are reliable. Highlighted rows are the ones your dates
      actually catch.</p>
    <div class="fol"><table><thead><tr><th>Spot</th><th>Elevation</th><th>Starts</th>
      <th>Peak</th><th>Ends</th><th>Your dates</th><th>What that means</th></tr></thead>
      <tbody id="folbody"></tbody></table></div>
  </section>

  <section class="panel" id="p-dwell">
    <h2>How long people actually spend</h2>
    <p class="sub">Reported by named travellers or published by the operator. Where nobody
      states a figure, it says so rather than guessing.</p>
    <div class="fol"><table class="dw"><thead><tr><th>Place</th><th>Typical time</th>
      <th>Who says so, and on what basis</th></tr></thead><tbody id="dwbody"></tbody></table></div>
  </section>

  <section class="panel" id="p-gloss">
    <h2>Glossary</h2>
    <p class="sub">Every term used above that isn't obvious in English.</p>
    <div class="gl" id="gloss"></div>
  </section>
</div>
"""

def main():
    data = ("<script>\nconst D=" + json.dumps(payload(), ensure_ascii=False)
            + ";\nconst G=" + json.dumps(GLOSSARY, ensure_ascii=False)
            + ";\nconst F=" + json.dumps(FOLIAGE, ensure_ascii=False)+ ";\nconst W=" + json.dumps(DWELL, ensure_ascii=False)+ ";\nconst S=" + json.dumps(SOURCES, ensure_ascii=False)+ ";\nconst TH=" + json.dumps([list(t) + ["https://www.google.com/maps/search/?api=1&query=" + t[2].replace(",", "%2C")] for t in TRAILHEADS], ensure_ascii=False)+ ";\nconst T=" + json.dumps(TIDES, ensure_ascii=False)+ ";\nconst SKL=" + json.dumps(SHIMANAMI_LABELS, ensure_ascii=False)+ ";\nconst SKV=" + json.dumps(SHIMANAMI_VERDICT, ensure_ascii=False)+ ";\nconst PN=" + json.dumps(PRICE_BODY, ensure_ascii=False)+ ";\nconst AT=" + json.dumps([list(a) + [pin(a[0]) or pin(a[1])] for a in ATTRACTIONS], ensure_ascii=False)+ ";\nconst BK=" + json.dumps(BOOKINGS, ensure_ascii=False)
            + ";\n" + JS + "\n</script>\n")
    inner = f"<style>{CSS}</style>\n{BODY}\n{data}"

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(f"<title>{TITLE}</title>\n\n{inner}")

    with open(os.path.join(OUT, "dashboard-standalone.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="description" content="Two car-free Shikoku routes for October 2026.">
<title>{TITLE}</title>
</head>
<body>
{inner}
</body>
</html>
""")
    print("wrote dashboard.html and dashboard-standalone.html")

if __name__ == "__main__":
    main()
