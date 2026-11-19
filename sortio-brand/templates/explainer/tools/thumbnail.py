"""Screenshot thumb.html (1280x720) to renders/thumbnail.jpg with headless Chromium, after fonts and images load.

usage:  python3 tools/thumbnail.py [thumb.html] [renders/thumbnail.jpg]
needs:  python3 -m pip install playwright && python3 -m playwright install chromium
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "thumb.html").resolve()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "renders/thumbnail.jpg")
out.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    pg.goto(src.as_uri())
    pg.evaluate("document.fonts.ready.then(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))))")
    pg.screenshot(path=str(out), type="jpeg", quality=92)
    b.close()
print(f"wrote {out} (1280x720 JPG; check the size limit in YouTube Studio)")
