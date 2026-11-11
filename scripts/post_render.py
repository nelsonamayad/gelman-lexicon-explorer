"""Post-render step, run by Quarto after every render (project.post-render).

Removes the ES6 polyfill <script> that Quarto adds next to MathJax. Every
browser this site supports has ES6, MathJax 4 doesn't need it, and it would
otherwise be an extra third-party request on every page.
"""
import glob
import os

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
