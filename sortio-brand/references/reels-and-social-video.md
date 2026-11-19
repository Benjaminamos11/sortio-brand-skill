# Reels, TikToks, story videos and short ads

How to make short Sortio videos (6–60 s): formats, story structures that fit Sortio, pacing, captions, music and voice, how the two existing reels were made, when to use real app screens and when AI video, the honesty rule, the QA gate and the posting copy.

Colours, fonts, logo use and type sizes are in `design-system.md`; wording, CTAs and hashtags in `voice-and-copy.md`; what Sortio does and may claim in `product-facts.md`. This file does not repeat them. Tool installation: `tools-setup.md`. The working template: `templates/reels/` (see its README).

Examples in this skill: `assets/examples/reels/11-reel-sortio-preview.mp4` (reel 11, 720p preview), `11-reel-sortio-cover.jpg`, `12-reel-cinematic-cover.jpg`, `template-preview.mp4`. The full reel 12 is in the repo's `examples/12-reel-cinematic.mp4` (outside the skill folder).

---

## 1. Pick the route

| Route | Looks like | Cost | Time | Use for |
|---|---|---|---|---|
| **A. Template reel** (`templates/reels/`) | Reel 11: warm canvas, serif headlines, real app screens in a phone, callouts, dark end card | FREE (local render) | 1–2 h | Feature reels, ads, the default |
| **B. Cinematic reel** | Reel 12: AI-generated film shots of a person (Higgsfield), then the real app screens, then the person again | PAID (≈ 45–60 Higgsfield credits) | half a day | Brand and awareness ads, one or two a month |
| **C. Screen recording reel** | A real screen recording of the app inside the phone frame, with headlines and captions | FREE | 1–2 h | Showing a flow exactly as it works (QR bill → banking app, Sortio AI typing) |

Routes A and C share the template: put a screen recording (`<video muted>`) where the template puts a screenshot. Route B uses the template's end card and app scenes and adds AI clips in front.

## 2. Format specs

| | Reels / TikTok / Shorts | Instagram Story video | Feed video (Instagram, LinkedIn) |
|---|---|---|---|
| Aspect, size | **9:16, 1080×1920** | 9:16, 1080×1920 | **4:5, 1080×1350** (make a separate layout; never crop the 9:16) |
| Text safe zone | **y 290–1250 px, x 65–890 px** (Instagram covers the top ≈14 % and the bottom ≈35 % with UI and caption; YouTube Shorts reserves the right side) | y 250–1580 px | 80 px margin all round |
| Length | **15–25 s** for ads and feature reels (reel 11: 20 s, reel 12: 22.5 s); 35–60 s for an informative reel with voice | 5–15 s works best (a story card can run up to 60 s) | 15–45 s |
| Frame rate | **30 fps** (render the same rate end to end) | 30 fps | 30 fps |
| Video codec | H.264 High, yuv420p, bt709, `+faststart`; HyperFrames default quality (CRF 16) gives ≈ 5 MB for 18 s, which is fine: the platforms re-encode anyway | same | same |
| Audio | AAC, 48 kHz, stereo, 192 kbps; **−14 LUFS integrated, true peak ≤ −1.5 dBTP** (what Instagram, TikTok and YouTube normalise to) | same | same |
| Captions | **Burned in** (most people watch muted) | burned in | burned in |
| First frame | A settled, readable frame (the poster): feeds and grids show it as the thumbnail. `tools/finalize.sh <file> <seconds>` bakes a chosen frame in as frame 0 | same | same |

The HyperFrames `check` command audits the Instagram Reels, TikTok and YouTube Shorts safe areas, text size (≥ 28 px on a 1080 px wide frame), contrast and overlaps. Fix every ✗; read every ⚠.

**Cover.** Upload a cover JPG (1080×1920) with the reel. The Instagram profile grid shows a centre crop of it (about 3:4 since 2025), so keep the headline in the middle 1080×1440 area. Good covers: the hook headline with the letter pile (reel 11 used the settled beat 1 frame with the three callouts), or a person with the claim (reel 12 used «Weniger Papierkram.» over the smiling woman).

