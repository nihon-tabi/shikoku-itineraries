# Route-planning tooling

## Google Maps MCP connector — installed, but USELESS for this trip

Installed `mcp-server-google-maps` (npm, v1.0.4, repo
<https://github.com/apurvaumredkar/google-maps-mcp>) and got it connected.

### Install notes (non-obvious)

This package is **HTTP-only — it has no stdio transport**, so the documented
`claude mcp add ... -- npx ...` stdio form fails with
`-32000: Connection closed`. Confirmed by unpacking the tarball: the only
env var it recognises is `MCP_AUTH_TOKEN`, and `dist/index.js` unconditionally
starts a `StreamableHTTPServerTransport` on `PORT` (default 3003).

Working setup:

```bash
# key + port live here, chmod 600
cat ~/.config/google-maps-mcp.env
#   GOOGLE_MAPS_API_KEY=...
#   PORT=3003

set -a; . ~/.config/google-maps-mcp.env; set +a
nohup npx -y mcp-server-google-maps > /tmp/gmaps-mcp.log 2>&1 &

claude mcp add --transport http --scope user google-maps http://localhost:3003/mcp
```

Health check: `curl -s http://localhost:3003/health` → `{"status":"ok",...}`.
The server must be running for the connector to work; it is not auto-started.

### Why it does not help — Google's Routes API has NO transit data for Japan

Tested directly against `routes.googleapis.com/directions/v2:computeRoutes`
with `travelMode: TRANSIT`:

| Query | Result |
| --- | --- |
| Awa-Ikeda Stn → Oboke Stn (Japan) | `{}` — zero results |
| Osaka Stn → Himeji Stn (Japan) | `{}` — zero results |
| Takamatsu Stn → Kotohira Stn (Japan) | `{}` — zero results |
| Kings Cross → Paddington (London) — control | 1298s, 4676 m ✅ |
| Grand Central → Times Square (NYC) — control | 473s, 1102 m ✅ |

The API key, billing and Routes API are all fine — the controls prove it.
Google simply does not serve transit routing for Japan through the API, even
though maps.google.com shows it in the browser. **Do not plan any Japanese
transit leg from this connector.**

### What to use instead

- **Operator timetables** (JR Shikoku station PDFs, Shikoku Kotsu, ferry
  companies) — authoritative, and they distinguish local vs limited express.
- **Jorudan** <https://world.jorudan.co.jp/mln/en/> — supports excluding
  limited express, which is the whole game here.
- **Yahoo! Transit** <https://transit.yahoo.co.jp/> — `expkind=1` in the query
  string excludes tokkyu; gives fares.
- **NAVITIME Japan Travel** <https://japantravel.navitime.com/en/>.

Google Maps *in the browser* is still fine for walking times and for locating
a bus stop.
