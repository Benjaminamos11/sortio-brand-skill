# Sortio design system (for social media)

This is the visual system for everything Sortio posts on social media: feed posts, stories, carousels, pictures and the stills inside videos. It is taken from three sources, all checked on 20 November 2026:

1. **sortio.ch**, the live website (Next.js, Tailwind v4 theme in `app/globals.css`, components in `app/_landing/`). Redesigned in October 2026.
2. **The Instagram ad kit**, 10 ads made in October 2026 (`templates/posts/ads.css` here is the portable version; the final ads are in `assets/examples/posts/`).
3. **The Sortio iOS app** (Expo / React Native, tokens in `src/theme/swiss.ts`).

**Rule of thumb: social media uses the website and ad-kit look** ("Swiss editorial": warm white canvas, near-black ink, an editorial serif for headlines, one ember-orange accent, real app screens in a phone). The app's own UI tokens matter only when you show or rebuild app screens.

---

## 1. Hard rules (from Benjamin, no exceptions)

1. **Never put an accent line or stripe on one side of a box only.** No `border-left` (or right/top/bottom) stripe and no inset box-shadow stripe on callouts, answer boxes, quotes, summaries, list items or table rows. Make a complete, polished card instead: rounded corners on all four sides, layered soft shadows or a softly tinted panel. A dot or an icon may mark a label. Neutral hairline dividers *between* equal rows or columns inside a card (as in the before/after table) and chart whiskers are fine. Note: the testimonial block on sortio.ch has a black rule above each quote; do not copy that pattern (and do not use testimonials at all, see `voice-and-copy.md`).
2. **Never add pause, play or stop buttons** to carousels, sliders, tickers or any other auto-moving element, not even "for accessibility" and not hidden behind a flag. Auto-advance may pause on hover or focus and stop after a click, arrow or swipe; that is enough. Do not propose it.
3. **One accent per layout.** Ember is used once or twice per frame (second headline line, check marks, one CTA, a glow). Never ember text on ember, never a second bright colour.
4. **Only real screens, only sample data.** Phone screens are real app captures with the sample letters marked MUSTER (see section 9). Never invent UI, numbers or app states.

---

## 2. Colour

### 2.1 Marketing palette (website + ad kit) — use this

| Token | Hex | Role |
|---|---|---|
| `canvas` | `#faf9f6` | Default background of posts and stories (warm white) |
| `paper` | `#ffffff` | Cards, crops, answer bubbles |
| `stone` | `#f1efea` | Tinted panels, table heads, quiet sections |
| `hairline` | `#e6e3dc` | 1.5px card borders (all four sides), row dividers inside cards |
| `ink` | `#0a0b0d` | Headlines, body on light, primary (black) button, Pro price card |
| `graphite` | `#5d6169` | Body copy, the muted second line of a headline |
| `steel` | `#8b8d98` | Eyebrows, fine print, struck-through "before" text |
| `ember` | `#ff4f00` | **The** accent: second headline line, check circles, "Gratis starten" button, question bubble, totals, glows |
| `ember-soft` | `#fff1ea` | Icon-tile background behind an ember icon, text selection |
| `ember-hover` | `#e64700` | Website hover state of ember buttons (not needed in static posts) |
| `abyss` | `#000710` | The dark band (Sortio AI section, dark stories) |
| `carbon` | `#15191e` | Hover of black buttons on the site; very dark surface |
| `moss` | `#4f6b4a` | Site token for success / "bezahlt" (waitlist confirmation text) |
| `moss-deep` | `#2f4430` | Dark green use-case card on the site; the ad kit's `--moss` |
| `ochre` | `#a8782a` | Defined on the site, not used in visible UI; reserve |
| `brick` | `#a4513a` | Defined on the site, not used in visible UI; reserve |

Small extras from the ad kit: phone body on the abyss band `#1a1e24`; the fact line over the Zürich photo `#2c3440`.

**Which is primary for marketing:** canvas + ink carry the layout, **ember `#ff4f00` is the brand accent**, abyss is the one dark surface. A good feed alternates light canvas posts with an occasional abyss or ink one.

