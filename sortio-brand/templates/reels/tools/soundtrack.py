"""Original soundtrack for the Sortio reel template: music and sound effects written together (F major, 120 BPM, one
shared room), timed from reel-config.js so every hit lands on the picture. No samples, no third-party music: the
output is synthesised here from scratch, so it is free to use in ads.

usage:  python3 tools/soundtrack.py            (run inside the reel folder)
needs:  python3 -m pip install numpy scipy      and ffmpeg on the PATH
writes: audio/soundtrack.m4a (AAC 192k, 48 kHz stereo, normalised to -14 LUFS)

If you change the motion timing in index.html, change the matching cue times below (they mirror index.html)."""
import json, os, re, subprocess, sys, tempfile
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg_src = open(os.path.join(HERE, "reel-config.js"), encoding="utf-8").read()
R = json.loads(re.sub(r"^\s*window\.REEL\s*=\s*", "", cfg_src).rstrip().rstrip(";"))

SR = 48000
DUR = float(R["duration"])
N = int(SR * DUR)
rng = np.random.default_rng(7)
music, sfx, send = np.zeros((2, N)), np.zeros((2, N)), np.zeros((2, N))

# scene times, computed exactly as in index.html
HOOK_END = R["hook"]["duration"]
BEATS, t = [], HOOK_END
for b in R["beats"]:
    BEATS.append((t, b)); t += b["duration"]
END = t
if abs(END + R["end"]["duration"] - DUR) > 0.01:
    sys.exit(f"reel-config.js: scene durations add up to {END + R['end']['duration']} s, but duration is {DUR} s")


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def tvec(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def add(bus, t0, sig, gain=1.0, pan=0.0, rev=0.0):
    i0 = int(round(t0 * SR))
    if i0 >= N or i0 < 0: return
    sig = sig[: N - i0]
    l, r = np.cos((pan + 1) * np.pi / 4) * np.sqrt(2) * gain, np.sin((pan + 1) * np.pi / 4) * np.sqrt(2) * gain
    bus[0, i0:i0 + len(sig)] += sig * l; bus[1, i0:i0 + len(sig)] += sig * r
    if rev:
        send[0, i0:i0 + len(sig)] += sig * l * rev; send[1, i0:i0 + len(sig)] += sig * r * rev


# ---------------------------------------------------------------- instruments
def epiano(t0, m, dur, vel=1.0, gain=0.05, pan=0.0):
    f, tt = hz(m), tvec(dur + 0.9)
    y = np.sin(2 * np.pi * f * tt + 1.4 * np.exp(-tt * 7) * np.sin(2 * np.pi * f * tt))
    y += 0.18 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 14)
    y *= np.exp(-tt * 1.8) * np.clip(tt / 0.004, 0, 1) * np.clip(1 - (tt - dur) / 0.25, 0, 1)
    add(music, t0, y * vel, gain, pan=pan, rev=0.28)


def pad(notes, t0, t1, cut0, cut1, gain):
    tt = tvec(t1 - t0); n = len(tt); cutoff = np.linspace(cut0, cut1, n); out = np.zeros((2, n))
    for m in notes:
        for det, side in ((-0.07, 0), (0.07, 1), (0.0, None)):
            f, ph = hz(m + det), rng.uniform(0, 2 * np.pi)
            for h in range(1, 40):
                if f * h > 5000: break
                s = (1 / h) / (1 + (f * h / cutoff) ** 4) * np.sin(2 * np.pi * f * h * tt + ph * h)
                if side is None: out += s * 0.5
                else: out[side] += s
    out *= np.clip(tt / 0.35, 0, 1) * np.clip((t1 - t0 - tt) / 0.6, 0, 1) / (len(notes) * 6)
    out = np.stack([hp(out[c], 150) for c in range(2)])
    i0 = int(t0 * SR); n = min(n, N - i0)
    music[:, i0:i0 + n] += out[:, :n] * gain; send[:, i0:i0 + n] += out[:, :n] * gain * 0.35


def bass(t0, m, dur, vel=1.0):
    f, tt = hz(m), tvec(dur + 0.08)
    y = np.tanh(1.6 * (np.sin(2 * np.pi * f * tt) + 0.22 * np.sin(4 * np.pi * f * tt))) / np.tanh(1.6)
    y *= np.clip(tt / 0.004, 0, 1) * (0.7 + 0.3 * np.exp(-tt / 0.25)) * np.clip((dur + 0.07 - tt) / 0.07, 0, 1)
    add(music, t0, lp(y, 900) * vel, 0.2)


def kick(t0, vel=1.0):
    tt = tvec(0.45); f = 46 + 80 * np.exp(-tt * 30)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7.5) + 0.25 * lp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 220)
    add(music, t0, y * vel, 0.4)


