# Explainer videos (60–180 s)

How to make a Sortio explainer from scratch: script, beats, voice-over, word-timed subtitles, a HyperFrames composition that moves on the spoken words, the mix, the render, the thumbnail and the YouTube/Instagram text. The method comes from Benjamin's explainer kit (used for his agency's YouTube explainers in October and November 2026), made generic and Sortio-branded. The working skeleton is `templates/explainer/` (its README is the command sheet). Short reels without voice: `reels-and-social-video.md`.

Brand rules live elsewhere and are not repeated: `design-system.md` (colours, fonts, logo, components), `voice-and-copy.md` (tone, CTAs, Swiss formats), `product-facts.md` (what Sortio does and may claim). Setup and costs: `tools-setup.md`.

---

## 1. The pipeline

```
script-template.md   beat sheet: what is said, what is shown, which word triggers what    (approve it)
        ↓
lines.json           the voice-over, one line per sentence: text, optional "say", pause, scene, chapter
        ↓
vo_elevenlabs.py     ElevenLabs, one request per line with the neighbouring lines as context
                     → vo/voice.wav + vo/words.json (start and end of every word)          (or --draft: free)
        ↓
build_subtitles.py   vo/subtitles.srt (upload) · vo/chapters.txt · vo-data.js (word times + caption chunks)
                     · the video length into index.html
        ↓
scenes.js + index.html   HyperFrames composition: scenes start on their first spoken line,
                     screens, callouts, rings and cards appear on cue words, captions burned in
        ↓
mix.sh               voice + optional ducked music bed → audio/mix.m4a at −14 LUFS
        ↓
hyperframes check → preview → render → finalize.sh → thumbnail.py → YouTube text
```

Everything is timed from the **voice**. Never animate to guessed times: record (or draft) the voice first, then the picture follows the words. That is what makes the video feel edited rather than assembled.

## 2. Script structure

**Length budget.** German voice-over runs at about **2.3 spoken words per second** including short pauses. 60 s ≈ 130 words, 90 s ≈ 200 words, 120 s ≈ 270 words, 180 s ≈ 400 words. 90–120 s is the sweet spot for one Sortio topic on YouTube; 60 s for a social cut.

**Shape** (the sample in `templates/explainer/lines.json`, 82 s):

| Part | Share | Sortio example |
|---|---|---|
| **Hook** (first sentence, 0–8 s) | 10 % | «Krankenkasse, Steuern, Mietzins: Jeden Monat landet derselbe Stapel Post auf dem Tisch.» The pain in the first words, the picture already showing it. No logo intro, no greeting. |
| **Promise** | 3 % | «So bringt Sortio Ordnung hinein.» |
| **3–5 steps**, one feature each, each with a real screen | 65 % | Scannen → Ablegen → Erinnern → Fragen (Sortio AI, Pro) |
| **Trust** | 10 % | «Deine Unterlagen werden in der Schweiz gespeichert, AES-256 verschlüsselt.» Only the wording in `product-facts.md`. |
| **Close + one CTA** | 10 % | «Sortio. Weniger Papierkram, mehr Kopf für das, was zählt. Kostenlos starten, im App Store.» |

Other good explainer topics: «QR-Rechnungen ohne Abtippen» (scan → IBAN/Referenz → banking app → bezahlt), «Frag deine Unterlagen» (Sortio AI: totals, finding receipts, drafting replies), «Steuererklärung vorbereiten» (export per year and category as PDF; never «erledigt deine Steuererklärung»), «Für KMU» (Kreditoren, MWST, Belege für die Treuhand), «Briefe auf Französisch» (DE/FR/EN reading).

