"""Regenerate everything derived from each entry's `theme` and `kind`.

Every entry in concepts/ has two classifications in its front matter:

    theme: "Noise and evidence"          # what the entry is about (one of THEMES)
    kind: "Principle or heuristic"       # what sort of entry it is (one of KINDS)

Run from the project root after adding an entry or changing either field:

    python scripts/build_groups.py

It writes or updates:
  - categories: [theme, kind] in each entry (drives the clickable tags and the
    category filter on the home-page table)
  - a "Filed under" line in each entry's source callout, linking to its
    theme and kind pages
  - themes/<slug>.qmd: one page per theme, with entries split into sections by kind
  - kinds/<slug>.qmd: one page per kind, with entries split into sections by theme
  - _group-cards.md: theme and kind cards for the home page
  - _sidebar.yml: the docked sidebar, with entries grouped by theme in Gelman's order
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (name, slug, description), in display order.
THEMES = [
    ("Noise and evidence", "noise-and-evidence",
     "What happens when noisy data meet the p < 0.05 threshold: exaggerated estimates, wrong signs, "
     "forking paths, power, and what a published result is really worth."),
    ("Building and checking models", "building-and-checking-models",
     "Priors, partial pooling, model checking, computation and workflow: how to build a model, "
     "find out what's wrong with it, and know when to stop."),
    ("Causes, samples and populations", "causes-samples-populations",
     "Causal designs, confounding and generalization, and turning unrepresentative samples into "
     "statements about populations with multilevel regression and poststratification."),
    ("Showing and telling", "showing-and-telling",
     "Graphs, tables and writing: displays that let readers compare, numbers worth printing, and words that help."),
    ("How science behaves", "how-science-behaves",
     "Publication, peer review, criticism, credit and incentives: why the published record looks the way it does. "
     "Many of these are aphorisms, illustrated with toy models."),
    ("Thinking about statistics", "thinking-about-statistics",
     "What probability means, why defaults matter, Bayesian and frequentist views, and habits of reasoning "
     "that help or mislead."),
]

# (name, slug, plural heading, description), in display order.
KINDS = [
    ("Method or technique", "methods", "Methods and techniques",
     "Something you can do: a model, a display, a check."),
    ("Principle or heuristic", "principles", "Principles and heuristics",
     "A rule of thumb, or a fact about how statistics works, with a simulation showing why it holds."),
    ("Fallacy", "fallacies", "Fallacies",
     "A tempting error in reasoning, with a simulation showing how it misleads."),
    ("Law or aphorism", "laws-and-aphorisms", "Laws and aphorisms",
     "A pithy saying, often a joke about research culture, with a toy model of the mechanism behind it."),
    ("Advice", "advice", "Advice",
     "Practical guidance for graphics, writing and analysis."),
]

PUBLISHED = "2026-11-11"   # date these group pages were first published


def field(text, name):
    m = re.search(rf'^{name}: "?(.*?)"?$', text, re.M)
    return m.group(1) if m else None


def read_entries():
    theme_names = {t[0] for t in THEMES}
    kind_names = {k[0] for k in KINDS}
    entries = []
    for path in sorted(glob.glob(os.path.join(ROOT, "concepts", "*.qmd"))):
        text = open(path, encoding="utf-8").read()
        slug = os.path.basename(path)[:-4]
        theme, kind = field(text, "theme"), field(text, "kind")
        if theme not in theme_names:
            sys.exit(f"{slug}: unknown or missing theme {theme!r}")
        if kind not in kind_names:
            sys.exit(f"{slug}: unknown or missing kind {kind!r}")
        entries.append({"slug": slug, "path": path, "text": text, "theme": theme, "kind": kind,
                        "order": int(field(text, "order")), "title": field(text, "title")})
    return sorted(entries, key=lambda e: e["order"])


def sync_entry(e, theme_slug, kind_slug):
    """Keep categories and the 'Filed under' line in step with theme and kind."""
    text = e["text"]
    cats = f'categories: ["{e["theme"]}", "{e["kind"]}"]'
    text = re.sub(r"^categories: .*$", cats, text, count=1, flags=re.M)
    filed = (f'Filed under [{e["theme"]}](../themes/{theme_slug}.qmd) · '
             f'[{e["kind"]}](../kinds/{kind_slug}.qmd).')
    if re.search(r"^Filed under ", text, re.M):
        text = re.sub(r"^Filed under .*$", filed, text, count=1, flags=re.M)
    else:
        # Insert as a second paragraph inside the source callout.
        text = re.sub(r"(::: \{\.callout-note[^\n]*\n(?:(?!:::).*\n)+?)(:::)", r"\1\n" + filed + r"\n\2",
                      text, count=1)
    if text != e["text"]:
        open(e["path"], "w", encoding="utf-8").write(text)


def group_page(title, subtitle, desc, sections, crumb):
    """A page with one grid listing per section; sections = [(id, heading, blurb, include)]."""
    listings = []
    for lid, _, _, include in sections:
        inc = "\n".join(f'      {k}: "{v}"' for k, v in include.items())
        listings.append(f'''  - id: {lid}
    contents: "../concepts/*.qmd"
    type: grid
    sort: "order"
    categories: false
    fields: [title, description]
    grid-columns: 3
    page-size: 100
    include:
{inc}''')
    body = []
    for lid, heading, blurb, _ in sections:
        body.append(f"## {heading}\n\n{blurb}\n\n::: {{#{lid}}}\n:::\n")
    return f'''---
title: "{title}"
date: {PUBLISHED}
subtitle: "{subtitle}"
description: "{desc}"
sidebar: false
listing:
{chr(10).join(listings)}
---

{crumb}

{chr(10).join(body)}'''


def main():
    entries = read_entries()
    theme_slug = {t[0]: t[1] for t in THEMES}
    kind_slug = {k[0]: k[1] for k in KINDS}
    for e in entries:
        sync_entry(e, theme_slug[e["theme"]], kind_slug[e["kind"]])

    def count(theme=None, kind=None):
        return sum(1 for e in entries if (theme is None or e["theme"] == theme) and (kind is None or e["kind"] == kind))

    crumb = ("Entries are listed in the order they appear in Gelman's list. "
             "See [all themes](../index.qmd#themes), [all kinds](../index.qmd#kinds), "
             "or [browse every entry](../index.qmd#all-entries).")

    os.makedirs(os.path.join(ROOT, "themes"), exist_ok=True)
    for name, slug, desc in THEMES:
        sections = [(f"k-{ks}", f"{plural} ({count(name, kn)})", kdesc, {"theme": name, "kind": kn})
                    for kn, ks, plural, kdesc in KINDS if count(name, kn)]
        page = group_page(name, f"{count(name)} entries", desc, sections, crumb)
        open(os.path.join(ROOT, "themes", f"{slug}.qmd"), "w", encoding="utf-8").write(page)

    os.makedirs(os.path.join(ROOT, "kinds"), exist_ok=True)
    for name, slug, plural, desc in KINDS:
        sections = [(f"t-{ts}", f"{tn} ({count(tn, name)})", "", {"theme": tn, "kind": name})
                    for tn, ts, _ in THEMES if count(tn, name)]
        sections = [(i, h, f"[See the whole theme](../themes/{THEMES[[t[0] for t in THEMES].index(inc['theme'])][1]}.qmd).", inc)
                    for i, h, _, inc in sections]
        page = group_page(plural, f"{count(kind=name)} entries", desc, sections, crumb)
        open(os.path.join(ROOT, "kinds", f"{slug}.qmd"), "w", encoding="utf-8").write(page)

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;")

    cards = ["```{=html}", '<div class="topic-grid">']
    for name, slug, desc in THEMES:
        first = desc.split(". ")[0].rstrip(".") + "."
        cards.append(f'<a class="topic-card" href="themes/{slug}.html"><span class="topic-name">{esc(name)}</span>'
                     f'<span class="topic-count">{count(name)} entries</span><span class="topic-desc">{esc(first)}</span></a>')
    cards += ["</div>", "```"]
    kcards = ["```{=html}", '<div class="topic-grid kind-grid">']
    for name, slug, plural, desc in KINDS:
        kcards.append(f'<a class="topic-card kind-card" href="kinds/{slug}.html"><span class="topic-name">{esc(plural)}</span>'
                      f'<span class="topic-count">{count(kind=name)} entries</span><span class="topic-desc">{esc(desc)}</span></a>')
    kcards += ["</div>", "```"]
    with open(os.path.join(ROOT, "_group-cards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cards) + "\n")
    with open(os.path.join(ROOT, "_kind-cards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(kcards) + "\n")

    lines = ["# Generated by scripts/build_groups.py; do not edit by hand.",
             "website:", "  sidebar:", "    - id: entries", '      title: "Entries"', "      style: docked",
             "      collapse-level: 1", "      contents:"]
    for name, slug, _ in THEMES:
        lines.append(f'        - section: "{name} ({count(name)})"')
        lines.append(f"          href: themes/{slug}.qmd")
        lines.append("          contents:")
        for e in entries:
            if e["theme"] == name:
                lines.append(f"            - concepts/{e['slug']}.qmd")
    with open(os.path.join(ROOT, "_sidebar.yml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    for name, _, _ in THEMES:
        print(f"{count(name):4d}  {name}")
    for name, *_ in KINDS:
        print(f"{count(kind=name):4d}  {name}")


if __name__ == "__main__":
    main()