def hat(t0, vel=1.0, pan=0.25):
    tt = tvec(0.06); add(music, t0, hp(rng.standard_normal(len(tt)), 7500) * np.exp(-tt * 70) * vel, 0.045, pan=pan, rev=0.08)


def pluck(t0, m, vel=1.0, pan=0.0, gain=0.07):
    f, tt = hz(m), tvec(0.5)
    y = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 8) + 0.3 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 34)) * np.clip(tt / 0.002, 0, 1)
    add(music, t0, y * vel, gain, pan=pan, rev=0.35)


def bell(t0, m, vel=1.0, pan=0.0, gain=0.1):
    f, tt = hz(m), tvec(1.6)
    y = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.4) + 0.45 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 3.5)
         + 0.25 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 6)) * np.clip(tt / 0.002, 0, 1)
    add(sfx, t0, y * vel, gain, pan=pan, rev=0.45)


def pop(t0, m, vel=1.0, pan=0.0, gain=0.12):
    f, tt = hz(m), tvec(0.25); fr = f * (1 + 0.5 * np.exp(-tt * 90))
    add(sfx, t0, np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 16) * np.clip(tt / 0.002, 0, 1) * vel, gain, pan=pan, rev=0.3)


def click(t0, vel=1.0, f=2600, gain=0.07):
    tt = tvec(0.03)
    y = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 400) + 0.4 * hp(rng.standard_normal(len(tt)), 3000) * np.exp(-tt * 600)
    add(sfx, t0, y * vel, gain, rev=0.08)


def thud(t0, vel=1.0, pitch=1.0, pan=0.0):
    """A letter landing on the table: soft body and a paper slap."""
    tt = tvec(0.3); f = (95 + 60 * np.exp(-tt * 40)) * pitch
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 26)
    slap = bp(rng.standard_normal(len(tt)), 500, 3200) * np.exp(-tt * 55)
    add(sfx, t0, (body * 0.9 + slap * 0.6) * vel, 0.32, pan=pan, rev=0.12)


def scratch(t0, dur, vel=1.0):
    tt = tvec(dur); n = bp(rng.standard_normal(len(tt)), 1800, 6000)
    add(sfx, t0, n * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 38 * tt))) * np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 0.7 * vel, 0.05, rev=0.1)


def whoosh(t0, dur, f0, f1, vel=1.0, gain=0.08):
    tt = tvec(dur); n = rng.standard_normal(len(tt) + 2000); out = np.zeros(len(tt))
    edges = np.linspace(0, len(tt), 25).astype(int)
    for k in range(24):
        a, b = edges[k], edges[k + 1]; fc = f0 * (f1 / f0) ** (k / 23)
        out[a:b] = bp(n[a:b + 2000], fc * 0.6, min(fc * 1.6, 20000))[2000:]
    add(sfx, t0, out * np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 1.5 * vel, gain, rev=0.25)


def boom(t0, m, dur=1.6, gain=0.3):
    tt = tvec(dur); add(music, t0, np.sin(2 * np.pi * hz(m) * tt) * np.exp(-tt * 2.2) * np.clip(tt / 0.01, 0, 1), gain)


# ---------------------------------------------------------------- score
BEAT = 0.5                                   # 120 BPM; bars start on the hook's end, so the groove drops with the phone
F_, DM, BB, C_ = [53, 57, 60, 64], [50, 53, 57, 60], [46, 50, 53, 57], [48, 52, 55, 60]
CHORDS = [(F_, 41), (DM, 38), (BB, 34), (C_, 36)]      # chord, bass root

# hook: dark filtered pad, a clock-like hat, the letters landing, the pen striking the line
pad([38, 45, 50, 53, 57], 0.0, HOOK_END + 0.1, 300, 900, 0.8)
for k in range(int(HOOK_END / 0.25)):
    hat(k * 0.25, vel=0.35 if k % 2 else 0.6, pan=0.3)
for i, land in enumerate([0.25, 0.7, 1.15, 1.5, 1.75]):
    thud(land, vel=0.9, pitch=1 + 0.06 * (i % 3), pan=(-0.2, 0.2)[i % 2])
scratch(2.2, 0.32)
whoosh(HOOK_END - 0.55, 0.6, 300, 3200, vel=0.9)

# groove from the hook's end to the end card: F  Dm  Bb  C, one bar (2 s) each
bars = int(np.ceil((END - HOOK_END) / (4 * BEAT)))
for k in range(bars):
    b0 = HOOK_END + k * 4 * BEAT
    ch, root = CHORDS[k % 4]
    for bt in range(4):
        tb = b0 + bt * BEAT
        if tb >= END - 0.05: break
        if bt in (0, 2): kick(tb, 1.0 if bt == 0 else 0.8)
        hat(tb + BEAT / 2, 0.8)
        if bt in (0, 2): bass(tb, root, BEAT * 1.6, 0.9)
    epiano(b0, ch[0] + 12, 1.6, 0.8, pan=-0.15); epiano(b0 + 0.01, ch[1] + 12, 1.6, 0.7); epiano(b0 + 0.02, ch[2] + 12, 1.6, 0.7, pan=0.15)
    pad([n + 12 for n in ch], b0, min(b0 + 4 * BEAT + 0.3, END + 0.3), 900, 1400, 0.35)

