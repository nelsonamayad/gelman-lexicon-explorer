"""Regenerate the topic pages and the home-page topic cards.

Run from the project root after adding entries or changing an entry's
`categories`:

    python scripts/build_topics.py

It writes topics/<slug>.qmd (one listing page per topic) and _topic-cards.md,
which index.qmd pulls in with {{< include _topic-cards.md >}}. The topic list
below is the fixed category set from _template.qmd, in display order.
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOPICS = [
    ("Bayesian inference", "bayesian-inference",
     "Priors, posteriors, partial pooling and what Bayesian probabilities mean. "
     "Entries about using prior information well, and about where Bayesian methods help and where they mislead."),
    ("Significance & noise", "significance-and-noise",
     "What happens when noisy data meet the p < 0.05 threshold: exaggerated estimates, wrong signs, "
     "forking paths and false discoveries. The core of the replication crisis, in simulations."),
    ("Causal inference", "causal-inference",
     "Experiments, observational studies, identification strategies and what they can and can't tell you about cause and effect."),
    ("Modeling workflow", "modeling-workflow",
     "How to build, check, expand and trust statistical models in practice: fake-data simulation, "
     "scaffolding, model checking and knowing when to stop."),
    ("Statistical graphics", "statistical-graphics",
     "Making graphs that show the data honestly and help readers compare: sort orders, axes, superplots and layered displays."),
    ("Surveys & MRP", "surveys-and-mrp",
     "Turning unrepresentative samples into population estimates with multilevel regression and "
     "poststratification, and the ways adjustment can still fail."),
    ("Research culture", "research-culture",
     "How incentives, peer review, publication and criticism shape what gets believed. "
     "Many of these entries are aphorisms, illustrated with toy models."),
    ("Reasoning & fallacies", "reasoning-and-fallacies",
     "Recurring errors in reasoning about data, evidence and people, with a simulation showing how each one misleads."),
    ("Philosophy of statistics", "philosophy-of-statistics",
     "What probability means, why defaults matter, and how to hold a statistical philosophy while respecting others."),
    ("Communication", "communication",
     "Writing, explaining and presenting statistical results: words, numbers, jargon and context."),
    ("Computing", "computing",
     "Statistical computing and software: convergence, typical sets, self-testing code and reproducibility."),
]


def main():
    names = {t[0] for t in TOPICS}
    counts = {t[0]: 0 for t in TOPICS}
    for path in glob.glob(os.path.join(ROOT, "concepts", "*.qmd")):
        text = open(path, encoding="utf-8").read()
        m = re.search(r"^categories: \[(.*)\]", text, re.M)
        if not m:
            raise SystemExit(f"{path}: no categories line")
        for cat in (c.strip() for c in m.group(1).split(",")):
            if cat not in names:
                raise SystemExit(f"{path}: unknown category {cat!r}")
            counts[cat] += 1

    os.makedirs(os.path.join(ROOT, "topics"), exist_ok=True)
    for name, slug, desc in TOPICS:
        page = f'''---
title: "{name}"
date: 2026-11-11
subtitle: "{counts[name]} entries"
description: "{desc}"
sidebar: false
toc: false
listing:
  contents: "../concepts/*.qmd"
  type: grid
  sort: "order"
  sort-ui: [order, title]
  filter-ui: true
  categories: false
  include:
    categories: "{name}"
  fields: [title, description]
  grid-columns: 3
  page-size: 60
---

{desc}

Entries are listed in the order they appear in Gelman's list. See [all topics](../index.qmd#topics) or [browse every entry](../index.qmd#all-entries).
'''
        with open(os.path.join(ROOT, "topics", f"{slug}.qmd"), "w", encoding="utf-8") as f:
            f.write(page)

    cards = ['```{=html}', '<div class="topic-grid">']
    for name, slug, desc in TOPICS:
        first = desc.split(". ")[0].rstrip(".") + "."
        first = first.replace("&", "&amp;").replace("<", "&lt;")
        cards.append(
            f'<a class="topic-card" href="topics/{slug}.html">'
            f'<span class="topic-name">{name.replace("&", "&amp;")}</span>'
            f'<span class="topic-count">{counts[name]} entries</span>'
            f'<span class="topic-desc">{first}</span></a>'
        )
    cards.append("</div>")
    cards.append("```")
    with open(os.path.join(ROOT, "_topic-cards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cards) + "\n")

    for name, _, _ in TOPICS:
        print(f"{counts[name]:4d}  {name}")


if __name__ == "__main__":
    main()
