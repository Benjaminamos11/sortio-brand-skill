"""Subtitles and caption data from the word timings in vo/words.json.

writes  vo/subtitles.srt   sentence cues (at most 42 characters per line) to upload to YouTube / Instagram
        vo-data.js         window.VO (word and line times) and window.CAPS (burned-in caption chunks) for index.html
        vo/chapters.txt    YouTube chapters from the "chapter" fields in lines.json
and sets data-duration on #root and <audio id="mix"> in index.html to the voice length plus --tail.

usage:  python3 tools/build_subtitles.py [--max 32] [--tail 3.0]
        --max   characters per burned-in caption chunk: 32 for 16:9, 22 for 9:16 (German needs short chunks)
        --tail  seconds after the last word (the end card)

Caption rules (strongest first): a chunk never exceeds --max (a single longer word may); a number stays with its unit
and «CHF» with its amount; break after a sentence end, colon or comma, else before a conjunction, preposition or
article; no chunk ends on «und», «die», «mit»...; no one-word last chunk; chunk lengths are balanced.
Numbers (with their unit) and the words in a line's "keys" list are marked as key words (ember in the video).
"""
import argparse, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--max", type=int, default=32)
ap.add_argument("--tail", type=float, default=3.0)
ap.add_argument("--project", default=".")
A = ap.parse_args()
P = os.path.abspath(A.project)
V = json.load(open(os.path.join(P, "vo", "words.json"), encoding="utf-8"))
LINES = json.load(open(os.path.join(P, "lines.json"), encoding="utf-8"))

WEAK = set("""und oder aber denn sondern dass wenn weil ob als wie mit im in ins auf für von vom zu zum zur an am bei
beim aus nach über unter vor durch ohne um der die das dem den des ein eine einen einem einer eines dein deine deinen
deinem deiner sein seine ihr ihre derselbe dieselbe dasselbe diese dieser dieses jeden jede jeder
and or but the a an of to in on for with at by from your""".split())
UNITS = set("""franken chf % prozent tag tage tagen woche wochen monat monate monaten jahr jahre jahren scans scan
sekunden minuten stunden dokumente dokument briefe brief rechnungen seiten seite""".split())
NUM = re.compile(r"^[\d'’.,:–-]*\d[\d'’.,:–-]*$")
bare = lambda w: re.sub(r"[^\wäöüÄÖÜàéèç%'’.-]", "", w).strip(".").lower()


def tokens(ws):
    """Glue «CHF» + amount and number + unit into one token, so a chunk never splits them."""
    out = []
    for w in ws:
        if out and (bare(out[-1][-1][0]) == "chf" or (NUM.match(bare(out[-1][-1][0]) or "x") and bare(w[0]) in UNITS)):
            out[-1].append(w)
        else:
            out.append([w])
    return out


def text(tok):
    return " ".join(w[0] for t in tok for w in t)


def cost(chunk, is_last, n_chunks):
    s = text(chunk); L = len(s)
    if L > A.max and len(chunk) > 1:
        return 1e9
    c = (A.max - L) ** 2 * 0.15
    end = chunk[-1][-1][0]
    if end[-1] in ".?!:;,":
        c -= 40
    elif bare(end) in WEAK:
        c += 400
    if is_last and len(chunk) == 1 and n_chunks > 0 and len(s) < 12:
        c += 300
    return c


def chunk_line(ws):
    toks = tokens(ws); n = len(toks)
    best = [0.0] + [1e18] * n; prev = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 12), j):
            c = best[i] + cost(toks[i:j], j == n, i)
            if c < best[j]:
                best[j], prev[j] = c, i
    cuts, j = [], n
    while j > 0:
        cuts.append((prev[j], j)); j = prev[j]
    return [toks[a:b] for a, b in reversed(cuts)]