# scene effects (cue times mirror index.html)
POP_NOTES = [77, 81, 84, 89]
for i, (s, b) in enumerate(BEATS):
    if i == 0 and b.get("before"):
        click(s + 0.3); click(s + 0.48, 0.9, f=1800); click(s + 0.53, 0.7, f=1500)       # tap, shutter
        tt = tvec(0.25); add(sfx, s + 0.48, hp(rng.standard_normal(len(tt)), 2500) * np.exp(-tt * 30), 0.05, rev=0.15)
        ready = s + 0.85
    else:
        whoosh(s - 0.06, 0.42, 500, 2400, vel=0.8)                                      # screen push
        ready = s + 0.35
    ring = ready + 0.1
    if b.get("highlight"):
        if b.get("collect"):
            whoosh(s + 0.3, 0.36, 2400, 600, vel=0.6, gain=0.05)
            pluck(s + 0.62, 53, 1.0, gain=0.15); pluck(s + 0.62, 65, 0.6, gain=0.09)         # lands in the folder
            ring = s + 0.62
        bell(ring, 84, 0.8, pan=0.15); bell(ring + 0.09, 89, 0.6, pan=0.2)
    for j, _ in enumerate(b.get("callouts", [])):
        at = (ring + 0.15 if b.get("highlight") else ready) + j * 0.25
        pop(at + 0.12, POP_NOTES[j % 4], pan=-0.15 + 0.15 * j)

# end card: the band rises, Bb swells and resolves to F, the paper plane flies in, a ding on the call to action
whoosh(END - 0.05, 0.55, 300, 2600, vel=1.0, gain=0.09)
pad([46, 50, 53, 58, 62], END, END + 0.6, 900, 1800, 0.6)
pad([41, 53, 57, 60, 65, 69], END + 0.5, DUR + 0.2, 1800, 1000, 1.2)
boom(END + 0.5, 29, 2.0, 0.28); kick(END + 0.5, 0.9)
epiano(END + 0.5, 65, 2.5, 1.0, gain=0.07); epiano(END + 0.51, 69, 2.5, 0.9, gain=0.07); epiano(END + 0.52, 72, 2.5, 0.9, gain=0.07)
whoosh(END + 0.3, 0.7, 600, 3000, vel=0.7, gain=0.06)
bell(END + 1.36, 84, 0.6, gain=0.08); bell(END + 1.36, 89, 0.45, pan=0.1, gain=0.08)
for k, m in enumerate([72, 69, 65, 60]):
    pluck(END + 1.9 + k * 0.25, m, vel=0.45 - 0.07 * k, pan=0.3 - 0.2 * k, gain=0.06)

# ---------------------------------------------------------------- mix
tt = np.arange(N) / SR
duck = np.ones(N)                                   # pad and keys breathe with the kick
for k in range(bars * 2):
    kt = HOOK_END + k * 2 * BEAT
    if kt < END: m = tt >= kt; duck[m] *= 1 - 0.25 * np.exp(-(tt[m] - kt) * 9)
ir_t = tvec(1.8)
ir = np.stack([lp(rng.standard_normal(len(ir_t)), 6500) * np.exp(-ir_t * 3.2) for _ in range(2)])
ir[:, : int(0.012 * SR)] = 0
ir /= np.abs(ir).sum(axis=1, keepdims=True) / 40
wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])
mix = music * duck + sfx + wet * 0.5
mix = np.stack([hp(lp(mix[c], 16500), 28) for c in range(2)])
mix /= np.abs(mix).max() / 0.85
mix = np.tanh(mix * 1.25) / np.tanh(1.25)
mix *= np.clip(tt / 0.02, 0, 1) * np.clip((DUR - tt) / 0.8, 0, 1)

os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
wav, m4a = os.path.join(tempfile.mkdtemp(), "soundtrack.wav"), os.path.join(HERE, "audio", "soundtrack.m4a")
wavfile.write(wav, SR, (mix.T * 0.95).astype(np.float32))
probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
m = json.loads(probe[probe.rindex("{"): probe.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", ln + ",aresample=48000", "-c:a", "aac", "-b:a", "192k", m4a], check=True)
os.remove(wav)
print(f"wrote audio/soundtrack.m4a ({DUR:.1f} s; source loudness {m['input_i']} LUFS, normalised to -14)")
