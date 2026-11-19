# Tools setup: what to install, what to sign up for, what it costs

Everything here runs on your own computer with your own accounts. Nothing in this repo contains keys or logins, and nothing should ever be added: keys go into a local `.env` file that is never committed or shared.

Legend: **FREE** = no cost · **PAID** = needs a paid plan or credits · **OPTIONAL** = only for some jobs.

## 1. What you need for which job

| Job | Claude | Local tools | Accounts |
|---|---|---|---|
| Copy, captions, scripts, picture prompts | claude.ai or Claude Code | none | — |
| Static posts and stories (`templates/posts/`) | Claude Code (or render by hand, see `pictures-and-posts.md`) | Python + Playwright | — |
| AI pictures and AI video clips | claude.ai or Claude Code | Higgsfield CLI or connector | Higgsfield (**PAID**, credits) |
| Reels from the template (`templates/reels/`) | **Claude Code** | Node 22+, ffmpeg, Python (numpy, scipy), HyperFrames | — |
| Explainers (`templates/explainer/`) | **Claude Code** | the reel tools + soundfile, Playwright | ElevenLabs (**PAID** for commercial use) |

**claude.ai versus Claude Code.** In claude.ai (web or the Chat tab of the desktop app) Claude can read this skill, write copy and scripts, design HTML, and call connectors (Higgsfield, the HyperFrames cloud connector). It cannot run ffmpeg, Node or a local HyperFrames render on your machine, so the reel and explainer templates in this skill need **Claude Code** (the Code tab of the Claude desktop app, or the `claude` terminal command). Recommended: do all video work in Claude Code.

## 2. Claude (PAID)

1. Install the Claude desktop app: macOS https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect · Windows https://claude.ai/api/desktop/win32/x64/setup/latest/redirect (docs: https://code.claude.com/docs/en/desktop).
2. Sign in and open the **Code** tab. Claude Code needs a paid Claude plan (Pro or Max) or a Claude Console account.
3. Install this skill: see the repo `README.md` (it goes to `~/.claude/skills/sortio-brand/`; local Claude Code sessions load skills from there).

## 3. Basics on the computer (FREE)

macOS with Homebrew is the easiest route. Install Homebrew from https://brew.sh (one command in Terminal), then:

```bash
brew install node ffmpeg python
node -v        # must be v22 or newer (HyperFrames needs Node 22+)
ffmpeg -version | head -1
python3 --version   # 3.9 or newer
```

Windows: install Node LTS from https://nodejs.org, ffmpeg with `winget install Gyan.FFmpeg`, Python from https://www.python.org. You can also simply ask Claude Code: «Install Node 22, ffmpeg and Python for me and check the versions.»

### Python packages (FREE)