**Opacity conventions** (from the site and kit): on dark backgrounds secondary text is white at 45–60 % (`rgba(255,255,255,0.45)` for the second headline line, `0.5` for eyebrows, `0.55` for notes, `0.6` for body), chips use `rgba(255,255,255,0.10)` fill or a `0.15` border. Ember glows: `rgba(255,79,0,0.10)` blurred 80–90px on light, `0.17` blurred 140px on abyss, `0.20–0.25` blurred 100–110px inside the ink price card.

### 2.2 Disagreements between sources

| Topic | Website | Ad kit | App | Use for social |
|---|---|---|---|---|
| Moss | `#4f6b4a` (token), `#2f4430` (card) | `--moss: #2f4430` | success `#4A6B4F` | `#2f4430` for a dark green card, `#4f6b4a` for "bezahlt" text |
| Canvas | `#faf9f6` | `#faf9f6` | `#FAFAF8` (light), `#000000` (dark) | `#faf9f6` |
| Ink | `#0a0b0d` | `#0a0b0d` | `#000000` | `#0a0b0d` |
| Orange | ember `#ff4f00` | ember `#ff4f00` | accent `#FF4F00` | `#ff4f00` |
| Logo orange | origami mark (gradient, about `#E07818`–`#F09028`) | same mark | flat plane in the app icon, measured `#FD6801` | do not recolour either mark |

### 2.3 Legacy colours (do not use for new content)

The site's older pages (`/qr`, `/card`, the old SVG logo) still use `brand-blue #0f172a`, `brand-orange #FF6B00` and `brand-light #f8fafc` (Tailwind slate). The app's old `colors.ts` (Material blue `#2196F3` etc.) is dead code. Neither is part of the current look.

### 2.4 App palette (only when rebuilding app UI)

From `src/theme/swiss.ts` (the code is the source of truth; the theme README in the app repo is out of date).

| Role | Light | Dark |
|---|---|---|
| canvas | `#FAFAF8` | `#000000` |
| surface / surfaceRaised | `#FFFFFF` / `#FFFFFF` | `#1C1C1E` / `#2C2C2E` |
| surfaceSunken | `#F2F2F7` | `#2C2C2E` |
| border / hairline | `rgba(0,0,0,0.045)` / `rgba(0,0,0,0.05)` | `rgba(255,255,255,0.10)` / `rgba(255,255,255,0.08)` |
| ink / inkSecondary / inkTertiary | `#000000` / `#8E8E93` / `#AEAEB2` | `#FFFFFF` / `#98989D` / `#636366` |
| accent | `#FF4F00` | `#FF4F00` |
| danger (overdue) | `#B23A2B` | `#E0705C` |
| warning (due soon) | `#A07A2C` | `#D4A94F` |
| success (paid) | `#4A6B4F` | `#8FB894` |
| info / appointment | `#3F5A4C` | `#7FA592` |

Each semantic colour has a 12 % "soft" tint for tiles and badges. In the app, orange is reserved for scan, Sortio AI and totals; the main button is black; red only means urgency. Category tiles are pastel tints, and orange is never a category colour.

---

## 3. Dark and light

- **Light is the default** for posts and stories: canvas background, ink type, ember accent.
- **Dark = the abyss band** (`#000710`), used on the site for the Sortio AI section and in the kit for the Sortio AI story. On abyss: white headline, second line white 45 %, ember glow, phone body `#1a1e24` with a 2px white-13 % outline, white CTA pill.
- **Ink cards** (`#0a0b0d`) are for the Pro price card and the closing "Jetzt starten" block, with a blurred ember glow in one corner.
- The app has a real dark mode (system setting). Marketing does not show dark-mode screens; all screenshots in `assets/screens/` are light.

---

## 4. Typography

### 4.1 Families

| Role | Family | Weights used | Where |
|---|---|---|---|
| Display / headlines | **Hedvig Letters Serif** (optical size 24pt) | 400 only | Website h1/h2, all ad headlines, big price numerals, quotes |
| Text / UI | **Inter** | 400, 500, 600 (700 rare) | Body, buttons, the "Sortio" wordmark in the lockup (600) |
| Mono | **JetBrains Mono** | 400–500 (700 in the app) | Eyebrows (uppercase, tracked), amounts, prices, IBAN, references, slide numbers |
| App display only | Inter Tight | 700, 800 | App screen titles ("Salü, Benjamin", "Rechnungen"). Not used in marketing type |

