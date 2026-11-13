"""Regenerate everything derived from each entry's `theme` and `kind`.

Every entry in concepts/ has two classifications in its front matter:

    theme: "Noise and evidence"          # what the entry is about (one of THEMES)
    kind: "Principle or heuristic"       # what sort of entry it is (one of KINDS)

Run from the project root after adding an entry or changing either field:

    python scripts/build_groups.py

It writes or updates:
  - categories: [theme, kind, difficulty] in each entry (drives the clickable
    tags and the category filter on the home-page table)
  - a "Related terms" line in the source callout from `search-terms`, so the
    site search finds an entry by its other names
  - `image:` and `image-alt:` pointing at the entry's social-media card in
    assets/cards/ (made by scripts/make_cards.py), when the card exists
  - a "Filed under" line in each entry's source callout, linking to its
    theme and kind pages
  - reciprocal "Related entries" links (if A lists B, B lists A)
  - a "Source check" line in each entry's source callout, from its
    `verified: true/false` field (and optional `source-note:`)
  - themes/<slug>.qmd: one page per theme, with entries split into sections by kind
  - kinds/<slug>.qmd: one page per kind, with entries split into sections by theme
  - _group-cards.md: theme and kind cards for the home page
  - _sidebar.yml: the docked sidebar, with entries grouped by theme in Gelman's order and
    labelled with their number in his list
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
     "A rule of thumb, or a fact about how statistics works, with a simulation that illustrates it, often a toy model of our own."),
    ("Fallacy", "fallacies", "Fallacies",
     "A tempting error in reasoning, with a simulation showing how it misleads."),
    ("Law or aphorism", "laws-and-aphorisms", "Laws and aphorisms",
     "A pithy saying, often a joke about research culture, with a toy model of the mechanism behind it."),
    ("Advice", "advice", "Advice",
     "Practical guidance for graphics, writing and analysis."),
]

# Bootstrap Icons (https://icons.getbootstrap.com) for each theme and kind,
# by slug. The home-page cards use them; keep the Themes and Kinds menus in
# _quarto.yml's navbar in step by hand.
ICONS = {
    "noise-and-evidence": "soundwave",
    "building-and-checking-models": "tools",
    "causes-samples-populations": "people",
    "showing-and-telling": "bar-chart-line",
    "how-science-behaves": "mortarboard",
    "thinking-about-statistics": "lightbulb",
    "methods": "gear",
    "principles": "compass",
    "fallacies": "exclamation-triangle",
    "laws-and-aphorisms": "quote",
    "advice": "chat-left-text",
}

# Reading level, a third axis: what a reader needs to know to follow the
# entry. It becomes the third category tag, so the home-page table can filter
# on it.
LEVELS = ["Introductory", "Intermediate", "Advanced"]

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
        level = field(text, "difficulty")
        if level not in LEVELS:
            sys.exit(f"{slug}: 'difficulty' must be one of {LEVELS}, got {level!r}")
        verified = field(text, "verified")
        if verified not in ("true", "false"):
            sys.exit(f"{slug}: 'verified' must be true or false, got {verified!r}")
        entries.append({"slug": slug, "path": path, "text": text, "theme": theme, "kind": kind,
                        "verified": verified == "true", "source_note": field(text, "source-note"),
                        "order": int(field(text, "order")), "title": field(text, "title"),
                        "level": level, "terms": field(text, "search-terms")})
    return sorted(entries, key=lambda e: e["order"])


def sync_entry(e, theme_slug, kind_slug):
    """Keep categories, the 'Filed under' and 'Related terms' lines in step with the front matter."""
    text = e["text"]
    cats = f'categories: ["{e["theme"]}", "{e["kind"]}", "{e["level"]}"]'
    text = re.sub(r"^categories: .*$", cats, text, count=1, flags=re.M)
    # Social-media preview card made by scripts/make_cards.py, if there is one.
    text = re.sub(r"^image(-alt)?: .*\n", "", text, flags=re.M)
    if os.path.exists(os.path.join(ROOT, "assets", "cards", f'{e["slug"]}.png')):
        card = (f'image: "../assets/cards/{e["slug"]}.png"\n'
                f'image-alt: "#{e["order"]} {e["title"]}: an explanation and an interactive simulation, '
                f'from the Andrew Gelman Statistical Lexicon Explorer"\n')
        text = re.sub(r"^(verified: .*\n)", lambda m: m.group(1) + card, text, count=1, flags=re.M)
    filed = (f'Filed under [{e["theme"]}](../themes/{theme_slug}.qmd) · '
             f'[{e["kind"]}](../kinds/{kind_slug}.qmd) · '
             f'[{e["level"]}](../index.qmd#category={e["level"]}).')
    if re.search(r"^Filed under ", text, re.M):
        text = re.sub(r"^Filed under .*$", filed, text, count=1, flags=re.M)
    else:
        # Insert as a second paragraph inside the source callout.
        text = re.sub(r"(::: \{\.callout-note[^\n]*\n(?:(?!:::).*\n)+?)(:::)", r"\1\n" + filed + r"\n\2",
                      text, count=1)
    # Visible source-verification status, generated from `verified`.
    if e["verified"]:
        check = "Source check: ✓ The explanation was checked against the source."
        if e["source_note"]:
            check += " " + e["source_note"]
    else:
        note = e["source_note"] or "It hasn't yet been checked against the source."
        check = (f"Source check: not verified. {note} The explanation follows the entry's "
                 "definition and Gelman's published work; read the source for his own argument.")
    if re.search(r"^Source check: ", text, re.M):
        text = re.sub(r"^Source check: .*$", lambda m: check, text, count=1, flags=re.M)
    else:
        text = re.sub(r"^(Filed under .*)$", lambda m: m.group(1) + 2 * chr(10) + check,
                      text, count=1, flags=re.M)
    # Other names readers search for (front matter `search-terms`), shown and
    # so indexed by the site search.
    text = re.sub(r"^Related terms: .*\n\n", "", text, count=1, flags=re.M)
    if e["terms"]:
        text = re.sub(r"^(Source check: .*)$", lambda m: f"Related terms: {e['terms']}." + 2 * chr(10) + m.group(1),
                      text, count=1, flags=re.M)
    text = sync_sim_code(text, e["slug"])
    if text != e["text"]:
        open(e["path"], "w", encoding="utf-8").write(text)


SIM_START = "<!-- Simulation code: generated by scripts/build_groups.py from the cells above. Don't edit. -->"
SIM_END = "<!-- End of generated simulation code. -->"
OJS_CELL_RE = re.compile(r"```\{ojs\}\n(.*?)```", re.S)


ANNOT_HEADER = "# Annotations"


def split_annotations(script):
    """Split an R script into its code and its Quarto code annotations.

    The script marks lines with `# <1>`, `# <2>`, ... and ends with a trailer:

        # Annotations
        # 1. What the first marked line does.
        # 2. ...

    Returns (code, notes): the code without the trailer, and the trailer as a
    Markdown ordered list that Quarto attaches to the code block
    (https://quarto.org/docs/authoring/code-annotation.html). A script with no
    trailer returns (script, "").
    """
    script = script.strip("\n")
    i = script.rfind("\n" + ANNOT_HEADER + "\n")
    if i < 0:
        return script, ""
    code, trailer = script[:i].rstrip("\n"), script[i + len(ANNOT_HEADER) + 2:]
    items = re.findall(r"^# (\d+)\. (.*)$", trailer, re.M)
    notes = "".join(f"{n}. {text.strip()}\n" for n, text in items)
    return code, notes


def sync_sim_code(text, slug):
    """One "Show simulation code" block per entry, after the simulation.

    Entry cells don't echo their code (concepts/_metadata.yml sets echo: false),
    so readers see the whole simulation in a single collapsible block instead
    of one toggle per cell. The block is a tabset: the OJS cells of the
    "Simulated example" section (minus cell options and the readout cell),
    plus the same simulation in R and Python from sims/r/<slug>.R and
    sims/python/<slug>.py. The tabs share a group, so a reader's choice of
    language carries over to every page.
    """
    start, end = text.find("## Simulated example"), text.find("## Key takeaways")
    if start < 0 or end < 0:
        return text
    section = text[start:end]
    i = section.find(SIM_START)
    cells_part = section if i < 0 else section[:i]
    cells = []
    for body in OJS_CELL_RE.findall(cells_part):
        if "sim-readout" in body:
            continue
        lines = [l for l in body.rstrip("\n").split("\n") if not l.startswith("//|")]
        cells.append("\n".join(lines).strip("\n"))
    if not cells:
        return text
    tabs = [("Observable JS", "js", "\n\n".join(cells), "")]
    for name, lang, path in [("R", "r", f"sims/r/{slug}.R"), ("Python", "python", f"sims/python/{slug}.py")]:
        full = os.path.join(ROOT, path)
        if slug and os.path.exists(full):
            code, notes = split_annotations(open(full, encoding="utf-8").read())
            tabs.append((name, lang, code, notes))
    note = ""
    if len(tabs) > 1:
        note = ("The R version uses base R, and the Python version uses NumPy and Matplotlib. Where the simulation "
                "draws random numbers, each language draws its own, so exact numbers differ slightly but show the "
                "same pattern. The numbered markers in the R code are explained under it.\n\n")
    body = "::: {.panel-tabset group=\"sim-language\"}\n\n" + "".join(
        f"## {name} {{.unlisted}}\n\n```{{.{lang}}}\n{code}\n```\n{notes}\n" for name, lang, code, notes in tabs) + ":::\n\n"
    block = (SIM_START + "\n\n<details class=\"code-fold sim-code\">\n<summary>Show simulation code</summary>\n\n"
             + note + body + "</details>\n\n" + SIM_END)
    if i >= 0:
        j = section.index(SIM_END, i) + len(SIM_END)
        section = section[:i] + block + section[j:]
    else:
        # After the last cell: before the "Try it in R" line if there is one.
        r = section.find("**Try it in R.**")
        k = r if r >= 0 else len(section.rstrip("\n")) + 1
        section = section[:k].rstrip("\n") + "\n\n" + block + "\n\n" + section[k:].lstrip("\n")
        if r < 0 and not section.endswith("\n\n"):
            section = section.rstrip("\n") + "\n\n"
    return text[:start] + section + text[end:]


RELATED_RE = re.compile(r"(## Related entries\n\n)((?:- .*\n)+)")
LINK_RE = re.compile(r"\]\(([a-z0-9-]+)\.qmd\)")


def sync_related(entries):
    """Make "Related entries" links reciprocal: if A lists B, B lists A.

    Missing reverse links are appended to the end of B's list, in Gelman's
    order. Links to entries that don't exist stop the script.
    """
    by_slug = {e["slug"]: e for e in entries}
    texts = {e["slug"]: open(e["path"], encoding="utf-8").read() for e in entries}
    links = {}
    for slug, text in texts.items():
        m = RELATED_RE.search(text)
        if not m:
            sys.exit(f"{slug}: no '## Related entries' list")
        targets = LINK_RE.findall(m.group(2))
        missing = [t for t in targets if t not in by_slug]
        if missing:
            sys.exit(f"{slug}: Related entries link to missing pages {missing}")
        links[slug] = targets
    to_add = {slug: [] for slug in texts}
    for a, targets in links.items():
        for b in targets:
            if a not in links[b] and a not in to_add[b] and a != b:
                to_add[b].append(a)
    added = 0
    for b, sources in to_add.items():
        if not sources:
            continue
        sources.sort(key=lambda s: by_slug[s]["order"])
        lines = "".join(f'- [{by_slug[s]["title"].replace(chr(92) + chr(34), chr(34))}]({s}.qmd)\n'
                        for s in sources)
        text = RELATED_RE.sub(lambda m: m.group(1) + m.group(2) + lines, texts[b], count=1)
        open(by_slug[b]["path"], "w", encoding="utf-8").write(text)
        added += len(sources)
    return added


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
    added = sync_related(entries)
    if added:
        print(f"added {added} reciprocal Related-entry links")

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

    def icon(slug):
        return f'<i class="bi bi-{ICONS[slug]} topic-icon" aria-hidden="true"></i>'

    cards = ["```{=html}", '<div class="topic-grid">']
    for name, slug, desc in THEMES:
        first = desc.split(". ")[0].rstrip(".") + "."
        cards.append(f'<a class="topic-card" href="themes/{slug}.html"><span class="topic-name">{icon(slug)}{esc(name)}</span>'
                     f'<span class="topic-count">{count(name)} entries</span><span class="topic-desc">{esc(first)}</span></a>')
    cards += ["</div>", "```"]
    kcards = ["```{=html}", '<div class="topic-grid kind-grid">']
    for name, slug, plural, desc in KINDS:
        kcards.append(f'<a class="topic-card kind-card" href="kinds/{slug}.html"><span class="topic-name">{icon(slug)}{esc(plural)}</span>'
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
                # "32 · The Statistical Significance Filter": the number is the
                # entry's place in Gelman's list. Titles keep their YAML escapes.
                lines.append(f"            - href: concepts/{e['slug']}.qmd")
                lines.append(f'              text: "{e["order"]} · {e["title"]}"')
    with open(os.path.join(ROOT, "_sidebar.yml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    for name, _, _ in THEMES:
        print(f"{count(name):4d}  {name}")
    for name, *_ in KINDS:
        print(f"{count(kind=name):4d}  {name}")
    print(f"{sum(e['verified'] for e in entries):4d}  verified against the source")


if __name__ == "__main__":
    main()