**Writing for the ear**
- One idea per sentence; 8–16 words per sentence. Split long sentences into two lines in `lines.json`.
- Say the thing, then show it. Each step: what you do («Du fotografierst einen Brief»), what Sortio does («Sortio liest …»), the result on screen.
- Numbers, dates and abbreviations get a spoken form in `say`: `"text": "… CHF 412.30, zahlbar bis 31.10.2026."` / `"say": "… vierhundertzwölf Franken dreissig, zahlbar bis zum einunddreissigsten Oktober zwanzig sechsundzwanzig."` English product words (App Store, PDF, IBAN) are usually read correctly; listen and add a `say` when not.
- «du», Swiss spelling (ss), no hype, no exclamation marks.
- **Fact gate**: every claim in the script is in `product-facts.md` (prices: re-check sortio.ch the day you record). Pro features are named as Pro («mit Sortio Pro fragst du Sortio AI …»). Keep a claim table (claim · source · VERIFIED) next to the script; cut what you cannot verify.

## 3. Beats and cues

A **beat** is one picture idea tied to one moment in the voice. In `scenes.js` every scene lists its picture elements and the **cue word** that triggers each one: `"cue": [3, "Betrag"]` = the word «Betrag» in line 3 of `lines.json` (first line = 0). The composition looks the word up in `vo/words.json` and starts the element exactly when it is spoken. Change the voice and every cue moves with it.

Rules (from the kit and the research behind the reels):
- **A new picture every 3–5 s** (a screen push, a callout, a ring, a card), **every 1.5–2.5 s in the first 10 s**. Nothing static for more than about 5 s; the end card keeps a slow move.
- **Build up rather than cut away**: add the next callout to the screen that is already there. The viewer always sees progress.
- **Show the noun when it is said**: «Absender» appears with the Absender callout, «Versicherungen» rings the folder tile.
- A scene starts 0.35 s before its first line and ends where the next scene starts; headlines reveal at the start of the scene, so the eye has the frame before the voice explains it.
- One accent per frame (ember): the second headline line, the ring, a key word in the caption.

Scene types in the skeleton (`templates/explainer/scenes.js`):

| Type | Layout (1920×1080) | Elements |
|---|---|---|
| `title` | centred serif headline | eyebrow, 2 lines (second in ember) |
| `phone` | text column left (x 160–1060), phone right (x 1236–1692) | headline, screens (first at scene start, more on cues, iOS push), callouts on cues, a highlight ring with a soft veil on a cue |
| `points` | headline left, up to 3 cards in a row | icon + short text per card, each on its cue |
| `end` | dark abyss band, centred | origami mark, wordmark, claim, CTA pill, sortio.ch; captions off |

Consecutive `phone` scenes keep the phone on screen and push the next screen in, like navigating the app.

## 4. Voice-over

**Default: ElevenLabs** (`templates/explainer/tools/vo_elevenlabs.py`).