Use a virtual environment, so nothing clashes with the system Python (Homebrew's Python refuses global installs):

```bash
python3 -m venv ~/.venvs/sortio
source ~/.venvs/sortio/bin/activate          # run this in every new terminal before the scripts
python3 -m pip install numpy scipy soundfile playwright
python3 -m playwright install chromium
```

What uses what: `numpy` + `scipy` → `templates/reels/tools/soundtrack.py`; `numpy` + `soundfile` → `templates/explainer/tools/vo_elevenlabs.py`; `playwright` → `templates/posts/render.py` and `templates/explainer/tools/thumbnail.py`.

## 4. HyperFrames (FREE, open source)

HyperFrames (by HeyGen, Apache-2.0, https://github.com/heygen-com/hyperframes) turns an HTML page with a seekable GSAP timeline into an MP4. The reel and explainer templates are HyperFrames compositions.

**The CLI needs no install.** It runs through `npx`, pinned to the version the templates were tested with:

```bash
npx --yes hyperframes@0.9.70 doctor     # checks Node, ffmpeg and the browser; the first run downloads a headless Chrome
npx --yes hyperframes@0.9.70 check      # lint + layout + contrast audit of index.html in the current folder
npx --yes hyperframes@0.9.70 preview    # opens HyperFrames Studio in the browser (timeline, scrubbing, edits)
npx --yes hyperframes@0.9.70 render --output renders/video.mp4
```

Newer versions usually work too (`npx --yes hyperframes@latest ...`); if something breaks after an update, go back to `@0.9.70`.

**The Claude Code plugin (recommended).** It teaches Claude the HyperFrames rules (`/hyperframes`). Run once in a terminal on the same machine (the desktop app uses the same install):

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

Then start a new Claude Code session. Update later with `claude plugin update hyperframes@hyperframes`. Without the plugin, the skills alone: `npx skills add heygen-com/hyperframes` (pick «Core Skills»).

**In claude.ai only:** HeyGen offers a HyperFrames connector (`https://mcp.heygen.com/mcp/hyperframes/`, needs a HeyGen account; credits and plan limits may apply). It renders in HeyGen's cloud, not from this skill's local templates, so it is a fallback for simple videos, not the main route.

## 5. ElevenLabs voice (PAID for commercial use)

Used for explainer voice-overs (and optionally reel voice-overs).

1. Sign up at https://elevenlabs.io. **The free plan has no commercial licence** (published content must credit ElevenLabs and may not be commercial), so Sortio videos need a **paid plan**; all paid plans include a commercial licence. Characters you generate count against the plan.
2. Create an API key: in the ElevenLabs app, open the developer settings (**API Keys**) and create a key. Restrict it to Text to Speech if the dialog offers it.
3. Put it in a `.env` file in your video project folder (the explainer template ships `.env.example`):
   ```
   ELEVENLABS_API_KEY=your-key-here
   ```
   `.env` is listed in `.gitignore`. Never paste the key into a file that is shared, a chat with other people, or a commit.
4. Pick a voice. Benjamin's explainers used **«Thomas: Credible Swiss Business Voice»** from the ElevenLabs **Voice Library** (Standard German, dry and calm). Add it to *My Voices* (Voice Library → search «Thomas Credible Swiss Business») and copy its voice ID from the voice's menu. Alternative with a Swiss accent: **«Heidi factual (Standard German – with Swiss Accent)»**. Library voices can be removed or changed by their creators: listen to a test line before every project, and read the voice's library page for its terms.
5. Model: `eleven_v4` (default in the script; supports German). Fallback: `eleven_multilingual_v2`.

## 6. Higgsfield AI pictures and video (PAID, credits)

Used for AI stills (GPT Image 2.5) and AI video clips (Kling 3.0, Seedance 2.5) — see `pictures-and-posts.md` and `reels-and-social-video.md`.

1. Account and plan at https://higgsfield.ai (credits are bought with a plan; check the price there).
2. Connect it to Claude, one of:
   - **claude.ai / desktop Chat:** Customize (or Settings) → Connectors → Add custom connector → URL `https://mcp.higgsfield.ai/mcp` → Connect, and authorise in the Higgsfield window. If Claude does not use it, start a new chat and mention Higgsfield by name.
   - **Claude Code:** `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`, then authorise when Claude Code asks (`/mcp` shows the status).
   - **Higgsfield CLI** (works well from Claude Code; https://github.com/higgsfield-ai/cli):
     ```bash
     brew install higgsfield-ai/tap/higgsfield     # or: npm install -g @higgsfield/cli
     higgsfield auth login                         # opens the browser once
     higgsfield account status
     ```
3. **Always check the cost before a video job** (the connector and CLI can report it, e.g. `get_cost` / `higgsfield generate cost ...`). Prices seen on 5 Oct 2026 (Ultra plan): GPT Image 2.5, high, 2k: 2.75 credits per image · Kling 3.0 pro, 5 s, 9:16, no sound: 8.75 credits · Seedance 2.5, 5 s, 1080p, no audio: 60 credits · Cinema Studio Video 4.0, 5 s, 720p: 35 credits. Reel 12 (4 stills + 4 clips) cost 46 credits.

## 7. Optional tools

- **Remotion** (React video framework, OPTIONAL; **PAID** for companies above 3 employees: free for individuals, non-profits and for-profit companies with up to 3 employees, otherwise a Company License, see https://github.com/remotion-dev/remotion/blob/main/LICENSE.md). Not needed for this skill's templates. New project: `npx create-video@latest --skills`; skills for Claude: `npx skills add remotion-dev/skills`.
- **HyperFrames desktop app** (OPTIONAL, FREE): `npx --yes hyperframes@0.9.70 open` offers it after a render; nice for hand edits on the timeline.
- **Music:** a royalty-free library with a licence that covers ads (for example Epidemic Sound or Artlist, **PAID** subscriptions), or the template's own synthesised soundtrack (FREE). See «Music» in `reels-and-social-video.md`.

## 8. Check that everything works

Ask Claude Code «Run the Sortio tools check» or run:

```bash
node -v && ffmpeg -version | head -1 && python3 -c "import numpy, scipy, soundfile, playwright; print('python ok')"
npx --yes hyperframes@0.9.70 doctor
cd ~/.claude/skills/sortio-brand/templates/reels && python3 tools/new_reel.py ~/Sortio-Videos/test-reel \
  && cd ~/Sortio-Videos/test-reel && npx --yes hyperframes@0.9.70 check && npx --yes hyperframes@0.9.70 render --output renders/test.mp4
higgsfield account status        # only if you use the CLI
```

The test reel renders in well under a minute and should look like `assets/examples/reels/template-preview.mp4`.
