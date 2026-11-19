# Sortio reel template (9:16, 18 s, HyperFrames)

A working reel in the Sortio look: hook text with a pile of letters → phone with the real app screen → three feature beats with callouts → dark end card with logo and call to action. Original soundtrack included. Rendered and checked with HyperFrames 0.9.70 (0 errors in `check`). A preview of the result is in `../../assets/examples/reels/template-preview.mp4`.

| Time | Scene | On screen |
|---|---|---|
| 0.0–2.9 | Hook | «BISHER · Briefe stapeln sich auf dem Tisch.» Four envelopes and the sample letter land, the line is struck through, the letter flies into the scanner |
| 2.9–6.6 | Beat 1 | «01 — Scannen · Sortio liest, was wichtig ist.» Tap on «Scannen», flash, review screen, three callouts: Absender, Betrag, Fälligkeit |
| 6.6–10.1 | Beat 2 | «02 — Ablegen · Automatisch im richtigen Ordner.» Push to the folders, the callouts drop into «Versicherungen» |
| 10.1–13.7 | Beat 3 | «03 — Erinnern · Keine Frist rutscht durch.» Push to the tasks, the Helsana task is highlighted, callout «1 Tag vor Frist erinnern» |
| 13.7–18.0 | End card | Paper plane, «Sortio», «Verwaltungs-Assistent · Aus der Schweiz», «Weniger Papierkram. Mehr Kopf für das, was zählt.», «Im App Store laden», «sortio.ch · Kostenlos starten» |

## Files

| File | What it is |
|---|---|
| `reel-config.js` | **Everything you normally edit:** texts, screens, callouts, highlight boxes, durations. Strict JSON after `window.REEL =` (no comments, no trailing commas), because `tools/soundtrack.py` reads it too. |
| `index.html` | The HyperFrames composition: layout (CSS) and motion (one paused GSAP timeline built from the config). Colours mirror `../../references/design-system.md`. |
| `audio/soundtrack.m4a` | Original music and effects for the default timing (synthesised, no samples, free to use in ads). |
| `tools/new_reel.py` | Makes a self-contained copy of the template for one reel (see below). |
| `tools/soundtrack.py` | Rebuilds the soundtrack from the config timing (needs `numpy`, `scipy`, `ffmpeg`). |
| `tools/finalize.sh` | Loudness to −14 LUFS, poster frame as frame 0, cover JPG, faststart. |
| `hyperframes.json`, `package.json` | HyperFrames project files; `npm run check / preview / render / finalize` shortcuts. |

The template points at the skill's shared files with `../../assets/...` (screens, logo, fonts). **HyperFrames refuses paths above the project folder** (`invalid_parent_traversal_in_asset_path`), so never render inside the skill folder. Always start a reel with `new_reel.py`.

## Make a reel (Claude Code, on your computer)

```bash
cd ~/.claude/skills/sortio-brand/templates/reels         # or wherever the skill lives
python3 tools/new_reel.py ~/Sortio-Videos/2026-11-20-qr-reel
cd ~/Sortio-Videos/2026-11-20-qr-reel
# 1. edit reel-config.js (texts, screens, durations)
python3 tools/soundtrack.py                               # 2. only if you changed durations or beats
npx --yes hyperframes@0.9.70 check                        # 3. must end with 0 errors
npx --yes hyperframes@0.9.70 preview                      # 4. look at it in HyperFrames Studio (browser)
npx --yes hyperframes@0.9.70 render --output renders/reel.mp4
bash tools/finalize.sh renders/reel.mp4 5.4               # 5. -> renders/reel-final.mp4 + reel-cover.jpg
```

`new_reel.py` copies the template, copies every `../../assets/...` file the reel uses into the new folder's `assets/`, and rewrites the paths. If you later point the config at another screen (write it as `assets/screens/<name>.webp`), run `python3 <skill>/templates/reels/tools/new_reel.py <reel folder> --sync` to copy it in.

Render time on a recent Mac: about 15 s. Output: H.264, 1080×1920, 30 fps, AAC 48 kHz, about 5 MB.

## Editing

