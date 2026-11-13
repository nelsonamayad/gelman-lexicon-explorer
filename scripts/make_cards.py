"""Make a social-media preview card (1200 x 630 PNG) for every entry.

    quarto render
    python scripts/make_cards.py                 # every entry
    python scripts/make_cards.py kangaroo 16     # some entries (slugs)

Each card shows the entry's number, title and Gelman's definition next to a
thumbnail of the entry's first chart, taken from the rendered page. The cards
go to assets/cards/<slug>.png, and build_groups.py points each entry's
`image:` at its card, so links to an entry shared on social media show it.
Rerun this after changing an entry's title, definition or chart, then run
build_groups.py. Needs Google Chrome (set CHROME if it isn't found) and the
rendered site in _site/.
"""

import concurrent.futures
import functools
import glob
import html
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_pages import QuietHandler, find_chrome  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "cards")

CARD = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=News+Cycle:wght@400;700&display=block" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ font-family: "News Cycle", "Arial Narrow", Arial, sans-serif; background: #fbfaf7; color: #1f2328;
         display: grid; grid-template-columns: 560px 1fr; }}
  .text {{ padding: 56px 24px 48px 64px; display: flex; flex-direction: column; border-left: 14px solid #2166ac; }}
  .site {{ font-size: 24px; color: #5c6670; letter-spacing: 0.02em; }}
  .num {{ font-size: 30px; font-weight: 700; color: #2166ac; margin-top: 36px; }}
  h1 {{ font-size: {title_size}px; line-height: 1.08; margin: 8px 0 24px; font-weight: 700; }}
  .def {{ font-size: {def_size}px; line-height: 1.3; color: #333a40; }}
  .foot {{ margin-top: auto; font-size: 20px; color: #5c6670; }}
  .chart {{ display: flex; align-items: center; justify-content: center; padding: 40px 48px 40px 16px; }}
  .chart svg {{ width: 100% !important; height: auto !important; max-height: 540px; color: #1f2328;
               background: transparent; font-family: "News Cycle", Arial, sans-serif; }}
</style></head>
<body>
  <div class="text">
    <div class="site">Andrew Gelman Statistical Lexicon Explorer</div>
    <div class="num">#{order}</div>
    <h1>{title}</h1>
    <div class="def">{definition}</div>
    <div class="foot">An explanation and an interactive simulation</div>
  </div>
  <div class="chart">{svg}</div>
</body></html>
"""


def front(text, name):
    m = re.search(rf'^{name}: "?(.*?)"?$', text, re.M)
    return m.group(1).replace('\\"', '"') if m else ""


def chrome_run(chrome, args, timeout=180):
    profile = tempfile.mkdtemp(prefix="cards-")
    try:
        return subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
                               "--hide-scrollbars", f"--user-data-dir={profile}"] + args,
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=timeout).stdout
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def first_chart(dom):
    """The first labelled chart's <svg>, with its <style> block (Plot inlines one)."""
    m = re.search(r'<svg[^>]*aria-label="[^"]*"[^>]*>.*?</svg>', dom, re.S)
    return m.group(0) if m else ""


def make(chrome, base, slug):
    text = open(os.path.join(ROOT, "concepts", f"{slug}.qmd"), encoding="utf-8").read()
    title, definition, order = front(text, "title"), front(text, "description"), front(text, "order")
    svg = ""
    for _ in range(3):  # a slow load sometimes dumps the page before the chart is drawn
        dom = chrome_run(chrome, ["--virtual-time-budget=20000", "--window-size=1100,900", "--dump-dom",
                                  f"{base}/concepts/{slug}.html"])
        svg = first_chart(dom)
        if svg:
            break
    if not svg:
        return f"{slug}: no chart found"
    title_size = 64 if len(title) < 30 else 52 if len(title) < 55 else 42
    def_size = 30 if len(definition) < 90 else 26 if len(definition) < 160 else 22
    page = CARD.format(order=order, title=html.escape(title), definition=html.escape(definition), svg=svg,
                       title_size=title_size, def_size=def_size)
    tmp = tempfile.mkdtemp(prefix="card-")
    try:
        src = os.path.join(tmp, "card.html")
        open(src, "w", encoding="utf-8").write(page)
        png = os.path.join(OUT, f"{slug}.png")
        chrome_run(chrome, ["--virtual-time-budget=5000", "--window-size=1200,630",
                            f"--screenshot={png}", "file:///" + src.replace(os.sep, "/")])
        return None if os.path.exists(png) else f"{slug}: screenshot failed"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    site = os.path.join(ROOT, "_site")
    if not os.path.isdir(site):
        sys.exit("_site not found. Run `quarto render` first.")
    os.makedirs(OUT, exist_ok=True)
    slugs = sys.argv[1:] or sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "concepts", "*.qmd")))
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=site))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    chrome = find_chrome()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        problems = [p for p in pool.map(functools.partial(make, chrome, base), slugs) if p]
    server.shutdown()
    for p in problems:
        print(p)
    print(f"{len(slugs) - len(problems)} of {len(slugs)} cards written to assets/cards/")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
