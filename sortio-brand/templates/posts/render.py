"""Render Sortio post templates (HTML) to PNG or JPG at their exact size.

Setup, once:
    pip install playwright
    playwright install chromium

Usage (from any folder):
    python render.py                      # every *.html next to this script
    python render.py post-price-4x5.html  # only these files (names or paths)
    python render.py --out ~/Desktop/sortio --jpg

Each HTML file declares its size in <meta name="sortio:size" content="1080x1350">.
Without that meta tag the size of the first .ad element is used.
Output goes to ./renders/ next to this script unless --out is given.

Before each screenshot the script waits for the web fonts and every <img>.
It then reports:
  - fonts that did not load (the brand fonts are in ../../assets/fonts),
  - images that did not load (wrong path),
  - [data-check] elements whose text is wider than its box or leaves the frame,
  - on 9:16 stories: [data-check] elements outside the safe zone
    (y 250 to 1580, so the Instagram UI does not cover them).
"""
import argparse
import asyncio
import re
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    sys.exit("Playwright is missing. Run: pip install playwright && playwright install chromium")

HERE = Path(__file__).resolve().parent
FONTS = ["Hedvig Letters Serif", "Inter", "JetBrains Mono"]
STORY_SAFE = (250, 1580)  # top and bottom limit for text and CTAs on 1080x1920

WAIT_JS = """
async (fams) => {
  await document.fonts.ready;
  await Promise.all(fams.map(f => document.fonts.load(`40px "${f}"`).catch(() => null)));
  // An image counts as settled once it has loaded or failed (complete), so a wrong path never hangs.
  await Promise.all([...document.images].map(img => img.complete ? null :
    new Promise(res => { img.addEventListener('load', res); img.addEventListener('error', res); setTimeout(res, 15000); })));
  await document.fonts.ready;
  return {
    missingFonts: fams.filter(f => !document.fonts.check(`40px "${f}"`)),
    brokenImages: [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
  };
}
"""

CHECK_JS = """
([safeTop, safeBottom]) => {
  const ad = document.querySelector('.ad');
  if (!ad) return ['no .ad element found'];
  const A = ad.getBoundingClientRect();
  const isStory = Math.round(A.width) === 1080 && Math.round(A.height) === 1920;
  const out = [];
  document.querySelectorAll('[data-check]').forEach(el => {
    const name = el.dataset.check;
    const r = el.getBoundingClientRect();
    if (el.scrollWidth > el.clientWidth + 1)
      out.push(name + ': text wider than its box');
    if (r.left < A.left - 0.5 || r.right > A.right + 0.5 || r.top < A.top - 0.5 || r.bottom > A.bottom + 0.5)
      out.push(name + ': outside the frame');
    let top = null, bottom = null;
    if (el.dataset.safe && el.dataset.safe !== 'off') [top, bottom] = el.dataset.safe.split(',').map(Number);
    else if (isStory && el.dataset.safe !== 'off') [top, bottom] = [safeTop, safeBottom];
    if (top !== null && (r.top - A.top < top || r.bottom - A.top > bottom))
      out.push(`${name}: outside the safe zone ${top}-${bottom} (is ${Math.round(r.top - A.top)}-${Math.round(r.bottom - A.top)})`);
  });
  return out;
}
"""


def declared_size(html: str):
    m = re.search(r'<meta\s+name=["\']sortio:size["\']\s+content=["\'](\d+)\s*[x×]\s*(\d+)["\']', html, re.I)
    return (int(m.group(1)), int(m.group(2))) if m else None


async def render(files, out_dir: Path, jpg: bool, scale: float) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for f in files:
            html = f.read_text(encoding="utf-8")
            size = declared_size(html) or (1080, 1350)
            page = await browser.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=scale)
            await page.goto(f.resolve().as_uri())
            info = await page.evaluate(WAIT_JS, FONTS)
            await page.wait_for_timeout(300)
            problems = await page.evaluate(CHECK_JS, list(STORY_SAFE))
            ad = await page.query_selector(".ad")
            target = out_dir / (f.stem + (".jpg" if jpg else ".png"))
            shot = {"path": str(target)}
            if jpg:
                shot.update(type="jpeg", quality=92)
            if ad:
                await ad.screenshot(**shot)
            else:
                await page.screenshot(**shot)
            box = await ad.bounding_box() if ad else {"width": size[0], "height": size[1]}
            real = f"{round(box['width'] * scale)}x{round(box['height'] * scale)}"
            status = "ok"
            if info["missingFonts"] or info["brokenImages"] or problems:
                status = "CHECK"
                failures += 1
            print(f"[{status}] {f.name} -> {target} ({real})")
            for fam in info["missingFonts"]:
                print(f"    font not loaded: {fam}")
            for src in info["brokenImages"]:
                print(f"    image not found: {src}")
            for prob in problems:
                print(f"    {prob}")
            await page.close()
        await browser.close()
    return failures


def main():
    ap = argparse.ArgumentParser(description="Render Sortio HTML templates to images.")
    ap.add_argument("files", nargs="*", help="HTML files (default: every *.html next to this script)")
    ap.add_argument("--out", default=str(HERE / "renders"), help="output folder (default: ./renders next to this script)")
    ap.add_argument("--jpg", action="store_true", help="write JPG (quality 92) instead of PNG")
    ap.add_argument("--scale", type=float, default=1.0, help="device scale factor, e.g. 2 for a double-size proof")
    args = ap.parse_args()

    if args.files:
        files = []
        for name in args.files:
            path = Path(name).expanduser()
            if not path.exists():
                path = HERE / name
            if not path.exists():
                sys.exit(f"Not found: {name}")
            files.append(path)
    else:
        files = sorted(HERE.glob("*.html"))
    if not files:
        sys.exit("No HTML files found.")

    failures = asyncio.run(render(files, Path(args.out).expanduser().resolve(), args.jpg, args.scale))
    if failures:
        print(f"\n{failures} file(s) need a look (see CHECK lines above).")
        sys.exit(1)


if __name__ == "__main__":
    main()