**Texts.** `hook.lines`, `beats[].eyebrow` and `beats[].lines`, `end.*`. Two lines of at most about 20 characters each at 92 px; check that nothing runs wider than the frame in `preview`. The second line of a beat is set in ember. Take headlines from `../../references/voice-and-copy.md`; Swiss spelling («ss», never «ß»).

**Screens.** `beats[].screen` is any file in `../../assets/screens/` (720×1565 px app screenshots with sample data). `beats[0].before` is the screen shown before the tap (the scanner), `tap` is the tap point in screenshot pixels.

**Callouts** repeat what the screen shows, they never add facts. Values must match the screenshot exactly (the review screen shows Helsana Versicherungen AG, CHF 412.30, Zahlbar bis 31.10.2026). Icons: `building`, `banknote`, `calendar`, `bell`, `folder`, `sparkle`, `check`. `"mono": true` sets amounts and dates in JetBrains Mono. Optional `"y"` overrides the vertical centre (keep it between 350 and 1180).

**Highlight.** `beats[].highlight` is a box `[x0, y0, x1, y1]` in screenshot pixels; it gets an ember ring and the rest of the screen is veiled. `"collect": true` makes the previous beat's callouts fly into that box (the «drops into the folder» move). To find a box, open the screenshot in Preview (Tools → Show Inspector shows the cursor position) or ask Claude to measure it with Python (PIL).

**Timing.** Each scene has a `duration`. If the total changes, update three places: `"duration"` in the config, and `data-duration` on `#root` and on `<audio id="music">` in `index.html` (the page logs an error and `check` fails when they disagree). Then rerun `tools/soundtrack.py`. Keep every beat at 3 s or more so the headline is readable (0.3 s per word after it has fully appeared).

**Number of beats.** Two to four beats work. Each beat needs its own screen. Example fourth beat for Sortio AI (values from `chat-open-bills.webp`):

```json
{
  "duration": 3.8,
  "eyebrow": "04 — Fragen",
  "lines": ["Frag deine", "Unterlagen."],
  "screen": "../../assets/screens/chat-open-bills.webp",
  "callouts": [
    { "icon": "sparkle", "label": "Sortio AI", "value": "Total: CHF 3’168.25", "y": 1100 }
  ]
}
```

Example QR-bill beat (values from `document-payment.webp`; check the screenshot before you use any number):

```json
{ "duration": 3.5, "eyebrow": "02 — Bezahlen", "lines": ["QR-Rechnung,", "ohne Abtippen."],
  "screen": "../../assets/screens/document-payment.webp", "callouts": [] }
```

**Music.** `tools/soundtrack.py` writes a new `audio/soundtrack.m4a` timed to the config (cue times mirror `index.html`; if you change motion times there, change the matching cues). To use a licensed track instead, put it in `audio/`, point `<audio id="music" src=...>` at it, and keep proof of the licence (see `../../references/reels-and-social-video.md`, Music).

**Poster / cover.** `finalize.sh <file> 5.4` bakes the frame at 5.4 s (beat 1 with the callouts settled) in as frame 0 and saves it as the cover JPG. Pick any settled frame; never a frame mid-transition.

## Formats

- **Reels, TikTok, Shorts, Stories:** this file as is (9:16).
- **Safe zone:** all reading text sits between y 290 and 1250 px, the band HyperFrames checks for Instagram Reels and YouTube Shorts. `check` still warns that some centred lines touch the right edge of the Shorts and TikTok zones (their right side is reserved for buttons); that is expected for Reels. For a TikTok-first cut, keep lines shorter (about 16 characters).
- **4:5 feed version:** do not crop the 9:16 file. Make a 1080×1350 variant (change `data-width/height`, the stage size and the vertical positions) or ask Claude to adapt the layout.

## Known `check` messages

- `container_overflow #phone … bottom 20px`: the phone is cut off by the frame edge on purpose.
- `outside_safe_zone … YouTube Shorts / TikTok (right edge)`: see Formats.
- `text_below_floor … "Fälligkeit" at 6 px`: the callouts while they shrink into the folder; not reading text.

Anything with ✗ (error) must be fixed before rendering.
