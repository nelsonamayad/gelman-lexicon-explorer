# Andrew Gelman Statistical Lexicon Explorer

**Every entry in Andrew Gelman's [Handy Statistical Lexicon](https://statmodeling.stat.columbia.edu/2009/05/24/handy_statistic/), explained, with an interactive simulation that runs in your browser.**

[![Check and publish](https://github.com/nelsonamayad/gelman-lexicon-explorer/actions/workflows/publish.yml/badge.svg)](https://github.com/nelsonamayad/gelman-lexicon-explorer/actions/workflows/publish.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Visit the site: <https://gelman-lexicon-explorer.netlify.app>**

Since 2009, Andrew Gelman has kept a running list of short, funny names for
"important methods and concepts related to statistics that are not as well
known as they should be": the statistical significance filter, the garden of
forking paths, the kangaroo, the piranha principle, Mister P, and 150 more.
This site is an homage to that list. It gives each of the 155 entries its own
page, so you can read what the idea is, why it matters, and how it works, and
then move the sliders and watch it happen.

> This is an independent study aid. It is not affiliated with, endorsed by or
> reviewed by Andrew Gelman. The entry names and definitions are his; the
> explanations and simulations are ours, and so are any mistakes in them.

## What you'll find

- **155 entries**, one page each, in the order of Gelman's list. Every page has
  the same shape: Gelman's definition, *What it is*, *Why it matters*, *How it
  works*, a simulated example, key takeaways, related entries, and the source.
- **An interactive simulation on every page**, written in
  [Observable JS](https://quarto.org/docs/interactive/ojs/) with seeded random
  numbers, so a given seed always reproduces the same picture. Each one is
  built so that the default settings show the entry's point.
- **The same simulation in three languages.** Under every chart, *Show
  simulation code* has tabs for the Observable JS that runs on the page and for
  R (base R only, with numbered annotations that explain the key lines) and
  Python (NumPy and Matplotlib), ready to copy and run.
- **[Try it in R](https://gelman-lexicon-explorer.netlify.app/r/)**: a few
  simulations rewritten in R that you can edit and run in the browser with
  [webR](https://docs.r-wasm.org/webr/latest/), nothing to install.
- **Ways in.** A twelve-stop [Start here](https://gelman-lexicon-explorer.netlify.app/start-here.html)
  tour; six themes (from *Noise and evidence* to *How science behaves*) and
  five kinds (methods, principles, fallacies, laws and aphorisms, advice); a
  searchable table of everything; and a random-entry button.
- **Source checks.** Each page says whether its explanation was checked
  against the post or paper the entry links to, and where the page goes
  beyond the source it says so.
- **Light and dark mode**, keyboard-operable controls, and accessible names
  and descriptions on every chart.

## Contributing

Corrections are the most useful contribution, especially where a page claims
more than Gelman's source supports. Every page on the site has **Report an
issue** and **Edit this page** links that come straight here.

- **Found a mistake?** [Open an issue](https://github.com/nelsonamayad/gelman-lexicon-explorer/issues)
  with the entry's name and what is wrong.
- **Want to fix it yourself?** Edit the entry under `concepts/` and open a
  pull request. Every pull request is checked automatically (front matter and
  structure, chart labels, links, the R and Python scripts, a full render, and
  a load of every page in a headless browser), so a change can't break a page
  without the check failing first.
- **Adding or rewriting an entry?** Start from `_template.qmd`. The conventions
  (page structure, quotation rules, how the simulations and the R and Python
  scripts are written) are documented in [CLAUDE.md](CLAUDE.md).

## Run it locally

You need [Quarto](https://quarto.org/docs/get-started/) 1.12 or later and
Python 3. The optional checks also use Google Chrome, R, NumPy and Matplotlib.

```bash
git clone https://github.com/nelsonamayad/gelman-lexicon-explorer.git
cd gelman-lexicon-explorer
quarto preview                      # live-reloading local server
```

Before opening a pull request, run the same checks as the workflow:

```bash
python scripts/check_entries.py     # front matter, sections, chart labels, seeds, links, annotations
python scripts/check_code.py        # runs every R and Python script
quarto render                       # builds the site into _site/
python scripts/check_pages.py       # loads every page in headless Chrome
```

After adding an entry or changing an entry's theme, kind, related entries,
simulation cells or scripts, run `python scripts/build_groups.py`: it
regenerates the theme and kind pages, the home-page cards, the sidebar and
each entry's code tabs, and makes related-entry links reciprocal.

## How it's built

- [Quarto](https://quarto.org) renders the site; a single `_brand.yml` holds
  the colors, fonts and light and dark themes.
- Simulations are [Observable JS](https://observablehq.com/documentation/cells/observable-javascript)
  drawn with [Observable Plot](https://observablehq.com/plot/), sharing one
  small library, `js/stats.js`, for seeded random numbers, distributions and
  regression.
- The R scripts follow the [tidyverse style guide](https://style.tidyverse.org)
  and use [Quarto code annotations](https://quarto.org/docs/authoring/code-annotation.html).
  The Python scripts use NumPy and Matplotlib only.
- The *Try it in R* pages use [webR](https://docs.r-wasm.org/webr/latest/)
  through the [quarto-live](https://r-wasm.github.io/quarto-live/) extension.
- GitHub Actions checks every pull request and publishes every push to `main`
  to [Netlify](https://www.netlify.com). Google Analytics loads only after
  consent.

| Path | What it is |
|---|---|
| `concepts/*.qmd` | One page per lexicon entry (follow `_template.qmd`) |
| `sims/r/*.R`, `sims/python/*.py` | R and Python versions of each simulation, shown in the code tabs |
| `js/stats.js` | Shared simulation helpers imported by every entry |
| `r/*.qmd` | The *Try it in R* pages (webR) |
| `themes/*.qmd`, `kinds/*.qmd`, `_sidebar.yml`, `_group-cards.md`, `_kind-cards.md` | Generated by `scripts/build_groups.py`; don't edit by hand |
| `scripts/` | `build_groups.py` and the three checks |
| `_quarto.yml`, `_brand.yml`, `styles.css` | Site structure, brand and styling |
| `.github/workflows/` | Check-and-publish workflow (Netlify) and a manual alternative (Posit Connect Cloud) |
| `reviews/` | Full reviews of the site and what was fixed after each |

## For maintainers: publishing

The workflow in `.github/workflows/publish.yml` renders and publishes to the
Netlify site recorded in `_publish.yml`. It needs one repository secret,
`NETLIFY_AUTH_TOKEN` (a Netlify personal access token); without it, pushes
still run the checks and skip the publish step. Netlify itself never builds
anything (`netlify.toml`). The workflow restores each file's modification
time from git, so every page's "Modified" date reflects its last commit. To
publish by hand, run `quarto publish netlify`.

`.github/workflows/publish-connect-cloud.yml` is a manual-only alternative for
Posit Connect Cloud; its header explains the one-time setup.

## Credits and license

Built by [Nelson Amaya D](https://github.com/nelsonamayad) with Claude Fable
5.1 (Anthropic) through Claude Code. The About page on the site describes how.

- Code (the simulations, `js/stats.js`, the scripts and workflows): [MIT](LICENSE).
- Explanations written for this site: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Entry names, the one-line definitions and the quotations are Andrew
  Gelman's, or those of the other authors named on each page. They are quoted
  for commentary and teaching and remain theirs.
