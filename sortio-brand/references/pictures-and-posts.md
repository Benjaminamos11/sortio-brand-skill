# Pictures and posts: how to make them

How to produce static Sortio content: feed posts, stories, carousels and single pictures. There are two proven ways, both used for the 10 test ads of October 2026 (all 10 are in `assets/examples/posts/`):

- **Set A — designed**: an HTML/CSS template with real app screenshots, rendered to an exact-size PNG. Ads 01–05.
- **Set B — AI images**: a photorealistic scene generated with Higgsfield (GPT Image 2.5), with the text either rendered by the AI or laid on top as HTML. Ads 06–10.

Read `design-system.md` (look), `voice-and-copy.md` (words) and `product-facts.md` (what may be claimed) first.

---

## 1. Set A: HTML/CSS template + real screenshots

### 1.1 What is in `templates/posts/`

| File | Format | Based on |
|---|---|---|
| `post-feature-screenshot-4x5.html` | Feed 1080×1350, one feature + one app crop | Ad 02 "QR-Rechnungen ohne Abtippen." |
| `story-sortio-ai-9x16.html` | Story 1080×1920, dark abyss band, phone + question bubble + answer card | Ad 04 "Frag deine Unterlagen." |
| `post-price-4x5.html` | Feed 1080×1350, "CHF 0 zum Start." + Pro card at CHF 10.– | Ad 03 (price corrected) |
| `post-quote-1x1.html` | Square 1080×1080, text only, a Sortio AI question on an ember card | sortio.ch "Im Alltag" card 04 |
| `carousel-slide-4x5.html` | Carousel slide 1080×1350, one everyday situation, 5 colour tones | sortio.ch "Im Alltag" cards |
| `story-photo-overlay-9x16.html` | Story 1080×1920, AI photo + HTML headline, lockup, CTA (the Set B overlay) | Ad 09 "In der Schweiz gespeichert." |
| `ads.css` | Shared tokens and components; loads the bundled fonts | Ad kit `ads.css` |
| `render.py` | Renders every HTML file to PNG/JPG at its declared size and checks it | Ad kit `render.py` |

Every template links `ads.css` and uses relative paths into `../../assets/` (logo, fonts, screens), so the folder structure must stay as it is. Each file declares its size in `<meta name="sortio:size" content="1080x1350">` and uses one canvas class: `post` (1080×1350), `story` (1080×1920), `square` (1080×1080) or `landscape` (1920×1080).

### 1.2 Make a post

1. Pick the angle and copy (one message per post) from `voice-and-copy.md`.
2. Copy the closest template inside `templates/posts/` and give it a new name, e.g. `2026-12-steuern-post.html`. For a carousel, make one file per slide: `steuern-01.html`, `steuern-02.html` …
3. Edit only the text and the image path. Screens: `../../assets/screens/<name>.webp`; crops: `../../assets/screens/crops/<name>.webp` (available: payment, plan, fields, folders, senders, swipe, chart, ai-cards). Full screens: home, folders, folder-invoices, folder-swipe-paid, document-top, document-fields, document-payment, review-result, analysis-running, scanner-page, plan-sheet, tasks, stats, chat-open-bills, chat-cards, chat-calendar.
4. Keep `data-check="…"` on every text block and the CTA; the renderer uses it to find overflow and safe-zone problems.
5. Render (below), look at the PNG at 100 % and on a phone, fix, render again.

### 1.3 Render on your own machine

Needs Python 3.9 or newer (macOS: `python3 --version`; install from python.org if missing).

```bash
# once
pip install playwright        # or: pip3 install playwright
playwright install chromium   # or: python3 -m playwright install chromium

# every time (from anywhere)
cd path/to/sortio-brand/templates/posts
python3 render.py                                  # renders every .html here
python3 render.py post-price-4x5.html              # only this one
python3 render.py --out ~/Desktop/sortio --jpg     # JPG into another folder
python3 render.py --scale 2 story-sortio-ai-9x16.html   # 2x proof for zooming
```

Output goes to `templates/posts/renders/` (ignored by git) unless you pass `--out`. The script waits for the fonts and images, screenshots the `.ad` element at exactly the declared size and prints one line per file:

