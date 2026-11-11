"""Static checks on every entry in concepts/. Exits non-zero if any fail.

    python scripts/check_entries.py

Checks:
  - required front matter: title, date, description, order (unique, 1..N),
    theme, kind, categories, source, verified
  - required sections, in order
  - every Plot.plot call sets ariaLabel and ariaDescription (accessibility)
  - simulations that draw random numbers (rng(...)) expose a "Random seed"
    control and pass `seed` to rng(); deterministic ones need no seed
  - the generated "Show simulation code" block is present (build_groups.py)
  - every local .qmd link resolves
  - Related-entry links are reciprocal (build_groups.py fixes this)

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
FIELDS = ["title", "date", "description", "order", "theme", "kind", "categories", "source", "verified"]


def main():
    problems = []
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

        for target in re.findall(r"\]\(([^)#\s]+\.qmd)(?:#[^)]*)?\)", text):
            if target.startswith("http"):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                say(f"broken link to {target}")

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

    for p in problems:
        print(p)
    print(f"{len(paths)} entries checked, {len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
