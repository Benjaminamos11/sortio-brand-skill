---
name: sortio-brand
description: "Sortio brand and content studio. The full Sortio design system (sortio.ch and the Sortio iPhone app: colors, fonts, logo, real app screens, layout, safe zones), the brand voice in Swiss High German, verified product facts and prices, and step-by-step workflows with templates for Instagram/TikTok/LinkedIn feed posts, stories, carousels, AI pictures (Higgsfield), reels and short video ads (HyperFrames, ffmpeg, ElevenLabs) and 60-180 s explainer videos. Use whenever the user asks for anything for Sortio or sortio.ch: a post, story, carousel, ad, picture, image prompt, reel, TikTok, video, explainer, caption, hashtags, script, voice-over, thumbnail, content plan, or a design that must look like Sortio."
---

# Sortio brand and content studio

Sortio («Dein Verwaltungs-Assistent für Privat und Geschäft») is a Swiss iPhone app: photograph a letter, Sortio reads it, files it in the right folder, prepares QR bills for payment, reminds you of every deadline and answers questions about your documents (Sortio AI). Website: https://www.sortio.ch

This skill makes content that looks, sounds and fact-checks like Sortio. All paths below are relative to this skill folder.

## Always, before you make anything

1. Read `references/design-system.md` sections 1 and 2 (hard rules, colors) and `references/voice-and-copy.md`. They are short and every job needs them.
2. Read `references/product-facts.md` before writing any claim, price or feature. If the post mentions a price, open https://www.sortio.ch/#preise and check it is still the same.
3. Then read only the workflow file for the job (table below).

## Pick the workflow

| The user wants | Read | Start from |
|---|---|---|
| Feed post, story, carousel, static ad, quote card | `references/pictures-and-posts.md` | `templates/posts/` (HTML/CSS + `render.py`) |
| AI picture, mood photo, background, Higgsfield prompt | `references/pictures-and-posts.md` (Set B: Higgsfield) | `assets/examples/posts/` for the look |
| Reel, TikTok, story video, short video ad (6-30 s) | `references/reels-and-social-video.md` | `python3 templates/reels/tools/new_reel.py <new folder>` |
| Explainer video (60-180 s, voice-over, subtitles) | `references/explainer-videos.md` | `python3 templates/explainer/tools/new_explainer.py <new folder>` |
| Caption, hashtags, headline ideas, content plan | `references/voice-and-copy.md` + `references/product-facts.md` | approved lines in `voice-and-copy.md` |
| Install tools, API keys, "what do I need" | `references/tools-setup.md` | |

## The look in ten lines (details in `references/design-system.md`)

- Swiss editorial: warm white canvas `#faf9f6`, near-black ink `#0a0b0d`, one accent: ember `#ff4f00`. Dark surface: abyss `#000710`.
- Headlines: Hedvig Letters Serif 400, sentence case, full stop at the end, tight tracking. Second line in graphite `#5d6169` (or ember for the punchline).
- Text: Inter. Eyebrows, amounts, prices: JetBrains Mono. Fonts are in `assets/fonts/` (OFL).
- Real app screens in a phone frame, from `assets/screens/` only. Never invent UI.
- One accent per layout. Never a second bright color.
- Never an accent stripe on one side of a box (no `border-left` callouts). Full rounded cards with soft shadows or a tinted panel instead.
- Never pause/play/stop buttons on auto-moving elements.
- Logo files in `assets/logo/`. Do not recolor or redraw the mark.
- Formats: feed 1080×1350, story/reel 1080×1920 (keep text and CTAs between y 250 and y 1580), square 1080×1080.
- CSS tokens to paste: `references/design-system.md` section 12, or link `templates/posts/ads.css`.

## The voice in five lines (details in `references/voice-and-copy.md`)

- Swiss High German, «du», calm and concrete. «ss», never «ß».
- CHF with the Swiss apostrophe: `CHF 3’168.25`. Prices as `CHF 10.– / Monat`.
- CTAs: «Gratis starten» or «Im App Store laden»; «Im App Store testen» for the 7-day trial.
- Name things as the app does: Sortio AI, QR-Rechnung, Fristen, Ordner.
- One idea per post. Show the feature, do not hype it.

## Honesty rules (never break)

- Only real app screens; amounts and letters come from the sample data (marked MUSTER).
- No invented numbers, user counts, ratings, reviews, testimonials, awards, «Nr. 1», speed or time-saved claims.
- No compliance or security claims beyond the site wording («Daten in der Schweiz», «AES-256 verschlüsselt»).
- No Android availability, no unlisted languages, no prices or discounts beyond `references/product-facts.md` section 3. Pro is CHF 10.– a month or CHF 79.– a year; the 7-day free trial belongs to the yearly plan only and always comes with «Danach CHF 79.– im Jahr. Vor Ablauf im App Store kündbar.». No savings claims. The full list is in `references/product-facts.md` section 7.
- When unsure whether a claim is allowed, leave it out and tell the user.

## Working with files

- Write each new piece in its own folder outside this skill folder (for example `~/Sortio-Content/2026-12-qr-rechnung/`).
- **Videos: always start with the copy script** (`new_reel.py` or `new_explainer.py`). HyperFrames refuses files above the project folder, so the templates cannot be rendered where they sit; the script copies the template, copies the screens, logo and fonts it uses and rewrites the paths. Then edit `reel-config.js` (reel) or `lines.json` + `scenes.js` (explainer), and run `npx --yes hyperframes@0.9.70 check` before `render`.
- Posts: copy the closest template under a new name inside `templates/posts/` (the templates reference `../../assets/`), render it with `python3 render.py <file> --out <your content folder>`, then move your HTML source to that content folder too, so the skill folder stays clean for updates.
- Render, then look at the result yourself (open the PNG, or extract 3-4 frames of a video with ffmpeg) before you hand it over. Fix what you see.
- Never write API keys into files you share. Keys live in a local `.env` (`ELEVENLABS_API_KEY`, Higgsfield login) that stays on the user's machine.
- In claude.ai (no local tools) you can still design posts as HTML, write copy, scripts and prompts; say clearly that rendering video needs Claude Code (see `references/tools-setup.md`).

## QA gate before you hand anything over

1. Spelling: Swiss German, no «ß», no English leftovers in German copy.
2. Facts: every feature and price matches `references/product-facts.md` (and the live site for prices).
3. Screens: real, sample data only, nothing personal visible.
4. Layout: safe zones respected, one accent, logo clear space, no one-sided stripe.
5. Size and format: exact pixel size, file type, for video also length, fps, loudness and burned-in subtitles as the workflow file says.
6. Deliver: the file(s), the caption text, hashtags and a one-line note of what was checked.
