"""Voice-over for an explainer: one ElevenLabs request per line of lines.json (with the lines before and after as
context, so the delivery flows), assembled with the script's pauses into vo/voice.wav plus word timings in
vo/words.json. Every line is cached in vo/cache/ by text, voice, model and settings, so a re-run only pays for the
lines you changed.

usage:
  python3 tools/vo_elevenlabs.py --voice <voice_id>             real voice (needs ELEVENLABS_API_KEY)
  python3 tools/vo_elevenlabs.py --draft                         free placeholder: silence with estimated word times
  python3 tools/vo_elevenlabs.py --voice <id> --only 3,4         re-record lines 3 and 4 only (then run again without --only)
options: --model eleven_v4 | eleven_multilingual_v2 | ...   --lang de   --speed 1.0   --stability 0.45
         --similarity 0.8   --style 0.2   --lead 0.6   --format mp3_44100_128   --wps 2.3 (draft speaking rate)

The key is read from the environment variable ELEVENLABS_API_KEY, or from a .env file in the project folder
(line: ELEVENLABS_API_KEY=...). It is never printed or written anywhere. Never commit .env.
Characters count against your ElevenLabs plan; the script prints how many it sends.

needs: python3 -m pip install numpy soundfile      and ffmpeg on the PATH

lines.json format, one object per spoken line (see the sample in this template):
  {"scene": "s2", "text": "Sortio liest den Betrag.", "say": null, "pause": 0.4, "chapter": "Scannen"}
  text    what the subtitles show (and what is spoken unless "say" is set)
  say     optional spoken version, e.g. "CHF 412.30" -> "vierhundertzwölf Franken dreissig"
  pause   silence after the line in seconds
  scene   id of the scene in scenes.js that this line belongs to
  chapter optional YouTube chapter title, set on the first line of a chapter
"""
import argparse, base64, hashlib, json, os, subprocess, sys, time, urllib.error, urllib.request
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID", ""))
ap.add_argument("--model", default="eleven_v4")
ap.add_argument("--lang", default="de")
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--stability", type=float, default=0.45)
ap.add_argument("--similarity", type=float, default=0.8)
ap.add_argument("--style", type=float, default=0.2)
ap.add_argument("--lead", type=float, default=0.6, help="silence before the first line")
ap.add_argument("--format", default="mp3_44100_128")
ap.add_argument("--only", default="")
ap.add_argument("--draft", action="store_true")
ap.add_argument("--wps", type=float, default=2.3, help="draft only: spoken words per second")
ap.add_argument("--project", default=".")
A = ap.parse_args()

P = os.path.abspath(A.project)
LINES = json.load(open(os.path.join(P, "lines.json"), encoding="utf-8"))
VO = os.path.join(P, "vo"); CACHE = os.path.join(VO, "cache")
os.makedirs(CACHE, exist_ok=True)
SR = 48000


def api_key():
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    env = os.path.join(P, ".env")
    if not k and os.path.isfile(env):
        for row in open(env, encoding="utf-8"):
            if row.strip().startswith("ELEVENLABS_API_KEY="):
                k = row.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("No ELEVENLABS_API_KEY: put it in .env in the project folder (see .env.example) or export it.")
    return k


def spoken(i):
    return (LINES[i].get("say") or LINES[i]["text"]).strip()


def request(i, key):
    text = spoken(i)
    settings = {"stability": A.stability, "similarity_boost": A.similarity, "style": A.style, "speed": A.speed,
                "use_speaker_boost": True}
    tag = hashlib.sha1(json.dumps([text, A.voice, A.model, settings, A.lang, A.format]).encode()).hexdigest()[:12]
    mp3, js = f"{CACHE}/{i:02d}.mp3", f"{CACHE}/{i:02d}.json"
    if os.path.exists(js) and json.load(open(js)).get("tag") == tag:
        return 0
    body = {"text": text, "model_id": A.model, "voice_settings": settings,
            "previous_text": spoken(i - 1) if i else None,
            "next_text": spoken(i + 1) if i + 1 < len(LINES) else None}
    if not A.model.startswith("eleven_multilingual"):        # multilingual v2 does not accept language_code
        body["language_code"] = A.lang
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{A.voice}/with-timestamps?output_format={A.format}"
    for attempt in range(6):
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"xi-api-key": key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=180)); break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 5:
                time.sleep(5 * (attempt + 1)); continue
            sys.exit(f"line {i}: ElevenLabs HTTP {e.code}: {msg}")
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    al = r.get("alignment") or r["normalized_alignment"]
    json.dump({"tag": tag, "spoken": text, "chars": al["characters"], "starts": al["character_start_times_seconds"],
               "ends": al["character_end_times_seconds"]}, open(js, "w"))
    print(f"line {i:02d} recorded ({len(text)} characters)")
    return len(text)


