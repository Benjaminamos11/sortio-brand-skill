# Sortio Brand & Content Skill

A Claude Skill that teaches Claude the full Sortio brand (the app that reads, files and reminds you about your paper mail, [sortio.ch](https://www.sortio.ch)) and how we make content for it: feed posts, stories, carousels, AI pictures, reels, short video ads and explainer videos.

Load it into your Claude once. After that, ask in plain words, for example:

- «Mach mir 3 Instagram-Posts für Sortio zum Thema QR-Rechnungen.»
- «Make a 15-second reel: letters pile up → scan → filed → reminder.»
- «Write and build a 90-second explainer: how Sortio AI answers questions about your documents.»
- «Give me a Higgsfield prompt for a story picture, kitchen table with a pile of letters, no text.»

Claude then uses the Sortio colors, fonts, logo, real app screens, voice and the rules below.

## What is inside

```
sortio-brand/                 ← the skill (this folder is what you install)
  SKILL.md                    ← entry point Claude reads first
  references/
    design-system.md          ← colors, fonts, logo, layout, safe zones, CSS tokens
    voice-and-copy.md         ← tone, Swiss German rules, approved headlines and CTAs
    product-facts.md          ← features, plans and prices, claims we never make
    pictures-and-posts.md     ← posts, stories, carousels, AI pictures (Higgsfield)
    reels-and-social-video.md ← reels, TikToks, story videos, short ads
    explainer-videos.md       ← 60–180 s explainers with voice-over and subtitles
    tools-setup.md            ← what to install, what costs money
  assets/                     ← logos, app screens (sample data), fonts, examples
  templates/
    posts/                    ← 6 HTML/CSS post templates + render.py (PNG/JPG at exact size)
    reels/                    ← 18 s reel (9:16, HyperFrames) + original soundtrack; start with tools/new_reel.py
    explainer/                ← 16:9 explainer (script, ElevenLabs voice-over, subtitles, thumbnail); start with tools/new_explainer.py
examples/                     ← bigger example videos (not part of the skill upload)
```

## Install

### Option A: Claude Code (Claude desktop app, Code tab) — recommended, can render videos

Open the Code tab, start a session and paste:

```text
Install the skill from https://github.com/Benjaminamos11/sortio-brand-skill: clone it and copy the folder sortio-brand to ~/.claude/skills/sortio-brand. Then read references/tools-setup.md and help me install what is missing.
```

Or in a terminal:

```bash
git clone https://github.com/Benjaminamos11/sortio-brand-skill.git && mkdir -p ~/.claude/skills && cp -R sortio-brand-skill/sortio-brand ~/.claude/skills/sortio-brand
```

To update later: `cd sortio-brand-skill && git pull` and copy the folder again.

### Option B: claude.ai (web or desktop chat) — posts, copy, picture prompts, scripts

1. Download `sortio-brand.zip` from the [latest release](https://github.com/Benjaminamos11/sortio-brand-skill/releases/latest).
2. In Claude: **Settings → Capabilities → Skills → Upload skill**, choose the zip.
3. Make sure «Code execution and file creation» is on.

In the chat version Claude can design posts, write copy, scripts and AI prompts. Rendering reels and explainer videos needs Option A (it runs ffmpeg, HyperFrames and Playwright on your computer).

## Accounts you may need (your own, never shared in this repo)

- **Higgsfield** for AI pictures and AI video clips (paid credits).
- **ElevenLabs** for voice-overs (paid plan for commercial use).
- Keys go into a local `.env` file on your computer. Never commit or paste them into files in this repo.

## Rules that always apply

- Show only the real Sortio app. Amounts and documents on screens come from sample data marked MUSTER.
- No invented numbers, ratings, awards, user counts or testimonials.
- Swiss High German: «ss», never «ß»; CHF amounts like `CHF 3’168.25`.
- Prices and plans: Pro CHF 10.– a month or CHF 79.– a year; the 7-day free trial is for the yearly plan only and always comes with «Danach CHF 79.– im Jahr. Vor Ablauf im App Store kündbar.». Check [sortio.ch](https://www.sortio.ch) and the App Store before publishing; `references/product-facts.md` has the details.

## Kurz auf Deutsch

Dieser Skill bringt deinem Claude das ganze Sortio-Design bei (Farben, Schriften, Logo, echte App-Screens, Tonalität) und wie wir Posts, Stories, KI-Bilder, Reels und Erklärvideos machen. Installieren: Option A (Claude Code, empfohlen, kann Videos rendern) oder Option B (claude.ai, Zip hochladen). Danach einfach sagen, was du brauchst, z. B. «Mach mir einen Reel über QR-Rechnungen».

Questions: ask Benjamin.