- `[ok] post-price-4x5.html -> …/renders/post-price-4x5.png (1080x1350)`
- `[CHECK] …` followed by what to fix: `image not found: …` (wrong path), `font not loaded: …`, `headline: text wider than its box`, `cta: outside the safe zone 250-1580` (stories). The exit code is 1 when anything needs a look.

Fonts come from `assets/fonts/`; if those files are missing, `ads.css` falls back to Google Fonts (needs internet).

**Without Python** (fallback): open the HTML file in Chrome → View → Developer → Developer Tools → toggle the device toolbar (Cmd+Shift+M) → set the size to e.g. 1080 × 1350 and zoom 100 % → Cmd+Shift+P → "Capture full size screenshot". Check the size of the resulting PNG.

### 1.4 Rules for Set A

- Only real screens from `assets/screens/` (sample data, letters marked MUSTER). Never edit numbers in a screenshot and never build fake UI.
- Text that repeats something from the screen (bubbles, totals) must match the screen exactly.
- One message, one accent, one CTA per post. Footer: lockup left, CTA right (posts); everything between y 250 and 1580 (stories).
- Export PNG for type-heavy designs (crisp text); JPG quality 90+ only when a photo dominates. sRGB.

---

## 2. Set B: AI images with Higgsfield

Account and connection setup: see `tools-setup.md`. Higgsfield costs credits; generate on purpose, not in bulk.

### 2.1 Model and settings (used for all five kit images)

| Setting | Value |
|---|---|
| Model | **GPT Image 2.5** (`gpt_image_2_5`, variant "flare") — Higgsfield's default for images with text and design |
| Quality | high |
| Resolution | 2k → 4:5 comes out at **1792×2240**, 9:16 at **1520×2688** |
| Aspect | 4:5 for feed, 9:16 for stories |
| Cost | **2.75 credits per image** (Higgsfield Ultra plan, October 2026). The five kit images cost 13.75 credits; all five first generations were usable, no re-rolls |
| References | Upload the real logo (`assets/logo/sortio-mark-origami.png`) when the AI should draw the lockup, and the real app screen when a phone screen is visible (07: `review-result`, 08: `folder-invoices`, 09: `home`). Convert WebP to PNG first if the upload refuses WebP: `sips -s format png assets/screens/home.webp --out home.png` |

### 2.2 Two ways to handle text

**A. The AI renders all text, logo and CTA** (ads 06 and 10). Put every word in the prompt in quotes, with font style, colour hex and position, and say "Spell every German word exactly as given. No other text anywhere." Check the result letter by letter; the kit's German came out correct. Then scale to the post size:

```bash
sips -z 1350 1080 raw.png --out post.png          # 4:5 raw (1792x2240) is exactly 4:5
```

Best for: feed posts where the scene and text must feel like one photo. Risks: the wordmark may come out bolder than Inter SemiBold (06), fine print on letters is gibberish when zoomed, no control over exact kerning.

**B. Generate without text, add text as HTML** (ads 07, 08, 09). Ask for "no text, no logos, no watermark outside the phone screen" and for a calm empty zone where the headline goes. Then put headline, lockup and CTA on top in the brand fonts with `templates/posts/story-photo-overlay-9x16.html` (replace the `.bg` image path with your file and render). For a 4:5 overlay, copy the story template, switch the class to `post`, the meta size to `1080x1350`, and set the text in a left column (ad 08: column 540px wide at left 64px, headline 58px, chips, CTA under it).

Best for: stories (exact safe zones), anything with a price or a claim, paid ads. The 9:16 raw (1520×2688) is not exactly 9:16; the overlay template crops it with `object-fit: cover`. Without the template: `magick raw.png -resize 1080x1920^ -gravity center -extent 1080x1920 story.png`.

In both ways the phone screen inside the image is the model's copy of the reference screen (very close in 07 and 09, smaller and less exact in 08). The kit did not composite the real screenshot on top. If the screen must be exact (a price, an amount), use Set A or composite the real screen in HTML.

### 2.3 Prompt pattern that worked

