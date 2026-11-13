"""Post-render step, run by Quarto after every render (project.post-render).

1. Removes the ES6 polyfill <script> that Quarto adds next to MathJax. Every
   browser this site supports has ES6, MathJax 4 doesn't need it, and it would
   otherwise be an extra third-party request on every page.
2. Replaces the cookie banner's stock English text, which says the site uses
   cookies "to show you personalized content and targeted ads". This site has
   no ads and uses only Google Analytics, loaded after consent (see
   _analytics.html and about.qmd#privacy). Quarto has no option for the
   banner text, so the bundled cookie-consent.js is patched here.
3. Checks the versions of Observable Plot, Inputs and d3 that Quarto's OJS
   runtime loads. Quarto hard-codes them (1.12.1: Plot 0.6.11, Inputs 0.10.6,
   d3 7.8.5) and CI pins Quarto, so they only change when Quarto does. A
   different version can change chart defaults, so this warns; check the
   charts with scripts/check_pages.py --readouts and update PINNED.
"""
import re
import glob
import os
import sys

out = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site")
files = [f for f in os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").split("\n") if f.endswith(".html")]
if not files:
    files = glob.glob(os.path.join(out, "**", "*.html"), recursive=True)

TAG = '<script src="https://cdnjs.cloudflare.com/polyfill/v3/polyfill.min.js?features=es6"></script>'
for f in files:
    if not os.path.exists(f):
        continue
    text = open(f, encoding="utf-8").read()
    if TAG in text:
        open(f, "w", encoding="utf-8", newline="").write(text.replace(TAG, ""))

# The library ships the sentence in US and UK spellings; replace both.
STOCKS = [('"nb_text":"We use cookies and other tracking technologies to improve your browsing experience on our '
           f'website, to show you personali{z} content and targeted ads, to anal{y} our website traffic, and to '
           'understand where our visitors are coming from."') for z, y in [("zed", "yze"), ("sed", "yse")]]
OURS = ('"nb_text":"With your permission, this site uses Google Analytics cookies to count visits and see which '
        'entries people read. There are no ads and no other tracking, and nothing is set unless you agree. '
        'You can change your choice at any time with the Cookie preferences link at the bottom of every page."')
js = os.path.join(out, "site_libs", "cookie-consent", "cookie-consent.js")
if os.path.exists(js):
    text = open(js, encoding="utf-8").read()
    patched = text
    for stock in STOCKS:
        patched = patched.replace(stock, OURS)
    if patched != text:
        open(js, "w", encoding="utf-8", newline="").write(patched)
    elif OURS not in text:
        print("post_render.py: cookie banner text not found in cookie-consent.js; "
              "the stock wording may have changed. Check the banner.", file=sys.stderr)

PINNED = {"@observablehq/plot": "0.6.11", "@observablehq/inputs": "0.10.6", "d3": "7.8.5"}
runtime = os.path.join(out, "site_libs", "quarto-ojs", "quarto-ojs-runtime.js")
if os.path.exists(runtime):
    text = open(runtime, encoding="utf-8").read()
    for name, want in PINNED.items():
        m = re.search(r'dependency\("' + re.escape(name) + r'", "([^"]+)"', text)
        if m and m.group(1) != want:
            print(f"post_render.py: Quarto now loads {name} {m.group(1)}, not {want}. "
                  "Chart defaults may have changed; check the pages and update PINNED.", file=sys.stderr)