## 3. Story structures that fit Sortio

Every Sortio reel tells one small story about paper mail, and the app is the turn in the story. One message per reel. Open on the problem or the result, never on the logo.

### 3.1 Pain → scan → filed → reminded (reel 11, the template)

| Time | Beat | On screen (real wording) |
|---|---|---|
| 0–3 s | **Hook: the pain** | «BISHER · Briefe stapeln sich auf dem Tisch.» Letters land on a pile; the line is struck through |
| 3–6 s | **Scan** | «01 — Scannen · Sortio liest, was wichtig ist.» Tap, flash, review screen; callouts Absender / Betrag / Fälligkeit |
| 6–9 s | **Filed** | «02 — Ablegen · Automatisch im richtigen Ordner.» The callouts drop into «Versicherungen» |
| 9–12 s | **Reminded** | «03 — Erinnern · Keine Frist rutscht durch.» The task lifts, a bell, «1 Tag vor Frist erinnern» |
| 12–16 s | **Ask** (optional 4th beat) | «04 — Fragen · Frag deine Unterlagen.» Real Sortio AI chat; question and total float out |
| last 4 s | **End card** | Logo, «Weniger Papierkram. Mehr Kopf für das, was zählt.», «Im App Store laden», «sortio.ch · Kostenlos starten» |

### 3.2 Other proven angles

- **Before / after.** «Bisher» line struck through in steel, then «Mit Sortio» with an ember check. Pairs: «IBAN abtippen» → «QR-Rechnung scannen», «Frist im Kalender suchen» → «Erinnerung am Vortag», «Ordner im Keller» → «Alles am Platz».
- **«Frag Sortio AI».** Hook is the question itself, big, as a bubble: «Welche Rechnungen sind diesen Monat noch offen?» Then the real chat screen (`chat-open-bills.webp`) and the answer total from that screen (CHF 3’168.25). Dark abyss band suits it. Sortio AI is a Pro feature: never call it free.
- **QR bill.** Hook «IBAN und Referenz abtippen war gestern.» Then `document-payment.webp` / `crops/payment.webp`: a tap opens the banking app. Never say Sortio pays the bill (it prepares the payment, you pay).
- **Cinematic mini-film (reel 12).** A person, an evening, a pile of post; one photo; a flash into the app; four words on four beats («Liest.» «Legt ab.» «Erinnert.» «Antwortet.»); relief; claim. See section 7.
- **CHF 0 zum Start.** Price hook with the real plan facts (`product-facts.md`, check sortio.ch the same day).
- **KMU.** «Die Administration deines Betriebs, im Griff.» Kreditoren, MWST, Treuhand; folder and invoice screens.
- **Swiss trust.** «In der Schweiz gespeichert.» with «AES-256 verschlüsselt · DE · FR · EN», only the wording in `product-facts.md`.

### 3.3 Hook patterns (first 1–2 seconds)

From Benjamin's research on explainer shorts that beat their channel's usual views (YouTube, Nov 2026): the topic alone never carries a video, the hook and the visual idea do.