All four are free under the SIL Open Font License (OFL 1.1). The Latin subsets the website serves are bundled in `assets/fonts/` (with `OFL.txt`) and wired into `templates/posts/ads.css`. For desktop apps (Canva, Figma, Keynote) install the full families from Google Fonts: [Hedvig Letters Serif](https://fonts.google.com/specimen/Hedvig+Letters+Serif), [Inter](https://fonts.google.com/specimen/Inter), [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono), [Inter Tight](https://fonts.google.com/specimen/Inter+Tight). Fallbacks if a tool lacks them: serif "Times New Roman", sans `-apple-system / Helvetica Neue`, mono `Menlo`.

### 4.2 Social type scale (px on a 1080px-wide canvas, from the ad kit)

| Element | Font | Size / line height | Tracking | Colour |
|---|---|---|---|---|
| Hero numeral (price "0") | Hedvig 400 | 380 / 0.8 | −0.03em | ink |
| Headline, feed post | Hedvig 400 | 86–104 / 1.0–1.04 | −0.025em | ink; 2nd line graphite or ember |
| Headline, story | Hedvig 400 | 88–104 / 1.02–1.04 | −0.025em | ink (light) / white (dark) |
| Headline in a narrow column over a photo | Hedvig 400 | 58 / 1.06 | −0.025em | ink |
| Carousel slide title | Hedvig 400 | 88 / 1.06 | −0.025em | per tone |
| Quote (text-only post) | Hedvig 400 | 74 / 1.08 | −0.025em | white on ember |
| Eyebrow | JetBrains Mono 500, UPPERCASE | 19–22 | +0.14em | steel (light), white 50 % (dark), ember (inside an answer card) |
| Body | Inter 400 | 29–32 / 1.45–1.5 | −0.01em | graphite |
| Before/after rows | Inter 400 struck / Inter 500 | 28 / 1.32 and 31 / 1.28 | −0.012em | steel struck / ink |
| Chat question bubble | Inter 500 | 37 / 1.28 | −0.015em | white on ember |
| Amount / price | JetBrains Mono 400 | 50–66 | −0.03em | ink or white; "CHF" smaller in steel / white 55 % |
| CTA label | Inter 500 | 30–32 | −0.01em | white on ink/ember, ink on white |
| Chip | Inter 400 | 22–24 | −0.005em | graphite |
| Lockup wordmark "Sortio" | Inter 600 | 34–40 | −0.02em | ink / white |

Headlines are sentence case and end with a full stop ("Keine Frist rutscht durch."). Two-line headlines put the second thought on its own line in a second colour: graphite on light ("Mehr Kopf für das, was zählt."), white 45 % on dark ("Bekomm Antworten."), or ember for the punchline ("ohne Abtippen.", "Start.").

### 4.3 Website scale (CSS px, for reference)

Hero h1 44 / 56 / 64px (mobile / tablet / desktop), line height 1.03, tracking −0.025em; section h2 40px → 52–60px, line height 1.05; feature title 34–42px, line height 1.1; card title 30px; body 16–19px at line height 1.6; eyebrow JetBrains Mono 11px, +0.14em, uppercase, steel; nav links Inter 500 14px; buttons Inter 500 15px in a 48px pill; prices JetBrains Mono 44px with "CHF" and "/ Monat" at 14px.

### 4.4 App scale (only for app-UI mock-ups)

display Inter Tight 800 34/40 (−1.2) · title1 Inter Tight 800 28/34 (−0.8) · title2 Inter Tight 700 22/28 (−0.5) · headline Inter 600 17/22 · body Inter 400 15/22 · callout Inter 500 13/18 · caption Inter 500 12/16 · micro Inter 600 11/14 uppercase +1.2 · amounts JetBrains Mono 700, tabular, 13/15/20/28.

---

## 5. Logo

### 5.1 Files (`assets/logo/`)

| File | What | Use |
|---|---|---|
| `sortio-mark-origami.png` | Orange origami paper plane with a white Swiss cross, transparent, 344×344 | **The in-post mark.** Used by the website nav and footer and by every ad in the kit |
| `sortio-lockup-ink.png` | Origami mark + "Sortio" (Inter 600, ink), transparent, 766×264 | Lockup on light backgrounds, for tools without the fonts (Canva etc.) |
| `sortio-lockup-white.png` | Same with white wordmark | Lockup on abyss, ink, ember or photos |
| `sortio-app-icon-1024.png` | Current App Store icon: flat orange plane on a white rounded tile | Profile picture, "download the app" end cards, anywhere the App Store icon is meant |
| `sortio-plane-flat.svg` / `sortio-plane-flat-white.svg` | Vector of the flat plane from the app icon (traced from the 1024px icon, `#FD6801` / white) | Large sizes and motion. It is a close trace, not the designer's master file |

There are **two marks in use**: the origami plane with the Swiss cross (website, ad kit) and the flat plane (App Store icon since the "Neues App-Icon" update, website favicon). For posts follow the website and the kit: origami mark in the lockup. Use the flat icon where people should recognise the app on their home screen. Ask Benjamin before mixing both in one piece.

Not shipped on purpose: the old `sortio-logo-with-text.svg` from the website repo ("sortio.ch" in heavy slate type with an orange ".ch", legacy colours). Do not recreate it.

### 5.2 Lockup and clear space

- Lockup = mark + the word "Sortio" set live in **Inter SemiBold (600)**, tracking −0.02em, capital S, no ".ch". Mark height = 1.45 × the wordmark font size (58px mark with 40px type; 50px with 34px); gap = 0.35 × font size (14px at 40px).
- Clear space around the lockup: at least the mark's height on every side (58px at the standard size). Posts keep the lockup in the bottom-left corner 72px from the edges, or top-right in photo stories.
- Minimum size: mark 40px on a 1080px canvas.
- On light: ink wordmark. On abyss, ink, ember or busy photos: white wordmark. The mark itself always stays orange.

### 5.3 Don'ts

Do not recolour, outline, rotate or stretch the mark; do not add a drop shadow or glow to it; do not put the origami mark on an ember background (it disappears, use the white wordmark on ember and keep the mark small, or put the lockup on a white chip); do not set "Sortio" in the serif or in all caps; do not let an AI image model redraw the logo for paid ads without checking it closely (in ad 06 the AI drew the wordmark bolder than Inter 600).

---

## 6. Spacing, radius, shadow

### 6.1 Spacing

- Side margins: **72px** on posts and stories (64px on dense layouts, 96px for the footer of the screenshot post).
- Top: eyebrow at 76–80px on posts; story text starts at **268–272px**.
- Bottom: footer (lockup + CTA) 72–76px from the bottom edge on posts.
- Vertical rhythm on posts: eyebrow → headline 22–34px, headline → body 30px, headline block → card 52–56px.
- App spacing scale (for app UI): 2 · 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 56; gutter 20, card padding 16, card gap 12, section gap 28.

### 6.2 Radius

| Element | Radius |
|---|---|
| Buttons, chips, tags, outcome pills | pill (999px) |
| Cards in posts | 28px (website 24–28px) |
| Big tinted panels | 40px |
| Pro price card | 32px |
| Screenshot crops | 34px in posts (20px on the website) |
| Question bubble | 40 40 12 40 (small corner = the tail, bottom right) |
| Answer card | 36px |
| Icon tiles | ~30 % of the tile (34px on a 112px tile, 15px on 48px) |
| Phone body / screen | 16.55 % / 13.4 % of the phone width (48 / 39px at 290px) |
| App tokens | xs 6 · sm 10 · md 14 · lg 20 (cards) · xl 28 (sheets) · pill |

### 6.3 Shadow

Shadows are long, soft and warm-black, never hard. Use them on phones, crops and floating cards on light backgrounds; on dark backgrounds use a faint white outline instead.

| Use | CSS |
|---|---|
| Phone on light | `0 60px 120px -48px rgba(10,11,13,0.55), 0 0 0 1px rgba(10,11,13,0.06)` |
| Phone on abyss | `0 60px 120px -40px rgba(0,0,0,0.8), 0 0 0 2px rgba(255,255,255,0.13)` |
| Crop / floating card | `0 40px 80px -48px rgba(10,11,13,0.45)` (kit), `0 30px 60px -40px rgba(10,11,13,0.5)` (site) |
| Large floating sheet (plan crop) | `0 40px 90px -40px rgba(10,11,13,0.5)` |
| CTA over a photo | `0 24px 50px -24px rgba(10,11,13,0.6)` |
| Bubbles over a dark phone | `0 30px 60px -30px rgba(0,0,0,0.7)` / `0 40px 80px -36px rgba(0,0,0,0.75)` |

The app uses a warm shadow colour `#17120E` (card: y 6, blur 14, 16 %; raised: y 10, blur 22, 20 %; overlay: y 16, blur 34, 26 %) and no shadows in dark mode.

---

## 7. Iconography

- **Lucide** line icons (lucide.dev, ISC licence) everywhere: website (MapPin, Lock, Languages, Archive, Check, ArrowRight, BellRing, ShieldCheck, Building2, FileSearch, Calculator, Coffee, ReceiptText) and app. Stroke width 1.8–2 for icons, 2.5–3.2 for check marks. Round caps and joins.
- **Icon tile**: a rounded square (≈30 % radius) in a soft tint with the icon in the strong colour: ember-soft + ember on light, `rgba(255,255,255,0.10–0.20)` + white on dark or ember cards.
- **Check mark**: white check in an ember circle (38px circle, 20px check in posts) for "Mit Sortio" points; plain ember check (26px, stroke 2.8) in price lists; ink circle with white check on the website feature lists.
- **Arrow**: thin steel arrow (`rgba(139,141,152,0.6)`) between "Bisher" and "Mit Sortio".
- **Apple glyph** inside the "Im App Store laden" pill (path in the templates). Google Play only as "Bald bei Google Play" with the coloured Play glyph, never as a live download.
- **Sparkle** marks Sortio AI (app: lucide Sparkles in ember on ember-soft).
- No emoji in visuals.

---

## 8. Components that appear in marketing

All are implemented in `templates/posts/ads.css` and the templates.

- **Phone frame** (`.phone` + `.screen`): ink body, radius 16.55 % and bezel 3.45 % of its width, screen aspect 720 / 1565 (the screenshot size), long soft shadow. On abyss use `.phone.on-dark`. Typical widths: 540–560px on a story, 290–300px on the website.
- **Screenshot crop card**: a white card with 22px padding, 34px radius, 1.5px hairline on all sides and a soft shadow, holding one crop from `assets/screens/crops/`. Often sits on a stone panel with an ember glow behind it.
- **Before/after table** ("Bisher" / "Mit Sortio"): stone header row with mono labels (steel / ember), rows separated by hairlines, struck-through steel text → arrow → ember check + ink text. Whole table is one complete rounded card.
- **Chat bubbles** (Sortio AI): question = ember bubble, white Inter 500, tail corner bottom-right; answer = white card with an ember "SORTIO AI" eyebrow, graphite text and a mono total row. In the app itself the user's bubble is black and the AI bubble white.
- **Price cards**: Basic as plain text or a canvas card; Pro as an **ink card** with an ember glow, "Pro" in Inter 600, mono price ("CHF" small, "10.–" big, "/ Monat" small), ember check list, a mono fine-print line ("MONATLICH KÜNDBAR"). The website adds an ember "BELIEBT" pill to the Pro card.
- **CTA buttons**: 92px pill on 1080px canvases (48px on the site). Ink with white text (default, "Im App Store laden" with Apple glyph), ember for "Gratis starten", white with ink text on dark.
- **App Store badge**: the website and kit use the pill with the Apple glyph, not Apple's official badge. For paid ads Apple's official "Laden im App Store" badge (Apple Marketing Tools, tools.applemarketingtools.com) is the guideline-safe choice; never redraw or recolour it.
- **Chips**: pill, 1.5px hairline, white fill, graphite text (e.g. "Kreditoren · MWST · AHV & BVG · Treuhand").
- **Use-case card / carousel slide**: tag chip + mono number ("02 / 06"), icon tile, serif title, problem (muted) + what Sortio does (stronger), outcome pill with check. Tones: paper, ink, ember, moss-deep, stone.
- **Trust strip**: lucide icon in ember + mono uppercase label ("DATEN IN DER SCHWEIZ", "AES-256 VERSCHLÜSSELT", "DEUTSCH · FRANZÖSISCH · ENGLISCH").
- **Ember glow**: a blurred ember circle behind phones and price cards; never a hard gradient band.

---

## 9. Screenshot and photo treatment

**Screenshots** (`assets/screens/`, 720×1565 WebP, status bar 09:41, full battery; crops 900px wide in `crops/`; home-screen pieces in `hero/`):
- They are real captures of the app with **sample letters marked "MUSTER"** (recipient "Laura Frei, Seestrasse 12, 8002 Zürich" is fictional; the IBAN `CH44 3199 9123 0008 8901 2` is the standard sample IBAN). The demo account's greeting shows the first name "Benjamin" (the founder); these exact screens are public on sortio.ch.
- Always show them inside the phone frame or as a rounded crop card. Never stretch, recolour, blur or retouch them, never change an amount, date or name, and never fake a screen state.
- Enlarged callouts (bubbles, total cards) must repeat **exactly** what the screen shows (e.g. "Total CHF 3’168.25" from `chat-open-bills`).
- Third-party sender names and logos appear on screens (Helsana, Swisscom, SBB, ewz, Serafe, AXA, Migros). Fine for organic posts like on the website; for paid ads ask Benjamin, and never make a third-party logo the hero of the image.
- Not included on purpose: `home-recent` (rendering glitch: the greeting overlaps a card) and `scanner-empty` (shows the English iOS Files picker).

**Photos and AI images**: bright, calm, Swiss. Warm off-white and stone palette, natural light oak, soft daylight, shallow depth of field, magazine quality; Zürich settings (Altbau kitchen, balcony, old-town rooftops, lake and Alps). Exactly one small ember-orange object as an accent (a pencil, a binder, a blanket). Leave a calm empty zone for type (top 28–38 % of the frame, or the left 45 % on a 4:5 post). No text, logos or watermarks inside the photo unless you deliberately let the AI render the text (see `pictures-and-posts.md`). AI-generated people may get Meta's "AI info" label.

---

## 10. Layout grids and safe zones

All sizes in px. Keep text and CTAs inside the safe area; backgrounds and decorative images may bleed.

### Feed post 4:5 — 1080 × 1350 (default for feed)
- Margins 72 left/right, eyebrow at y≈80, footer baseline 72 from the bottom.
- Zones: **top 0–520** eyebrow + headline + body; **middle 520–1180** visual (crop card on a stone panel, phone, table or price card); **bottom 1180–1278** footer: lockup left, CTA right.
- Instagram's profile grid now crops feed posts to 3:4 in the centre (about 1012 × 1350): keep key text at least 34px inside the left and right edges.

### Story 9:16 — 1080 × 1920
- **Safe zone y 250–1580** for all text, lockup and CTA (top 250 = profile bar and progress; bottom 340 = reply bar and stickers). Sides 64–72.
- Typical: eyebrow + headline at y 268–272; visual 660–1500 with a gradient fade into the background colour near 1180–1510; footer row (lockup + CTA) at y≈1468, or a centred CTA at y 1452–1488.
- Reel covers and in-video text follow stricter Reels rules (much bigger bottom zone for caption and buttons); see `reels-and-social-video.md`.

### Square 1:1 — 1080 × 1080
- Margins 56–72; card inset 56 with 44px radius; footer row 56 from the bottom. Use for text-only posts, carousels that must stay square, and link previews.

### Landscape 16:9 — 1920 × 1080 (web, LinkedIn, YouTube, presentations)
- Not in the ad kit; derived from the website hero: margins 120, text column on the left 7 of 12 columns (≈ 960px), headline Hedvig 96–120px, phone (width ≈ 400px) or crop on the right with an ember glow; footer row 96 from the bottom.

### Carousel
- 1080 × 1350 per slide (or 1080 × 1080). Same margins on every slide, number slides in mono ("01 / 06"), keep the lockup in the same corner, put the CTA on the last slide. Instagram may crop carousel slides in the grid to the first slide's 3:4 centre.

---

## 11. Motion feel (where defined)

From the website (framer-motion) and the app (`theme.motion`). The video agent's references cover full video; this is the feel to match in any animated post.

- **Easing**: `cubic-bezier(0.22, 1, 0.36, 1)` (fast out, long settle). Things settle, they do not bounce.
- **Reveal**: fade in and rise 24px over 0.8s; stagger 0.05–0.08s between items; strike-through lines draw in 0.5s.
- **Tabs / auto-advance**: 6.5s per item, a thin ember progress bar, pauses on hover/focus, stops for good after a click. No pause/play button.
- **Count-up** numbers: 1.6s, always land on the exact final value.
- **Springs**: segmented pill stiffness 420 / damping 34; app spring speed 16 / bounciness 3; press-in instant.
- **App durations**: fast 150ms, base 220ms, slow 320ms; cubic ease-out.
- Screen recordings of Sortio AI chats on the site are sped up 1.5×. Reduced-motion users get the static frame.

---

## 12. Ready-to-paste CSS custom properties

```css
@import url("https://fonts.googleapis.com/css2?family=Hedvig+Letters+Serif:opsz@12..24&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=block");

:root {
  /* surfaces */
  --sortio-canvas: #faf9f6;
  --sortio-paper: #ffffff;
  --sortio-stone: #f1efea;
  --sortio-hairline: #e6e3dc;
  /* text */
  --sortio-ink: #0a0b0d;
  --sortio-graphite: #5d6169;
  --sortio-steel: #8b8d98;
  /* accent */
  --sortio-ember: #ff4f00;
  --sortio-ember-soft: #fff1ea;
  --sortio-ember-hover: #e64700;
  /* dark */
  --sortio-abyss: #000710;
  --sortio-carbon: #15191e;
  --sortio-phone-dark: #1a1e24;
  /* quiet tones */
  --sortio-moss: #4f6b4a;
  --sortio-moss-deep: #2f4430;
  --sortio-ochre: #a8782a;
  --sortio-brick: #a4513a;

  /* type */
  --sortio-font-display: "Hedvig Letters Serif", "Times New Roman", serif;
  --sortio-font-sans: "Inter", -apple-system, "Helvetica Neue", Arial, sans-serif;
  --sortio-font-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
  --sortio-tracking-display: -0.025em;
  --sortio-tracking-eyebrow: 0.14em;
  --sortio-leading-display: 1.04;
  --sortio-leading-body: 1.45;

  /* social sizes at 1080px width */
  --sortio-h1-post: 92px;
  --sortio-h1-story: 96px;
  --sortio-body: 30px;
  --sortio-eyebrow: 22px;
  --sortio-cta-height: 92px;
  --sortio-cta-font: 32px;
  --sortio-margin: 72px;
  --sortio-story-safe-top: 250px;
  --sortio-story-safe-bottom: 1580px;

  /* shape */
  --sortio-radius-pill: 999px;
  --sortio-radius-card: 28px;
  --sortio-radius-panel: 40px;
  --sortio-radius-crop: 34px;

  /* shadow */
  --sortio-shadow-phone: 0 60px 120px -48px rgba(10,11,13,0.55), 0 0 0 1px rgba(10,11,13,0.06);
  --sortio-shadow-phone-dark: 0 60px 120px -40px rgba(0,0,0,0.8), 0 0 0 2px rgba(255,255,255,0.13);
  --sortio-shadow-card: 0 1px 2px rgba(10,11,13,0.04), 0 30px 60px -40px rgba(10,11,13,0.45);
  --sortio-shadow-float: 0 2px 6px rgba(10,11,13,0.05), 0 40px 80px -40px rgba(10,11,13,0.5);
  --sortio-glow: rgba(255,79,0,0.10);

  /* motion */
  --sortio-ease: cubic-bezier(0.22, 1, 0.36, 1);
  --sortio-reveal-duration: 0.8s;
}
```

The templates use the same values without the `sortio-` prefix (see `templates/posts/ads.css`).
