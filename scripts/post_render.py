"""Post-render step, run by Quarto after every render (project.post-render).

1. Removes the ES6 polyfill <script> that Quarto adds next to MathJax. Every
   browser this site supports has ES6, MathJax 4 doesn't need it, and it would
   otherwise be an extra third-party request on every page.
2. Replaces the cookie banner's stock English text, which says the site uses
   cookies "to show you personalized content and targeted ads". This site has
   no ads and uses only Google Analytics, loaded after consent (see
   _analytics.html and about.qmd#privacy). Quarto has no option for the
   banner text, so the bundled cookie-consent.js is patched here.
"""
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