```
[Format line] Instagram feed ad (4:5) | Vertical 9:16 photograph for an Instagram story, photorealistic [editorial / lifestyle] photograph[, with clean typography | , no text].
Scene: [one concrete Swiss everyday place: Zurich Altbau kitchen / balcony / workshop office / window with old town, lake and Alps], [the letters, invoices with QR payment slips, phone], no people | [one person, age, clothing, calm expression].
[If a phone screen shows:] The phone screen faces the camera, fully visible, unobstructed, showing exactly the app screen from the reference image ([describe it briefly]).
Light and palette: bright soft daylight, warm off-white #faf9f6, stone #f1efea, natural oak, [near-black accents], one small ember-orange #ff4f00 accent ([object]).
Composition: [subject] in [part of the frame]. The [top 28–38% / left 45%] of the frame is calm and empty, reserved for [a headline | typography].
Quality: shallow depth of field, premium magazine quality.
[Approach A only:] Typography in that empty area, left-aligned with generous margins. Headline in an elegant editorial serif (like Hedvig Letters Serif), regular weight, tight tracking, near-black #0a0b0d, exactly: "…". Below it, smaller, in a clean sans serif (Inter), graphite grey #5d6169, exactly: "…". Bottom left: a small brand lockup, the orange paper-plane logo from the reference image next to the word "Sortio" in semibold sans serif. Bottom right: a rounded pill button in [ember orange #ff4f00 | near-black #0a0b0d] with white sans-serif text exactly "…". Spell every German word exactly as given.
Closing: No other text anywhere, no watermark, no other logos. | No text, no logos, no watermark outside the phone screen.
```

### 2.4 The five prompts from the kit (verbatim)

**06 · Feed 4:5 · "Briefe stapeln sich auf dem Tisch?" · text by the AI · reference: Sortio logo**
> Instagram feed ad (4:5), photorealistic editorial photograph with clean typography. Scene: a light oak kitchen table in a bright Zurich Altbau apartment (white walls, tall window, soft morning daylight from the left). On the table an overflowing, messy stack of paper letters and bills: Swiss windowed envelopes, invoices with QR payment slips, folded letters, a few envelopes sliding off the pile. Beside it a white ceramic coffee cup. No people. Calm warm palette: warm off-white #faf9f6, paper white, stone beige #f1efea, with one small ember-orange #ff4f00 accent (an orange pencil on the pile). Shot from slightly above, shallow depth of field, soft natural shadows, magazine quality. The upper 38% of the frame is calm, empty, softly lit wall space reserved for typography. Typography in that empty top area, left-aligned with generous margins. Headline in an elegant editorial serif (like Hedvig Letters Serif), regular weight, tight tracking, near-black #0a0b0d, exactly: "Briefe stapeln sich auf dem Tisch?" Below it, smaller, in a clean sans serif (Inter), graphite grey #5d6169, exactly: "Foto machen – Sortio liest und legt ab." Bottom left: a small brand lockup, the orange paper-plane logo from the reference image next to the word "Sortio" in semibold sans serif, near-black. Bottom right: a rounded pill button in ember orange #ff4f00 with white sans-serif text exactly "Gratis starten". Spell every German word exactly as given. No other text anywhere, no watermark, no other logos.

**07 · Story 9:16 · "Jeder Brief in Sekunden digital." · HTML overlay · reference: `review-result` screen**
> Vertical 9:16 photorealistic lifestyle photograph for an Instagram story, no text. A person's hands (warm skin tone, cream knit sweater sleeves) hold an iPhone upright over a paper letter on a light oak table, as if they just photographed the letter. The letter on the table is a Swiss health-insurance bill with a QR payment slip at the bottom. The phone is held straight and facing the camera, its whole screen fully visible and unobstructed by fingers, showing exactly the app screen from the reference image (light UI: scanned letter preview at top, two cards 'Absender' and 'Betrag', black button at the bottom). Bright soft daylight, warm white #faf9f6 and stone beige tones, a single ember-orange #ff4f00 accent (an orange pen on the table). The phone and hands sit in the middle of the frame, roughly from 30% to 80% of the height. The top 28% of the frame is calm, softly blurred warm-white wall, empty, reserved for a headline. The bottom 18% is calm blurred table surface. Shallow depth of field, premium magazine quality. No text, no logos, no watermark outside the phone screen.

