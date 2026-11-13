"""Static checks on every entry in concepts/. Exits non-zero if any fail.

    python scripts/check_entries.py

Checks:
  - required front matter: title, date, description, order (unique, 1..N),
    theme, kind, difficulty, categories, source, verified
  - required sections, in order
  - every Plot.plot call sets ariaLabel and ariaDescription (accessibility)
  - simulations that draw random numbers (rng(...)) expose a "Random seed"
    control and pass `seed` to rng(); deterministic ones need no seed
  - the generated "Show simulation code" block is present (build_groups.py)
  - every entry has R and Python versions (sims/r/<slug>.R and
    sims/python/<slug>.py) shown in its code tabs, with lines of at most 78
    characters; scripts/check_code.py runs them
  - every R script has Quarto code annotations: `# <n>` markers whose numbers
    1..k match the items of its `# Annotations` trailer (build_groups.py
    turns the trailer into the list under the R tab)
  - every local .qmd link resolves
  - Related-entry links are reciprocal (build_groups.py fixes this)
  - the helper import names only helpers the cells use (the import line is
    shown to readers in the Observable JS tab)
  - charts use only the approved colors (PALETTE), which keep every
    meaningful mark at 3:1 contrast or better in light and dark mode
  - "Law or aphorism" entries label their simulation as a toy model ("toy",
    "our own" or "made-up") unless the simulation is a real statistical
    mechanism (REAL_MECHANISM)

It also prints warnings, which don't fail the check, for quoted strings that
look like hypothetical lines (quotation marks right after "such as", "like",
"say" and similar, with no attribution nearby). The site's convention is that
quotation marks are only for words someone actually said or wrote, and
hypothetical lines go in italics; read each warning and decide.

Run it after editing entries and before committing; it complements the
headless-browser check described in CLAUDE.md, which catches runtime errors.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ["## What it is", "## Why it matters", "## How it works", "## Simulated example",
            "## Key takeaways", "## Related entries", "## Source"]
FIELDS = ["title", "date", "description", "order", "theme", "kind", "difficulty", "categories", "source",
          "verified"]
GENERATED = re.compile(r"<!-- Simulation code: generated.*?<!-- End of generated simulation code. -->", re.S)
OJS_CELL = re.compile(r"```\{ojs\}\n(.*?)```", re.S)

# Colors allowed in the OJS cells. Blue, red and dark red are the series
# colors; gray, green and gold are the darkened versions that pass 3:1 on both
# backgrounds; purple and the two mid grays pass too. #ddd and #f0f0f0 are
# only for decorative stems and empty cells that carry no information.
PALETTE = {"#2166ac", "#d6604d", "#67001f", "#8a8a8a", "#1a9850", "#b8860b", "#984ea3",
           "#777", "#7f7f7f", "#ddd", "#f0f0f0"}

# "Law or aphorism" entries whose simulation shows a real statistical
# mechanism, so it needs no toy-model label. Every other aphorism entry must
# say its simulation is a toy model of its own.
REAL_MECHANISM = {
    "arrows-other-theorem-strong", "bayesian", "clarkes-law", "conservatism",
    "correlation-does-not-imply-correlation", "default-greatest-trick", "god-is-in-every-leaf",
    "guarantee-is-assumption", "honesty-and-transparency", "objects-of-the-class",
    "paradox-of-philosophizing", "random-in-random-out", "robustness-checks", "salad-tongs",
    "statistical-chemotherapy", "story-time", "theoretical-statistics",
    "theoretical-vs-applied-statisticians", "until-it-runs-twice",
}

# Quotation marks right after these words usually introduce a hypothetical
# line, which the site sets in italics.
HYPOTHETICAL_CUE = re.compile(
    r'\b(such as|like|say|says|saying|asks|asking|thinks|e\.g\.,?|for example,?)\s+"([^"\n]*\s[^"\n]*)"')
ATTRIBUTION = re.compile(r"Gelman|writes|wrote|post|quot|called|calls|in his words|in their words|"
                         r"put it|said|the line|the phrase|the term|law|proverb|saying", re.I)


def main():
    problems = []
    warnings = []
    orders = {}
    related = {}
    paths = sorted(glob.glob(os.path.join(ROOT, "concepts", "*.qmd")))
    for path in paths:
        slug = os.path.basename(path)[:-4]
        text = open(path, encoding="utf-8").read()
        say = lambda msg: problems.append(f"{slug}: {msg}")

        fm = text.split("---", 2)[1] if text.startswith("---") else ""
        for f in FIELDS:
            if not re.search(rf"^{f}:", fm, re.M):
                say(f"missing front matter field '{f}'")
        m = re.search(r"^order: (\d+)", fm, re.M)
        if m:
            orders.setdefault(int(m.group(1)), []).append(slug)

        pos = [text.find(s) for s in SECTIONS]
        if -1 in pos:
            say(f"missing section(s): {[s for s, p in zip(SECTIONS, pos) if p == -1]}")
        elif pos != sorted(pos):
            say("sections out of order")

        plots = len(re.findall(r"Plot\.plot\(\{", text))
        if plots == 0:
            say("no Plot.plot chart")
        if len(re.findall(r"Plot\.plot\(\{\s*ariaLabel:", text)) != plots:
            say("a Plot.plot call is missing ariaLabel")
        if text.count("ariaDescription:") < plots:
            say("a Plot.plot call is missing ariaDescription")

        if "rng(" in text.replace("import {rng", ""):
            if 'label: "Random seed' not in text:
                say("uses rng() but has no 'Random seed' control")
            if not re.search(r"rng\(seed", text):
                say("uses rng() without passing the seed")
        if "Math.random" in text:
            say("uses unseeded Math.random")
        if "```{ojs}" in text and "<!-- Simulation code: generated" not in text:
            say("no generated 'Show simulation code' block (run build_groups.py)")
        for lang, rel_path in [("R", f"sims/r/{slug}.R"), ("Python", f"sims/python/{slug}.py")]:
            full = os.path.join(ROOT, rel_path)
            if not os.path.exists(full):
                say(f"missing {lang} version of the simulation ({rel_path})")
            elif f"## {lang} {{.unlisted}}" not in text:
                say(f"{lang} version not in the code tabs (run build_groups.py)")
            else:
                script = open(full, encoding="utf-8").read()
                trailer = script.rfind("\n# Annotations\n")
                code = script if trailer < 0 else script[:trailer]
                # Quarto renders a trailing `# <n>` marker as a small circle, so it doesn't
                # count; the annotation trailer is shown as text, not code.
                if any(len(re.sub(r"\s*# <\d+>$", "", line)) > 78 for line in code.splitlines()):
                    say(f"{rel_path} has lines over 78 characters (they scroll sideways on the page)")
                if lang == "R":
                    marks = sorted({int(m) for m in re.findall(r"# <(\d+)>$", code, re.M)})
                    items = sorted(int(m) for m in re.findall(r"^# (\d+)\. ", script[trailer:], re.M)) if trailer >= 0 else []
                    if not marks or trailer < 0:
                        say(f"{rel_path} has no code annotations (`# <1>` markers and a `# Annotations` trailer)")
                    elif marks != items or marks != list(range(1, len(marks) + 1)):
                        say(f"{rel_path}: annotation markers {marks} don't match the trailer items {items}")

        for target in re.findall(r"\]\(([^)#\s]+\.qmd)(?:#[^)]*)?\)", text):
            if target.startswith("http"):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                say(f"broken link to {target}")

        body = GENERATED.sub("", text.split("---", 2)[2] if text.startswith("---") else text)
        cells = OJS_CELL.findall(body)
        prose = re.sub(r"\[[^\]]*\]\([^)]*\)", "[link]", OJS_CELL.sub("", body))
        imp = next((m for m in (re.search(r'import \{([^}]*)\} from "\.\./js/stats\.js"', c) for c in cells) if m),
                   None)
        if imp:
            rest = "\n".join(cells).replace(imp.group(0), "")
            unused = [n.strip() for n in imp.group(1).split(",")
                      if n.strip() and not re.search(r"\b" + re.escape(n.strip()) + r"\b", rest)]
            if unused:
                say(f"imports helpers it never uses: {', '.join(unused)}")
        colors = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", "\n".join(cells))}
        if colors - PALETTE:
            say(f"chart colors outside the approved palette: {', '.join(sorted(colors - PALETTE))}")
        if 'kind: "Law or aphorism"' in fm and slug not in REAL_MECHANISM:
            if not re.search(r"\btoy\b|our own|made-up", prose, re.I):
                say("aphorism simulation is not labelled as a toy model ('A toy model, our own.')")
        for m in HYPOTHETICAL_CUE.finditer(prose):
            if not ATTRIBUTION.search(prose[max(0, m.start() - 150):m.start()]):
                warnings.append(f"{slug}: possible hypothetical line in quotation marks: \"{m.group(2)[:70]}\"")

        rel = re.search(r"## Related entries\n\n((?:- .*\n)+)", text)
        related[slug] = re.findall(r"\]\(([a-z0-9-]+)\.qmd\)", rel.group(1)) if rel else []

    for slug, targets in related.items():
        for t in targets:
            if t in related and slug not in related[t]:
                problems.append(f"{slug}: Related link to {t} is not reciprocated (run build_groups.py)")

    expected = set(range(1, len(paths) + 1))
    if set(orders) != expected:
        problems.append(f"order values are not exactly 1..{len(paths)}: missing {sorted(expected - set(orders))}")
    for o, slugs in orders.items():
        if len(slugs) > 1:
            problems.append(f"order {o} used by {slugs}")

    for w in warnings:
        print("warning:", w)
    for p in problems:
        print(p)
    print(f"{len(paths)} entries checked, {len(problems)} problem(s), {len(warnings)} warning(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