1. **The pain or question as the first words and the first picture**, no preamble: «Briefe stapeln sich auf dem Tisch.» / «Welche Rechnungen sind noch offen?»
2. **A struck-through «before»** (Sortio's signature): the old way, crossed out on screen.
3. **A numbered promise**: «3 Dinge, die Sortio aus jedem Brief liest.»
4. **Myth or contrarian line**: «Papierkram ist Ordnungssache? Nein, Fotosache.» (keep it true and calm; no hype words, see `voice-and-copy.md`).
5. **A «see this» promise** paid off within 2 s: the pile lands, the letter flies into the phone.
6. **Shared confusion** as a question stack, for explainers: «Zahlbar bis? Referenz? Wohin damit?»

The first frame already shows the topic (pile, question, phone). No logo intro, no «Hallo, ich bin …». Test two or three hooks on the same body (Instagram Trial Reels) and compare skip rate and average watch time first, then shares and saves; raw views last.

## 4. Pacing

- **A visual change every 1.5–2.5 s** (4–6 per 10 s), mostly by *adding* something (a callout, a ring, a line) rather than hard cuts. First movement within the first second. Nothing static for more than 3 s (the template slowly pushes in on the phone to avoid it).
- **Readable text stays settled long enough**: about 0.5 s + 0.3 s per word *after* the whole line is in. A five-word headline needs ≈ 2 s; a beat of 3–4 s fits a two-line headline plus its callouts. HyperFrames `check` flags lines that leave too early (`line_unread`).
- **Cut on the music.** Reel 11 runs at 120 BPM with bars on odd seconds, so the groove drops at 3.0 s exactly when the letter lands in the scanner. Reel 12 runs at 96 BPM (one bar = 2.5 s) and puts one word on each bar.
- **Transitions**: an iOS-style push between app screens; a white flash for «the photo is taken»; the dark band rising for the end card. A plain crossfade between two busy layouts looks muddy: let the old content leave, then bring the new in.
- **End on a frame that resolves the hook** and can loop: the end card holds 2–3 s.

## 5. On-screen text and captions

- **Headlines**: Hedvig Letters Serif, two lines, the second line in ember for the punchline (template default 92 px on 1080 wide). Mono eyebrow above (`01 — Scannen`). Sentence case with a full stop. Tokens and sizes: `design-system.md`.
- **Callouts** repeat what the screen shows (Absender, Betrag, Fälligkeit) as complete white rounded cards with an ember-soft icon tile; never a one-sided accent stripe.
- **Subtitles for spoken reels**: burned in, Inter 600 at 40–48 px, **1–3 words per line, German often 1–2** (long compounds like «Krankenkassenprämie»), at most 2 lines and about 22–26 characters per chunk, centred in the lower part of the safe band (y ≈ 1050–1250). One key word or number per chunk may be ember. Ink on a white card on light scenes, white on dark scenes. Never in the bottom 35 %. `templates/explainer/tools/build_subtitles.py --max 22` makes these chunks from the word timings.
- **No text walls**: at most about 8 words on screen at once besides small labels.
- Swiss spelling (ss), amounts `CHF 412.30`, `CHF 3’168.25` (typographic apostrophe), dates `31.10.2026`.

## 6. Music and voice

### Music

- **Reels 11 and 12 use original soundtracks** synthesised in Python (numpy/scipy): music and sound effects written as one piece in one key, sharing one reverb, every effect on the picture's cue. No samples, no third-party music, so they are free to use in paid ads. The template ships the same approach: `templates/reels/tools/soundtrack.py` (F major, 120 BPM, paper thuds on the landing letters, a pen scratch on the strike-through, pops for the callouts, whooshes for the screen pushes, a bell for the reminder, a resolution and a ding on the end card).
- **Royalty-free or licensed music only.** Before using any track: the licence must cover *paid social media advertising* (not only organic posts) worldwide or at least in Switzerland, for the brand Sortio. Keep the licence certificate or receipt in the project folder (`music-licence.pdf`). Stock libraries with ad licences (e.g. Epidemic Sound, Artlist) are paid subscriptions.
- **Never** use commercial or «trending» songs, a track ripped from YouTube, or music from Instagram's or TikTok's in-app library in an ad: those licences cover organic posts inside that app only, and business accounts are often limited to the platform's own royalty-free collection.
- AI music (ElevenLabs Music, Higgsfield audio models) has its own terms per plan; read them before using it in an ad.
- Mix: effects sit under the music, nothing harsh or spiky; the whole reel at −14 LUFS. `tools/finalize.sh` measures and corrects it.

### Voice

- Most short reels work **without** voice (music + on-screen text). Add a voice-over for 30–60 s informative reels and explainers.
- Voice used by Benjamin: ElevenLabs **«Thomas: Credible Swiss Business Voice»** (Voice Library, Standard German), model `eleven_v4`, voice settings **stability 0.42, similarity 0.8, style 0.22**, delivered a little faster than recorded (×1.08–1.18; set `--speed` up to about 1.15 in the script, or speed up with ffmpeg `atempo`, which keeps the pitch). A calm female alternative with a Swiss accent: «Heidi factual» (stability 0.5, similarity 0.8, style 0.15). Setup and key handling: `tools-setup.md`; the script with word timings: `templates/explainer/tools/vo_elevenlabs.py`.
- Write numbers for the ear in a separate `say` field («vierhundertzwölf Franken dreissig»), keep the subtitles in figures («CHF 412.30»).
- AI voice = synthetic content: switch on the platform's AI label at upload.

## 7. How reels 11 and 12 were made (5 Oct 2026)

Both were built by Claude Code from the sortio.ch website project with Benjamin's «launch video» skill, which writes the whole video itself as an HTML page and renders it. Neither used HyperFrames' CLI; the template in this skill rebuilds the same look as a HyperFrames composition, which is easier to preview, check and edit.

### 7.1 Reel 11 «Sortio» (20 s, route A)

1. **Inspect.** Read the site's copy, colours, fonts and the real app screenshots (720×1565 WebP with sample data). Answer: what is it, for whom, what sets it apart, the visual hook, which real UI to show, the share caption.
2. **Plan** (`brag-plan.md`): format 1080×1920, 30 fps, 20 s; angle «one letter's journey»: the Helsana sample premium bill from the pile is scanned, read (Absender / Betrag / Fälligkeit), dropped into «Versicherungen», becomes the task «Prämienrechnung Oktober 2026» with a reminder, then Sortio AI totals the open October bills. Storyboard with times, on-screen text and sound per scene (the table in 3.1 is that storyboard).
3. **Prepare assets** (Python/PIL): cut the folder and task screenshots into tiles and rows, paint the band behind them with the row colour, so the tiles can animate in over an empty screen; crop the two sample letters from the review screens.
4. **Build** one HTML page at 1080×1920 where every frame is a pure function of time (`render(t)` sets every style): mask-reveal serif headlines, CSS envelopes with a fictitious sample address (Frau Laura Frei, Seestrasse 12, 8002 Zürich) and «P.P.» franking, the phone with real screens, callouts, a real screen recording of the Sortio AI chat (288 JPG frames drawn onto a canvas at varying speed), the dark band outro with the paper plane.
5. **Check stills** at every scene and mid-transition; fix overflow and collisions.
6. **Render** with Playwright (headless Chromium, 1080×1920, device scale 1): one screenshot per frame piped into ffmpeg (`libx264 -preset slow -crf 14 -pix_fmt yuv420p`, bt709 tags). The poster frame (5.2 s, callouts settled) is baked in as frame 0.
7. **Soundtrack** (`audio.py`, numpy/scipy): F major, 120 BPM, bars on odd seconds; hook on a filtered Dm9 pad with clock-like hats, letters landing on eighth notes, a pen scratch at the strike; the groove drops at 3.0 s; tap and shutter clicks, pops F5–A5–C6 for the three callouts, push whooshes, tile ticks, a low pluck when the letter lands in the folder, bell C6→F6 for the reminder, an arpeggio for the AI answer, B♭ swell → F resolution at 17 s, a ding on the CTA; sidechain breathing on the kick, one shared reverb, soft clip.
8. **Deliver**: `brag.mp4` (20.0 s, H.264 + AAC), `brag.jpg` cover, `share-copy.txt` caption (section 10).

### 7.2 Reel 12 «Cinematic» (22.5 s, route B)

Brief from Benjamin: «a cinematic one where someone uses Sortio». The project had no film footage, so Claude asked first (AI scenes with Higgsfield, or a free version from real screens only) and Benjamin chose Higgsfield.

1. **Cost check** before generating (Higgsfield connector, `get_cost`): Kling 3.0 pro 5 s 9:16 without sound 8.75 credits; Seedance 2.5 5 s 1080p without audio 60 credits; Cinema Studio Video 4.0 5 s 720p 35 credits. Kling 3.0 was chosen: calm shots with little camera motion, a fraction of the cost.
2. **Four start frames** with **GPT Image 2.5** (`gpt_image_2_5`), 9:16, quality high, resolution 2k (1520×2688), 2.75 credits each. Frames 1 and 2 from text only; frames 3 and 4 with frame 2 as the reference image, so it is the same woman in the same kitchen. Every prompt ends with «Absolutely no text, no logos, no readable writing anywhere».
3. **Four clips** with **Kling 3.0** (`kling3_0`), mode pro, 5 s, 9:16, sound off, each clip's start image = its still. Higgsfield once answered with a preset recommendation («IN THE DARK») instead of a job; the same request was sent again with that preset declined. Outputs were 1080×1912 at 24 fps, 5.04 s; they were scaled to 1084×1920, cropped to 1080×1920 and extracted at 30 fps.
4. **Sync**: the shutter blink in the scan clip was found by measuring the brightness of the phone screen per frame (≈ 2.85 s into the clip) and placed so the white flash into the app hits the downbeat at 7.5 s.
5. **Composition** (same HTML technique as reel 11): live-action shots with a dark scrim and serif lines («ZÜRICH · 21:47», «Jeden Monat.», «Derselbe Stapel.», «Foto machen.»); white flash; the app stage on the abyss band with the real screens in 3D and one huge serif word per bar («Liest.» «Legt ab.» «Erinnert.» «Antwortet.»); the relief shot with «Weniger Papierkram. / Mehr Kopf für das, was zählt.»; end card with logo, «Dein Verwaltungsassistent. Für Privat und Geschäft.», App Store pill, sortio.ch. Fine generated film grain over everything.
6. **Soundtrack** (`audio.py`, 96 BPM, bar 2.5 s): rain, a ticking clock and soft felt piano in D minor; the mail thud; a riser into the shutter; a big brass-like hit and sub boom at the flash; a driving pulse in F (F, Dm, B♭, C) under the app words with a hit per word; warm F major and the piano motif for the relief; final hit, plane whoosh and CTA ding. Gentle bus compression; muxed as AAC 256k at −14.7 LUFS, true peak −1.7 dBFS.
7. **Render** at 30 fps (675 frames), poster frame 16.5 s (she smiles, «Weniger Papierkram.»).
8. **Cost**: 46 credits (4 × 2.75 + 4 × 8.75), no re-rolls.
9. **Flags noted for ads**: the woman is AI-generated (Meta may show an «AI info» label; switch the AI label on); the Helsana sample letter appears in the app scenes.

**The prompts** (verbatim, reuse and adapt them):

> Still 1, mail: Cinematic film still, vertical 9:16, shot on ARRI Alexa with an anamorphic lens, fine 35mm film grain, very shallow depth of field. Night in a Zurich Altbau apartment kitchen. Low camera angle just above a dark oak kitchen table. A hand (cream knit sweater sleeve) is dropping a thick, messy stack of paper mail onto the table: plain white window envelopes and folded letters, a few envelopes already sliding and fanning out across the wood, frozen mid-motion, tiny dust particles glowing in the light. Key light: a warm tungsten table lamp from the left, pooling amber light on the paper. Background: a tall window with rain drops on the glass and soft blue bokeh city lights of Zurich at night. Teal-and-amber color grade, deep blacks, moody and premium, like a high-end film trailer. One small ember-orange accent (an orange pencil on the table). Absolutely no text, no logos, no readable writing anywhere; the paper shows only faint illegible grey lines.

> Still 2, the woman: Cinematic film still, vertical 9:16, shot on ARRI Alexa with an anamorphic lens, fine 35mm film grain, shallow depth of field. Night in a Zurich Altbau apartment kitchen. A woman in her early 30s (Swiss, shoulder-length dark-blonde hair, natural look, cream knit sweater) sits at a dark oak kitchen table, elbow on the table, fingertips at her forehead, looking down tiredly at a messy pile of paper letters and white window envelopes in front of her. Medium shot from the front-side, she is in the lower-middle of the frame, the upper third is calm darkness and window. Key light: warm tungsten table lamp from the left lighting her face and the paper; cool blue rim light from a tall rainy window behind her with soft bokeh city lights of Zurich. Teal-and-amber color grade, deep blacks, quiet, moody, premium film-trailer look. A white ceramic mug and an ember-orange pencil on the table. Absolutely no text, no logos, no readable writing anywhere; the paper shows only faint illegible grey lines.

> Still 3, the scan (reference: still 2): Cinematic film still, vertical 9:16, same woman, same kitchen and same night lighting as in the reference image (dark-blonde shoulder-length hair, cream knit sweater, dark oak table, warm tungsten lamp from the left, rainy window with Zurich night lights behind). Close-up from slightly above and behind her right shoulder: she holds an iPhone flat and steady above a single unfolded paper letter lying on the table, taking a photo of it. The phone screen shows the camera viewfinder framing the white letter and glows softly, lighting her fingers and the paper with a cool white light. Her face is partly visible in soft profile, focused and calm. Shallow depth of field, anamorphic lens, fine 35mm film grain, teal-and-amber grade, deep blacks, premium film-trailer look. Absolutely no text, no logos, no readable writing anywhere; the letter shows only faint illegible grey lines.

> Still 4, relief (reference: still 2): Cinematic film still, vertical 9:16, same woman, same kitchen and same night lighting as in the reference image (dark-blonde shoulder-length hair, cream knit sweater, dark oak table, warm tungsten lamp, tall rainy window with Zurich night lights and church spires). A little later: she leans back in her chair, relaxed and relieved, with a soft genuine smile, holding the white mug with both hands and looking out of the window at the city lights. On the table in front of her the letters are now one small, neat, tidy stack held by a paper clip, and her iPhone lies face down beside it; the ember-orange pencil lies parallel to the stack. Medium shot, she sits in the lower-middle of the frame, the upper third is the dark window with bokeh lights. Warmer grade than before, amber lamp light, soft blue window light, fine 35mm film grain, anamorphic lens, shallow depth of field, premium film-trailer look. Absolutely no text, no logos, no readable writing anywhere.

> Clip 1 (from still 1): Slow motion, cinematic: the hand lets go of the stack of envelopes, the letters drop onto the dark oak table and slide and fan out across the wood, settling gently. Dust particles glint in the warm lamp light, rain drops run down the window, the city lights in the background twinkle. Very slow camera push-in. Realistic paper physics, shallow depth of field, film grain. No text appears.

> Clip 2 (from still 2): Cinematic, subtle realistic motion: the woman exhales slowly, lowers her hand from her forehead and reaches for the top letter on the pile, picking it up and looking at it with a tired expression. Rain drops slide down the window, city lights twinkle softly. Very slow camera push-in toward her. Shallow depth of field, film grain. No text appears.

> Clip 3 (from still 3): Cinematic, realistic subtle motion: the woman holds the iPhone steady above the letter, adjusts it slightly to frame the page, then taps the shutter button with her thumb; the phone screen briefly flashes brighter, lighting her fingers and the paper. Rain drops slide down the window, city lights twinkle. Very slow camera push-in over her shoulder. Shallow depth of field, film grain. No text appears.

> Clip 4 (from still 4): Cinematic, subtle realistic motion: the woman smiles softly, takes a slow sip from the mug and keeps looking out of the window at the rainy city lights, relaxed and relieved. Rain drops slide down the glass, the city lights twinkle, steam rises gently from the mug. Very slow camera dolly back. Shallow depth of field, film grain. No text appears.

## 8. Real app screens versus AI video, and the honesty rule

**The rule: everything that shows the Sortio app is real.** Real screenshots from `assets/screens/` or real screen recordings, with the sample data they contain (marked MUSTER). AI may create people, rooms, light, paper and props, but never the app interface, a phone screen with app content, numbers, ratings, reviews, testimonials, awards or user counts. In reel 12 the AI phone only shows a camera viewfinder; every app scene is a real screenshot.

- **Numbers on screen** come from the sample screens (CHF 412.30, 31.10.2026, CHF 3’168.25) or from `product-facts.md`. No «spart 5 Stunden», «10’000 Nutzer», stars or quotes.
- **Third-party names** in the sample screens (Helsana, Swisscom, SBB, ewz, Serafe, AXA) are the app's sender recognition, not partners. For paid ads, decide with Benjamin whether to show them large.
- **Personal data**: only sample data. Never film or photograph your own or a client's real letters, names, addresses, IBANs or QR codes. The sample screens greet a demo user by first name («Salü Benjamin»); avoid zooming in on it.
- **AI people**: switch on the AI label at upload (Instagram/Meta «AI info», TikTok «AI-generated content», YouTube «altered or synthetic content»). Do not make an AI person look like a real, identifiable person.

**When to use which footage**

| Need | Use |
|---|---|
| Show what the app does | Real screenshots (template) or a real screen recording |
| Show a flow with typing, scrolling or a tap into another app | Screen recording: record on an iPhone with the sample-data demo account only (ask Benjamin for recordings or new screens; never your real documents), trim with ffmpeg, place as `<video muted playsinline>` inside the phone frame |
| A person, an emotion, a place (kitchen table, Zürich, an office) | AI stills and clips (Higgsfield), or licensed stock footage |
| A product shot of the phone in a hand | AI image of the hand and phone with a **blank or viewfinder screen**, then lay the real screenshot onto the screen in the composition |

**AI video with Higgsfield, the method**

1. Write the shot list first (4–5 shots of 5 s for a 20 s reel; most shots are used for 2–3 s).
2. **Check the cost** of every job before you submit it (`higgsfield generate cost …`, or ask Claude to call the connector's cost check). Say the number to yourself (or the client) before spending.
3. Make **start frames as stills** first (GPT Image 2.5, 9:16, high, 2k). Approve them by eye. For the same person in several shots, use the approved still as the reference image.
4. Animate each still (image-to-video):
   - **Kling 3.0** (`kling3_0`, mode pro, 5 s, sound off): calm single shots, slow push-ins, small gestures. ≈ 8.75 credits per 5 s (Oct 2026).
   - **Seedance 2.5** (`seedance_2_5`, mode `omni_reference` with the still as start image, 4–30 s, up to 1080p, `generate_audio` false): Higgsfield's default for complex motion, multi-shot or longer clips, and for keeping identity across a sequence. ≈ 60 credits per 5 s at 1080p (Oct 2026): use it when Kling cannot do the motion.
5. Prompt pattern: camera and lens, light, grade (Sortio: warm tungsten or soft daylight, one ember-orange prop), what moves and how slowly, «Very slow camera push-in», «Realistic paper physics», and always **«No text appears.»** (video) / «Absolutely no text, no logos, no readable writing anywhere» (stills). German letters on paper come out as gibberish: keep paper text illegible on purpose.
6. If Higgsfield suggests a preset instead of running the job, decline it and resubmit your own prompt.
7. Download every result immediately, keep the raw file, the prompt, model, settings and credits in a `prompts.md` next to the project. Never pay twice for the same job: if a download fails, find the finished job in the job list (`higgsfield generate list`).
8. In the composition: put each clip as a muted `<video>` with its own `data-start`/`data-duration` (HyperFrames converts 24 fps sources to 30 fps), a dark gradient scrim under the text, the serif lines on top, and keep the app scenes real.

CLI examples (check flags with `higgsfield model get <model>`):

```bash
higgsfield generate cost kling3_0 --prompt "slow push-in" --start-image ./still-2.png --duration 5 --mode pro --sound off --aspect_ratio 9:16
higgsfield generate create gpt_image_2_5 --prompt "…" --aspect_ratio 9:16 --quality high --resolution 2k --wait
higgsfield generate create gpt_image_2_5 --prompt "same woman … (reference image)" --image ./still-2.png --aspect_ratio 9:16 --quality high --resolution 2k --wait
higgsfield generate create kling3_0 --prompt "…" --start-image ./still-2.png --duration 5 --mode pro --sound off --aspect_ratio 9:16 --wait
higgsfield generate create seedance_2_5 --prompt "…" --mode omni_reference --start-image ./still-2.png --duration 5 --resolution 1080p --generate_audio false --aspect_ratio 9:16 --wait
```

## 9. QA gate before posting

Nothing is posted until every line is ticked. Keep the ticked list as `qa.md` next to the video.

**Facts (the fact-check gate).** Make a table of every claim spoken or shown: claim, source (quote from sortio.ch or `product-facts.md`, with the date read), status VERIFIED / CHANGED / CUT. Anything not verified is cut, not softened. Prices: check sortio.ch on the day of posting.

- [ ] Every claim VERIFIED; no invented numbers, ratings, testimonials, awards, user counts
- [ ] Pro features not presented as free; no «bezahlt automatisch», no compliance claims (`product-facts.md`, section 7)
- [ ] App UI is real; numbers on screen match the sample screen exactly; only sample data visible
- [ ] Swiss spelling (ss), «du», CHF formats, no emoji, no exclamation marks in headlines (`voice-and-copy.md`)

**Picture**
- [ ] `npx --yes hyperframes@0.9.70 check` → 0 errors; warnings read and understood
- [ ] All reading text inside the safe zone (y 290–1250 for Reels); nothing important under the caption area
- [ ] Every line readable at phone size, held long enough; frame 0 is a settled poster frame
- [ ] Watched in full on a phone, sound off (the captions carry the message) and sound on

**Sound**
- [ ] −14 LUFS ±1, true peak ≤ −1.5 dBTP (`tools/finalize.sh` prints both); no clipping, no harsh effects
- [ ] Music licence covers paid ads (or the original template soundtrack); licence file saved

**File**
- [ ] 1080×1920, 30 fps, H.264 + AAC, duration as planned, `+faststart`
- [ ] Cover JPG 1080×1920, headline inside the centre 3:4 area
- [ ] AI label decision made (AI people, AI voice, AI music → label on)
- [ ] Benjamin's OK for anything that runs as a paid ad

## 10. Posting copy

**Caption pattern** (`voice-and-copy.md` has the rules): one hook sentence (the situation) → one or two sentences on what Sortio does → CTA with «App Store» and/or «sortio.ch» → blank line → five hashtags, always `#Sortio`. 150–300 characters before the hashtags.

Reel 11, as posted in the kit:

```text
Foto machen, Sortio erledigt den Rest: Absender, Betrag und Frist erkannt, im richtigen Ordner abgelegt, rechtzeitig erinnert. Und wenn du wissen willst, was im Oktober noch offen ist, fragst du einfach. Jetzt im App Store, kostenlos starten auf sortio.ch.

#Sortio #Papierkram #Schweiz #Rechnungen #Admin
```

Reel 12:

```text
Jeden Monat derselbe Stapel. Foto machen, und Sortio liest, legt ab, erinnert dich an jede Frist und beantwortet deine Fragen. Kostenlos starten im App Store, sortio.ch.

#Sortio #Papierkram #Zürich #Schweiz #Rechnungen
```

(Both mention Sortio AI («fragst du einfach», «beantwortet deine Fragen») next to «kostenlos starten»: fine, because neither says the AI itself is free.)

**At upload**
- Instagram: cover = the cover JPG; audio name for the original soundtrack «Sortio · <Titel>»; share to feed on for the main reel; AI label on when AI people/voice/music are in it; alt text = one plain sentence of what the video shows. Use Trial Reels to test hooks with non-followers first.
- TikTok: same caption (TikTok allows longer; do not stuff hashtags), AI-generated content label when it applies.
- YouTube Shorts: title = the hook (≤ 60 characters), description = caption + `https://www.sortio.ch`, «altered or synthetic content» Yes when AI is in it, not made for kids, language German.
- Paid ads: link to the App Store URL in `product-facts.md`.

**Deliverables per video** (one folder, e.g. `2026-11-20-qr-rechnung/`): `<slug>-9x16.mp4`, `<slug>-cover.jpg`, `<slug>-caption.txt`, `qa.md` (with the fact table), `prompts.md` (AI jobs and credits, if any), the project source (template copy). Benjamin's practice: a posting list in which every entry stays `approved: false` until he has said yes to that exact file and caption.
