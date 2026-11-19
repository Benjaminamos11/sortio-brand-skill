"""Start a new reel from this template as a self-contained HyperFrames project.

HyperFrames only loads files inside the project folder, so the template's "../../assets/..." paths (they point at the
skill's shared logo and app screens) cannot be rendered in place. This script copies the template to a new folder,
copies every shared asset the reel uses into <new folder>/assets/, and rewrites the paths to "assets/...".

usage:  python3 tools/new_reel.py ~/Sortio-Videos/2026-11-20-qr-reel      (run inside templates/reels)
        python3 tools/new_reel.py <folder> --sync     re-copy shared assets after you edited reel-config.js
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        # templates/reels
# the skill folder (sortio-brand) that holds assets/: next to this template, or the installed copy
_roots = [os.path.dirname(os.path.dirname(HERE)), os.environ.get("SORTIO_SKILL", ""),
          os.path.expanduser("~/.claude/skills/sortio-brand")]
SKILL = next((r for r in _roots if r and os.path.isdir(os.path.join(r, "assets", "screens"))), _roots[0])
SHARED = re.compile(r"(\.\./\.\./assets/[^\"'\s)]+)")
TEXT = ("index.html", "reel-config.js")

if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
    print(__doc__); sys.exit(0 if sys.argv[1:2] in (["-h"], ["--help"]) else 2)
dest =os.path.abspath(os.path.expanduser(sys.argv[1]))
sync = "--sync" in sys.argv[2:]

if not sync:
    if os.path.exists(dest) and os.listdir(dest):
        sys.exit(f"{dest} exists and is not empty; pick a new folder (or pass --sync to refresh its assets)")
    shutil.copytree(HERE, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("renders", ".hyperframes", "__pycache__", "*.mp4"))

missing, copied = [], 0
for name in TEXT:
    path = os.path.join(dest, name)
    src = open(path, encoding="utf-8").read()
    # in a project made earlier, paths already read "assets/..."; --sync looks the originals up again
    for ref in sorted(set(SHARED.findall(src)) | {"../../" + r for r in re.findall(r"[\"'](assets/(?:screens|logo|fonts|images|examples)/[^\"']+)", src)}):
        rel = ref[len("../../"):]
        orig = os.path.join(SKILL, rel)
        if not os.path.isfile(orig):
            if not os.path.isfile(os.path.join(dest, rel)):
                missing.append(rel)
            continue
        os.makedirs(os.path.dirname(os.path.join(dest, rel)), exist_ok=True)
        shutil.copy2(orig, os.path.join(dest, rel)); copied += 1
    open(path, "w", encoding="utf-8").write(src.replace("../../assets/", "assets/"))

print(f"{'refreshed' if sync else 'created'} {dest} ({copied} shared asset file(s) copied into assets/)")
if missing:
    print("MISSING in the skill's assets folder (fix reel-config.js or add the files):\n  " + "\n  ".join(missing))
    sys.exit(1)
print("next: cd into it, then  npx --yes hyperframes@0.9.70 check  and  npx --yes hyperframes@0.9.70 preview")