- **Voice**: «Thomas: Credible Swiss Business Voice» from the ElevenLabs Voice Library (Standard German, calm, credible; Benjamin's choice for his YouTube explainers, «dry»). Female alternative with a Swiss accent: «Heidi factual (Standard German – with Swiss Accent)». How to add a library voice and find its ID: `tools-setup.md`. Always listen to a test line before recording a whole project; library voices can change.
- **Model** `eleven_v4` (supports German; fallback `eleven_multilingual_v2`, which ignores `language_code`).
- **Settings used with Thomas**: stability **0.42**, similarity **0.8**, style **0.22**. Thomas speaks slowly; Benjamin sped his films up by **×1.08–1.18** (pitch-preserving). In the script use `--speed 1.1` (ElevenLabs speed, 0.7–1.2), or speed up the finished `vo/voice.wav` with `ffmpeg -i vo/voice.wav -af atempo=1.1 vo/voice-fast.wav` *before* `build_subtitles.py` (then re-run the timing: simplest is to use `--speed`).
- **How the script works**: one request per line, sent with the previous and next line as context (`previous_text`/`next_text`), so the intonation flows across lines; the `with-timestamps` endpoint returns the character timing, which the script turns into word timings; each line is trimmed to its speech (60 ms before, 120 ms after) and the script's own pauses are inserted, so you control the rhythm. Every line is cached by text, voice, model and settings: re-running only pays for changed lines.
- **Draft first** (`--draft`, free): silence with estimated word times at 2.3 words/s. Build and review the whole picture on the draft, then record the real voice once. A «DRAFT VOICE» badge marks draft renders.
- **Cost**: ElevenLabs counts characters of the spoken text; German runs at roughly 1’000 characters per minute of voice. The 82 s sample is about 1’100 characters.
- Commercial use needs a paid ElevenLabs plan. AI voice = synthetic content: declare it at upload.

**Alternative** (no ElevenLabs account): Benjamin's first explainer used Google Gemini TTS (voice «Charon», one request for the whole script) and got the word times by transcribing the result with faster-whisper. The skeleton does not include that route; ElevenLabs is simpler because it returns the timings itself.

## 5. Subtitles and burned-in captions

`templates/explainer/tools/build_subtitles.py` makes both from `vo/words.json`:

- **`vo/subtitles.srt`** for the platform's subtitle upload (YouTube: «Untertitel»; language German): one cue per sentence, split at the comma nearest the middle when longer than 42 characters, each cue held 0.3 s past its last word.
- **Burned-in caption chunks** (`window.CAPS` in `vo-data.js`), for viewers without sound and for social cuts. Rules, strongest first: never more than `--max` characters (32 for 16:9, **22 for 9:16**); «CHF» stays with its amount and a number with its unit; break after a sentence end, colon or comma, otherwise before a conjunction, preposition or article; never end a chunk on «und», «die», «mit» and the like; no one-word last chunk; balanced lengths. Numbers and the words in a line's `"keys"` are set in ember.
- Look: Inter 600, 42 px, ink on a white rounded card with a soft shadow (16:9: y 950, left-aligned in the text column on phone scenes, centred otherwise). On the dark end card captions are off (the claim is on screen anyway).
- **`vo/chapters.txt`**: YouTube chapters from the `"chapter"` fields (the first chapter is forced to 0:00). YouTube needs at least three chapters of at least 10 s each.

## 6. The HyperFrames composition

`templates/explainer/index.html` is a HyperFrames composition. The parts that matter when you change it (full rules: the HyperFrames plugin's `/hyperframes-core` skill):

- The root `<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="…">`; `build_subtitles.py` writes the duration (voice + 3 s end card) into it and into `<audio id="mix">`.
- **One paused GSAP timeline**, registered as `window.__timelines["main"]`. Every motion is a tween on it at an absolute time. No `Math.random`, no clocks, no network at render time; GSAP from the pinned CDN URL is the one exception the HyperFrames examples use.
- Every `<audio>` needs an `id` (otherwise the render is silent). Never put `crossorigin` on media. Animate children, not elements with `data-start`.
- **Fonts and images must be files inside the project.** The template points at the skill's `../../assets/` (fonts, logo, screens); `tools/new_explainer.py` copies what is used into the project and rewrites the paths, because HyperFrames refuses paths above the project folder.
- Type at least **28 px** on screen (HyperFrames checks it), contrast ≥ 4.5:1 for reading text (labels in graphite `#5d6169`, not steel, on white cards).

Loop while building:

```bash
npx --yes hyperframes@0.9.70 check                    # lint + runtime + layout + contrast; must say 0 errors
npx --yes hyperframes@0.9.70 snapshot --at 3,12,19,35 --no-end --output renders/stills   # stills to look at
npx --yes hyperframes@0.9.70 preview                  # Studio in the browser: scrub, play with sound, edit
```

Look at stills of every scene **and** of mid-transition moments before the full render. Typical fixes: a headline line too long (keep two lines of ≤ 20 characters at 96 px), a callout colliding with the captions (the column ends at y ≈ 900), a cue word not found (the page logs `cue not found …`; match the word in `text`, not in `say`).

**9:16 version for Reels/Shorts.** Do not crop the 16:9 render. Either make a 30–60 s cut with `templates/reels/` (same screens and headlines, the voice lines of one step) or adapt the explainer layout to 1080×1920: phone centred below the headline (y ≥ 290), callouts over the phone, captions with `--max 22` at y ≈ 1100–1250, everything readable inside y 290–1250 (see `reels-and-social-video.md`, Format specs).

## 7. Mix

`templates/explainer/tools/mix.sh [music file]`:

- Voice alone, or voice plus a music bed: the music is looped or cut to length, lowered by 20 dB, ducked further under the voice with a sidechain compressor, faded in over 1.5 s and out over 2.5 s.
- **Two-pass loudness normalisation to −14 LUFS integrated, true peak −1.5 dBTP** (the level YouTube, Instagram and TikTok play at), AAC 192 kbps, 48 kHz → `audio/mix.m4a`, which `index.html` plays. (One of Benjamin's first explainers was mixed at −16 LUFS; his later YouTube versions use −14.)
- Music: royalty-free with a licence that covers the use (YouTube and paid ads), or none. The reel template's synthesised soundtrack is free to use but timed for an 18 s reel; for an explainer use a calm, steady bed without big hits.
- Optional sound effects (soft whoosh on screen pushes, a pop per callout) work well if they are quiet and in the background. Add them as extra `<audio id="sfx-…">` elements with `data-start` at the cue time, or mix them in before `mix.sh`.

## 8. Render

```bash
npx --yes hyperframes@0.9.70 render --output renders/explainer.mp4        # CRF 16, 30 fps
bash tools/finalize.sh renders/explainer.mp4 12                           # loudness check, poster frame from 12 s, cover JPG
```

The 82 s sample renders in about 22 s on a recent Mac (1920×1080, 30 fps, ≈ 5 MB). Check the result with `ffprobe` (duration = the root `data-duration`) and watch it once fully with sound.

**Motion blur (optional, 8× render time).** Benjamin's explainers were rendered at 240 fps and blended down to 30 fps, which gives fast moves a natural blur. Blend 4 of every 8 frames («half blur»):

```bash
npx --yes hyperframes@0.9.70 render --fps 240 --output renders/explainer-240.mp4
ffmpeg -i renders/explainer-240.mp4 -vf "tmix=frames=4,select='eq(mod(n\,8)\,1)',setpts=N/(30*TB)" -r 30 \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a copy renders/explainer-blur.mp4
```

## 9. Thumbnail, YouTube and Instagram text

- **Thumbnail**: `thumb.html` (1280×720): the promise in at most two serif lines (≤ 4 words each, second line ember), the real app screen in a phone, the lockup. `python3 tools/thumbnail.py` → `renders/thumbnail.jpg`. It must read at phone size: one idea, big type, no small text.
- **Title** (≤ 60 characters): the promise, plainly. «Sortio erklärt: Post scannen, ablegen, keine Frist verpassen».
- **Description**: two sentences on what the video shows → `https://www.sortio.ch` → the App Store link from `product-facts.md` → a blank line → the chapters from `vo/chapters.txt` → 3–5 hashtags (`#Sortio` first).
- **Subtitles**: upload `vo/subtitles.srt`.
- **Upload settings**: altered or synthetic content «Yes» for an AI voice or AI people; not made for kids; language German; no paid promotion unless it is an ad.
- **Instagram/LinkedIn cut**: the caption pattern of `reels-and-social-video.md`, section 10.

## 10. QA before publishing

Run the reel QA gate (`reels-and-social-video.md`, section 9) and in addition:

- [ ] The script's claim table is complete; every claim VERIFIED against `product-facts.md` / sortio.ch on the day
- [ ] Every voice line listened to: pronunciation of names, numbers, «Sortio», English words; no clipped words at line joins
- [ ] Captions in sync (spot-check five places) and identical to the voice (`text` vs `say` only differs in how numbers are spoken)
- [ ] No draft badge in the render (`DRAFT VOICE` means the voice was a placeholder)
- [ ] `finalize.sh` reports −14 LUFS ±1, true peak ≤ −1.5 dBTP
- [ ] Chapters start at 0:00, at least three, each ≥ 10 s; thumbnail readable at 25 % size
- [ ] Benjamin's OK on the final file, title and description