# ---- burned-in caption chunks
caps = []
for li, (a, b, txt, scene, chapter) in enumerate(V["lines"]):
    ws = [w for w in V["words"] if w[3] == li]
    keys = [k.lower() for k in LINES[li].get("keys", [])]
    for ch in chunk_line(ws):
        flat = [w for t in ch for w in t]
        html = []
        for t in ch:
            s = " ".join(w[0] for w in t)
            is_key = any(NUM.match(bare(w[0]) or "x") for w in t) or any(k in s.lower() for k in keys)
            html.append(f'<span class="k">{s}</span>' if is_key else s)
        caps.append({"s": flat[0][1], "e": flat[-1][2], "text": text(ch), "html": " ".join(html), "line": li, "scene": scene})
for i, c in enumerate(caps):            # hold a chunk until the next one starts when the gap is short, else 0.4 s
    nxt = caps[i + 1]["s"] if i + 1 < len(caps) else c["e"] + 1.0
    c["e"] = round(nxt - 0.04 if nxt - c["e"] < 0.8 else min(c["e"] + 0.4, nxt - 0.04), 3)

# ---- SRT: one cue per sentence, split at the comma nearest the middle when longer than 42 characters
MAXSRT = 42
def srt_split(ws):
    t = " ".join(w[0] for w in ws)
    if len(t) <= MAXSRT or len(ws) < 2:
        return [ws]
    mid = len(t) / 2
    cand = [(abs(len(" ".join(w[0] for w in ws[:i])) - mid) - (12 if ws[i - 1][0][-1] in ",;:" else 0), i) for i in range(1, len(ws))]
    i = min(cand)[1]
    return srt_split(ws[:i]) + srt_split(ws[i:])

cues = []
for li in range(len(V["lines"])):
    ws, sent = [w for w in V["words"] if w[3] == li], []
    for w in ws:
        sent.append(w)
        if w[0][-1] in ".?!:" or w is ws[-1]:
            cues += [[p[0][1], p[-1][2], " ".join(x[0] for x in p)] for p in srt_split(sent)]; sent = []
for i, c in enumerate(cues):
    c[1] = min(c[1] + 0.3, cues[i + 1][0] - 0.05) if i + 1 < len(cues) else c[1] + 0.6
ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}".replace(".", ",")
open(os.path.join(P, "vo", "subtitles.srt"), "w", encoding="utf-8").write(
    "\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues)))

# ---- chapters for the YouTube description (the first chapter must start at 0:00)
chap = [(0.0 if not k else ln[0], ln[4]) for k, ln in enumerate(l for l in V["lines"] if l[4])]
mmss = lambda x: f"{int(x // 60)}:{int(x % 60):02d}"
open(os.path.join(P, "vo", "chapters.txt"), "w", encoding="utf-8").write("\n".join(f"{mmss(a)} {t}" for a, t in chap) + "\n")

# ---- data for the composition, and its length
total = round(V["dur"] + A.tail, 2)
data = {"dur": V["dur"], "total": total, "draft": V.get("draft", False), "words": V["words"], "lines": V["lines"]}
open(os.path.join(P, "vo-data.js"), "w", encoding="utf-8").write(
    "window.VO = " + json.dumps(data, ensure_ascii=False) + ";\nwindow.CAPS = " + json.dumps(caps, ensure_ascii=False) + ";\n")
idx = os.path.join(P, "index.html")
if os.path.isfile(idx):
    h = open(idx, encoding="utf-8").read()
    h = re.sub(r'(<div id="root"[^>]*?data-duration=")[\d.]+(")', rf"\g<1>{total}\g<2>", h)
    h = re.sub(r'(<audio id="mix"[^>]*?data-duration=")[\d.]+(")', rf"\g<1>{total}\g<2>", h)
    open(idx, "w", encoding="utf-8").write(h)
print(f"{len(caps)} caption chunks (longest {max(len(c['text']) for c in caps)} chars), {len(cues)} SRT cues, "
      f"{len(chap)} chapters; video length {total} s written to index.html")