def decode(mp3):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def word_spans(meta):
    """(start, end) of every spoken word, from the character alignment."""
    spans, cur = [], None
    for c, s, e in zip(meta["chars"], meta["starts"], meta["ends"]):
        if c.isspace():
            if cur: spans.append(cur); cur = None
        else:
            cur = [cur[0], e] if cur else [s, e]
    if cur: spans.append(cur)
    return spans


def draft_line(i):
    """Placeholder: silence as long as the line would take, words spread by length."""
    words = spoken(i).split()
    dur = max(0.8, len(words) / A.wps)
    tot = sum(len(w) for w in words); acc, spans = 0, []
    for w in words:
        spans.append([dur * acc / tot, dur * (acc + len(w)) / tot]); acc += len(w)
    return np.zeros(int(dur * SR), np.float32), spans


if A.draft:
    print("draft mode: no voice is recorded; timings are estimates at", A.wps, "words per second")
else:
    if not A.voice:
        sys.exit("Pass --voice <voice_id> (or set ELEVENLABS_VOICE_ID). See references/explainer-videos.md, Voice.")
    key = api_key()
    only = {int(x) for x in A.only.split(",") if x.strip()} if A.only else set(range(len(LINES)))
    sent = sum(request(i, key) for i in sorted(only))
    print(f"{sent} characters sent to ElevenLabs" if sent else "all lines from cache, nothing sent")
    if A.only:
        sys.exit(0)

audio, words, lines, t = [np.zeros(int(A.lead * SR), np.float32)], [], [], A.lead
for i, row in enumerate(LINES):
    if A.draft:
        x, sp = draft_line(i); a0 = 0.0; seg = x
    else:
        meta = json.load(open(f"{CACHE}/{i:02d}.json")); x = decode(f"{CACHE}/{i:02d}.mp3")
        sp = word_spans(meta)
        a0, a1 = max(0.0, sp[0][0] - 0.06), min(len(x) / SR, sp[-1][1] + 0.12)   # trim to speech: 60 ms in, 120 ms tail
        seg = x[int(a0 * SR):int(a1 * SR)].copy(); f = int(0.008 * SR)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    disp = row["text"].split()
    if len(disp) == len(sp):                                  # shown words map 1:1 onto spoken words
        ws = [(w, s - a0, e - a0) for w, (s, e) in zip(disp, sp)]
    else:                                                     # "say" changed the word count: spread by length
        tot = sum(len(w) for w in disp); s0, s1 = sp[0][0] - a0, sp[-1][1] - a0; acc, ws = 0, []
        for w in disp:
            ws.append((w, s0 + (s1 - s0) * acc / tot, s0 + (s1 - s0) * (acc + len(w)) / tot)); acc += len(w)
    for w, s, e in ws:
        words.append([w, round(t + s, 3), round(t + e, 3), i])
    lines.append([round(t + ws[0][1], 3), round(t + ws[-1][2], 3), row["text"], row.get("scene", ""), row.get("chapter")])
    audio.append(seg); t += len(seg) / SR
    gap = float(row.get("pause", 0.4))
    audio.append(np.zeros(int(gap * SR), np.float32)); t += gap

y = np.concatenate(audio)
peak = float(np.max(np.abs(y))) or 1.0
sf.write(os.path.join(VO, "voice.wav"), (y / peak * 0.89 if peak > 1e-6 else y).astype(np.float32), SR, subtype="PCM_24")
json.dump({"dur": round(len(y) / SR, 3), "draft": A.draft, "words": words, "lines": lines},
          open(os.path.join(VO, "words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"wrote vo/voice.wav and vo/words.json ({len(y) / SR:.1f} s, {len(lines)} lines, {len(words)} words)")