**08 · Feed 4:5 · "Die Administration deines Betriebs, im Griff." · HTML overlay · reference: `folder-invoices` screen**
> Photorealistic editorial photograph, 4:5, no text. A Swiss small-business owner (woman around 40, dark blonde hair tied back, linen shirt, relaxed and in control) sits at a clean wooden desk in her bright small workshop office (a carpentry or design studio in Switzerland, white walls, big window, plants). Behind her, a shelf with neatly labelled ring binders and archive boxes, one binder in ember orange. On the desk: a small stack of supplier invoices, a laptop closed, a coffee cup. She holds an iPhone in one hand at a comfortable angle; its screen is visible to the camera and shows the app screen from the reference image (light UI list titled 'Rechnungen' with invoice rows and orange amounts). The person and desk occupy the right and lower part of the frame. The left 45% and the top 30% of the frame stay calm and uncluttered (soft white wall), reserved for text. Palette: warm off-white #faf9f6, stone #f1efea, natural oak, near-black accents, one ember-orange #ff4f00 accent. Natural daylight, shallow depth of field, premium magazine look. No text, no logos, no watermark outside the phone screen.

**09 · Story 9:16 · "In der Schweiz gespeichert." · HTML overlay · reference: `home` screen**
> Vertical 9:16 photorealistic photograph for an Instagram story, no text. A calm, premium Swiss scene: an iPhone stands upright, slightly tilted back on a small stand, on a light oak table directly in front of a large window. Through the window, softly out of focus: Zurich old town rooftops, church spires and the lake, the Alps faint in the distance, clear early morning light, pale sky. The phone screen faces the camera straight on, fully visible, and shows exactly the app screen from the reference image (light UI, greeting 'Salü, Benjamin', a card with 'CHF 150.50' and a black 'Bezahlen' button, orange camera button at the bottom). Beside the phone, a small neat stack of opened letters with a paper clip and a white cup. The phone sits in the vertical middle of the frame (about 35% to 78% of the height). The top 30% of the frame is calm pale sky, empty, reserved for a headline. The bottom 17% is calm table surface. Palette: warm white #faf9f6, stone, soft blue-grey sky, natural oak, one tiny ember-orange #ff4f00 accent. Premium magazine quality, shallow depth of field. No text, no logos, no watermark outside the phone screen.

**10 · Feed 4:5 · "Keine Frist rutscht durch." · text by the AI · reference: Sortio logo**
> Instagram feed ad (4:5), photorealistic lifestyle photograph with clean typography. Scene: a relaxed woman in her early 30s sits on a sunny balcony of a Zurich apartment building with a coffee, glancing at her iPhone with a calm, content expression (we see the back of the phone, not the screen). Soft late-afternoon light, potted plants, a linen cushion, an ember-orange #ff4f00 blanket or cushion as the single accent colour. Warm off-white and stone palette. She sits in the lower right two-thirds of the frame. The upper 36% of the frame is calm, softly blurred sky or light wall, empty, reserved for typography. Typography in that empty top area, left-aligned with generous margins. Headline in an elegant editorial serif (like Hedvig Letters Serif), regular weight, tight tracking, near-black #0a0b0d, exactly: "Keine Frist rutscht durch." Below it, smaller, in a clean sans serif (Inter), graphite grey #5d6169, exactly: "Sortio erinnert dich rechtzeitig." Bottom left: a small brand lockup, the orange paper-plane logo from the reference image next to the word "Sortio" in semibold sans serif. Bottom right: a rounded pill button in near-black #0a0b0d with white sans-serif text exactly "Jetzt testen". Spell every German word exactly as given. No other text anywhere, no watermark, no other logos.

The raw, text-free generation of 09 is in `assets/examples/posts/raw/09-raw-zuerich-fenster.jpg` (scaled to 1080 wide) so the overlay template renders out of the box.

### 2.5 Rules for Set B

