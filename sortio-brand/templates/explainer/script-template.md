# Explainer script: <Titel>

Fill this in first, get it approved, then turn the «Voice» column into `lines.json` (one row per sentence or half sentence) and the «Picture» column into `scenes.js`.

- **Topic and promise (one sentence):** e.g. «Wie Sortio einen Brief liest, ablegt und dich an die Frist erinnert.»
- **Viewer:** Privat (Krankenkasse, Steuern, Mietzins) or KMU (Kreditoren, MWST, Treuhand). One per video.
- **Length:** 60–180 s. German voice-over runs at about **2.3 words per second** with pauses, so 60 s ≈ 130 words, 90 s ≈ 200 words, 180 s ≈ 400 words.
- **Format:** 16:9 1920×1080 for YouTube (default of this template); a 9:16 cut for Reels/Shorts needs its own layout (see `references/explainer-videos.md`).
- **Facts:** every claim must be in `references/product-facts.md`. Prices only after checking sortio.ch on the day. Amounts and documents on screen come from the sample screens (MUSTER).
- **Address:** «du», Swiss spelling (ss, never ß), CHF amounts written `CHF 412.30` / `CHF 3’168.25` in subtitles and spoken out in `say`.

## Beats

| # | Scene id | Time (approx.) | Beat | Voice (exact words) | Picture (what is on screen) | Cue words |
|---|---|---|---|---|---|---|
| 1 | s1 | 0–8 s | **Hook**: the pain in the first sentence, no logo intro | «Krankenkasse, Steuern, Mietzins: Jeden Monat landet derselbe Stapel Post auf dem Tisch.» | Title card «Jeden Monat derselbe Stapel.» | — |
| 2 | s1 | 8–10 s | **Promise** | «So bringt Sortio Ordnung hinein.» | same card | — |
| 3 | s2 | 10–28 s | **Step 1: Scannen** | «Du fotografierst einen Brief …» «Sortio liest, was wichtig ist: Absender, Betrag, Fälligkeit …» | Phone: scanner, then review screen; callouts Absender / Betrag / Fälligkeit | «Sortio», «Absender», «Betrag», «Fälligkeit» |
| 4 | s3 | 28–38 s | **Step 2: Ablegen** | «Dann legt Sortio den Brief im richtigen Ordner ab …» | Phone: folders, ring on «Versicherungen» | «Versicherungen» |
| 5 | s4 | 38–50 s | **Step 3: Erinnern** | «Aus jedem Brief entstehen Aufgaben …» | Phone: tasks, ring on the Helsana task, callout «1 Tag vor Frist erinnern» | «Aufgaben», «Vortag» |
| 6 | s5 | 50–62 s | **Step 4: Fragen** (Sortio AI, Pro) | «Und mit Sortio Pro fragst du Sortio AI …» | Phone: chat screen, callout «Total: CHF 3’168.25» | «Antwort» |
| 7 | s6 | 62–73 s | **Trust** | «Deine Unterlagen werden in der Schweiz gespeichert …» | Three cards: Daten in der Schweiz · AES-256 verschlüsselt · DE · FR · EN | «Schweiz», «AES-256», «Deutsch» |
| 8 | s7 | 73–83 s | **Close + CTA** | «Sortio. Weniger Papierkram, mehr Kopf für das, was zählt. Kostenlos starten, im App Store.» | End card on the dark band: logo, claim, «Im App Store laden», sortio.ch | — |

Rules for the beats:
- One idea per beat. A new picture (screen push, callout, ring, card) at least every 3–5 s; in the first 10 s every 1.5–2.5 s.
- The hook answers «why should I keep watching?» within the first sentence. No «Hallo, ich bin …», no logo sting first.
- Show the real app for every feature claim. If no screen exists for a claim, cut the claim or record a new screen with sample data.
- End with one call to action only («Kostenlos starten» or «Im App Store laden»), never three.

## YouTube text (fill in after the voice is final)

- **Title** (≤ 60 characters, the promise, no clickbait): e.g. «Sortio erklärt: Post scannen, ablegen, nie mehr eine Frist verpassen»
- **Description:** two sentences on what the video shows, then the link `https://www.sortio.ch`, then the chapters from `vo/chapters.txt` (first one at 0:00), then 3–5 hashtags.
- **Subtitles:** upload `vo/subtitles.srt` (language: German (Switzerland) or German).
- **Thumbnail:** `renders/thumbnail.jpg` from `thumb.html` (1280×720, at most 4 words a line).
- **Altered or synthetic content:** «Yes» when the voice is AI (ElevenLabs) or the video contains AI-generated people or scenes.

## Checklist before recording the real voice

- [ ] Every sentence checked against `references/product-facts.md` (and sortio.ch for prices)
- [ ] Numbers and abbreviations have a `say` version (CHF, dates, AES-256, IBAN)
- [ ] Draft render watched once with the draft voice (`--draft`), timing feels right
- [ ] Benjamin (or the client contact) approved the script