- Swiss, bright, calm, real-looking. No stock-photo clichés (no thumbs up, no shocked faces, no piles of cash).
- One ember accent object per image; never an ember wash or filter.
- People are AI-generated: Meta may add an "AI info" label. Do not present them as customers, do not give them names or quotes.
- Third-party brands: the kit's 07 shows "Helsana Versicherungen AG" large on the letter and the phone. Avoid prominent real brands in new prompts ("a Swiss health-insurance bill" without a name), and ask Benjamin before using such an image in paid ads.
- A prompt never names a real private person. The 09 prompt mentions the demo account's greeting only because it describes the reference screen.
- Check every AI-rendered word, the logo shape, hands and fingers, the phone screen, and that no extra text or watermark slipped in.

---

## 3. When to use which

| Situation | Use |
|---|---|
| Showing a specific feature, a price, an exact amount, an AI answer, a claim | **Set A** |
| Carousels, explainer slides, before/after, price posts | **Set A** |
| Stories with a CTA (exact safe zone) | **Set A**, or **Set B with HTML overlay** |
| Emotional hook, relatable pain point, "Swiss life" mood, lifestyle scenes, KMU setting | **Set B** |
| Feed post where scene and type should feel like one photo | **Set B, AI-rendered text** (check spelling) |
| Paid ads | Set A, or Set B with HTML overlay; ask Benjamin about AI people and third-party logos |
| A/B testing "designed vs. AI" | A matched pair with the same message and format (the kit's suggestion: 06 vs. 01) |

Set A is free, exact and repeatable; Set B costs credits and adds stopping power. A good month mixes both: mostly Set A feature and situation posts, a few Set B images as hooks.

---

## 4. Carousels

- 4–7 slides, 1080×1350 (or 1080×1080 if the account's grid is square).
- Slide 1: the hook (a situation or question in the serif, one line of context). Middle slides: one situation or feature each (`carousel-slide-4x5.html`, or `post-feature-screenshot-4x5.html` for a screen). Last slide: what it costs and the CTA (reuse the price card or "Gratis starten" + "Im App Store laden").
- Same margins, same lockup corner, mono numbering "01 / 06" on every slide; vary the tone in a fixed order (e.g. paper → ink → ember → moss → stone).
- Render all slides in one go: `python3 render.py steuern-*.html` and upload in file order.

---

## 5. QA checklist before posting

**Format**
- [ ] Exact size: 1080×1350 (feed), 1080×1920 (story), 1080×1080 (square), 1920×1080 (landscape). `render.py` prints the real size.
- [ ] Stories: all text, lockup and CTA between y 250 and 1580; nothing important within 64px of the sides. Feed: key text at least 34px inside the left/right edges (3:4 grid crop).
- [ ] `render.py` shows `[ok]` for the file (no broken images, no missing fonts, no overflow).

**Words**
- [ ] Swiss spelling: no "ß" anywhere (search the file for ß), "du" form, guillemets «», en dash –.
- [ ] Every word spelled correctly, also inside AI images; feature names right ("Sortio AI", "QR-Rechnung").
- [ ] Headline ends with a full stop; no exclamation marks; no emoji in the image.
- [ ] CTA is one of the approved ones; Android only as "Bald bei Google Play".

**Facts**
- [ ] Prices match sortio.ch today (Basic CHF 0 with 8 scans/month, Pro CHF 10.– per month). No CHF 9.90. Yearly CHF 79 or the 7-day trial only with Benjamin's OK.
- [ ] Every amount, sender and date comes from a MUSTER sample screen and matches it exactly.
- [ ] No invented numbers, ratings, awards, user counts, testimonials or customer names.
- [ ] Data claims worded as on the site ("Daten in der Schweiz", "AES-256 verschlüsselt").
- [ ] Pro-only features (Sortio AI, Auto-Fristen) are not called free.

**Brand**
- [ ] Logo: correct file, not redrawn, not recoloured, clear space kept, white wordmark on dark/photo.
- [ ] One accent colour (ember) used once or twice; canvas/ink/stone otherwise.
- [ ] No box with an accent line on one side only; cards complete and rounded.
- [ ] Screenshots unedited, inside the phone frame or a rounded crop card.
- [ ] Third-party logos not the focus; AI people not presented as customers.

**Caption**
- [ ] Hook → what Sortio does → CTA with App Store / sortio.ch → 4–5 hashtags incl. #Sortio.
- [ ] Link in bio or the App Store link from `product-facts.md`.
