# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The **Andrew Gelman Statistical Lexicon Explorer**: a Quarto website with one page for each of the 155 entries in Andrew Gelman's [Handy Statistical Lexicon](https://statmodeling.stat.columbia.edu/2009/05/24/handy_statistic/), as of November 2026: 153 from the March 2026 archived version of the post, plus two added by August 2026 (#154, #155) whose descriptions quote their linked posts, because no archived copy of the updated list exists. Each page explains the concept and runs an interactive simulation written in Observable JS (OJS) in the browser. No R or Python runs at render time; the few "Try it in R" pages run R in the reader's browser with webR. It is independent and not affiliated with Gelman, and the footer and About page say so. GitHub Actions checks every pull request and publishes every push to `main` to Netlify; Posit Connect Cloud is a manual alternative. The repository is `github.com/nelsonamayad/gelman-lexicon-explorer`. Planned improvements, including in-page R with webR, are in `TODO.md`.

## Commands

```bash
quarto preview                          # live-reloading dev server
quarto render                           # full build into _site/
quarto render concepts/<slug>.qmd       # re-render a single page
python scripts/build_groups.py          # regenerate theme/kind pages, cards, sidebar, links
python scripts/check_entries.py         # static checks on every entry (run before committing)
python scripts/check_pages.py           # load every built page in headless Chrome (after quarto render)
python scripts/check_pages.py _site concepts/<slug>.html --readouts   # one page, with its readout text
```

Run `scripts/build_groups.py` after adding an entry or changing any entry's `theme`, `kind`, `verified` or Related entries. It regenerates `themes/*.qmd`, `kinds/*.qmd`, the home-page cards (`_group-cards.md`, `_kind-cards.md`) and the sidebar (`_sidebar.yml`), and it syncs each entry's `categories`, its "Filed under" and "Source check" lines, and makes every Related-entry link reciprocal (if A lists B, B lists A). Don't edit those generated files by hand.

`quarto render` only checks OJS syntax. Runtime errors, such as a misspelled helper or a bad Plot option, show up only in the browser. `scripts/check_pages.py` serves `_site/` locally, loads each page in headless Chrome and fails on any `observablehq--error` box or entry page without a labelled chart; `--readouts` prints the text under each chart. CI runs it after `quarto render`. Don't re-render while it is running, because it will report missing files.

## Structure

- `_quarto.yml`: site structure: the navbar (Themes and Kinds menus, Start here, Random entry, About), search, footer, social cards, dates and `metadata-files: [_sidebar.yml]`. The generated sidebar groups entries by theme in Gelman's order, so previous/next links step through a theme. `website.site-url` is the Netlify URL (`https://gelman-lexicon-explorer.netlify.app`). `repo-url` and `repo-actions: [edit, issue]` add "Edit this page" and "Report an issue" links to every page.
- `_analytics.html` (Google Analytics, loaded only after consent through Quarto's `cookie-consent` banner; don't use Quarto's `google-analytics` option, which loads Google's script before consent), `_a11y.html` (accessible names for icon links and the listing filter), `scripts/post_render.py` (run by Quarto after each render; strips the ES6 polyfill), `assets/social-card.png` (1200x630 preview image; `canonical-url`, `twitter-card: summary_large_image` and a pinned MathJax are set in `_quarto.yml`).
- `_brand.yml`: colors (with light/dark values, which gives the dark-mode toggle), Google fonts and the logo (`assets/logo.svg`). `styles.css` adds font fallback stacks and the layout for the home page and its theme and kind cards.
- `index.qmd`: hero section, theme cards and kind cards (included from the generated `_group-cards.md` and `_kind-cards.md`), and the full table listing of `concepts/` sorted by `order`.
- `themes/*.qmd` (six themes, entries split into sections by kind) and `kinds/*.qmd` (five kinds, split by theme): generated grid listings that filter on the custom `theme` and `kind` fields with `include:`. Edit `scripts/build_groups.py`, not these files.
- `start-here.qmd` (a curated tour), `random.qmd` (picks a random entry from `listings.json` at runtime), `404.qmd` and `about.qmd`.
- `_template.qmd`: the required page structure (not rendered, because of the leading underscore). New or rewritten entries should follow it.
- `concepts/<slug>.qmd`: one file per lexicon entry.
- `r/<slug>.qmd` and `r/index.qmd`: "Try it in R" pilot pages (statistical-significance-filter, sixteen, multiple-comparisons, mathematical-simplicity). Each has editable `{webr}` cells that run R in the browser through the vendored quarto-live extension (`_extensions/r-wasm/live/`, installed with `quarto add r-wasm/quarto-live`). Front matter: `engine: markdown` (so no R, Python or Jupyter is needed at render time), `filters: [live]`, `ojs-engine: true`, `sidebar: false`, `toc: false` and `webr: cell-options: autorun: true`. R pages are kept separate from entries because webR downloads tens of MB when the page opens. The matching entry links to its R page with a "**Try it in R.**" line at the end of its Simulated example section. Use base R where possible: every extra package is another download.
- `js/stats.js`: shared simulation helpers, imported on every page with `import {...} from "../js/stats.js"`. It provides a seeded RNG (`rng(seed)` returns a uniform generator with `.normal`, `.normals`, `.binomial`, `.poisson`, `.gamma`, `.beta`, `.t`, `.lognormal` and others attached), summaries (`mean`, `sd`, `quantile`, `cor`), `pnorm`/`qnorm`/`dnorm`, `pt` (Student t CDF), `pValue(est, se, df)` (t reference when `df` is given), `normalPosterior`, `lm` (simple regression), `ols` (multiple regression with SEs), `ridge` and `twoGroup` (Welch t test). `fmt` never prints "-0.00" and shows "–" for NaN. Add a helper here rather than copying it into pages.
- `.github/workflows/publish.yml`: on pull requests and pushes to `main`, restores file modification times from git (for the "Modified" dates), runs `check_entries.py`, renders with Quarto 1.12.1 and runs `check_pages.py`. On pushes to `main` it then runs `quarto publish netlify --no-render --no-prompt --no-browser`, which updates the site recorded in the committed `_publish.yml` (secret `NETLIFY_AUTH_TOKEN`; without it the step is skipped with a warning). `netlify.toml` stops Netlify from running its own builds.
- `.github/workflows/publish-connect-cloud.yml`: manual-only alternative that runs `quarto publish posit-connect-cloud --no-prompt --no-browser`. It needs a committed `_publish.yml` (from a first manual publish) and the secrets `POSIT_CONNECT_CLOUD_ACCESS_TOKEN`, `POSIT_CONNECT_CLOUD_REFRESH_TOKEN` and `POSIT_CONNECT_CLOUD_ACCOUNT_ID`. Quarto's Connect Cloud publisher rejects `--token`.
- Authors are Nelson Amaya D (github.com/nelsonamayad) and Claude Opus 5.5. They are credited only on the About page (its `author` field and its "How this site was built" section), not on the home page, entry pages or footer. Every page has `date` (published, set in its front matter) and `date-modified: last-modified` (set site-wide in `_quarto.yml`). New pages need a `date:` line. License: MIT for code (`LICENSE`), CC BY 4.0 for the explanations; entry names, definitions and quotes remain Gelman's (see `about.qmd`).
- `project.render` is limited to `**/*.qmd`, so `README.md`, `TODO.md` and `CLAUDE.md` are never published.

## Page conventions

Front matter: `title` (the entry name), `date` (published), `description` (Gelman's definition, verbatim), `order` (1-based position in his list), `theme` (one of six) and `kind` (one of five), both listed in `_template.qmd` and `scripts/build_groups.py`, `categories` (always `[theme, kind]`, kept in sync by the script), `source` (the URL the entry links to in the original list), `verified` (`true` once the explanation has been checked against the source, otherwise `false`) and an optional `source-note:` explaining how or why not. Under "Source", link papers with a DOI (`https://doi.org/...`) or arXiv URL, looked up through the Crossref or arXiv API rather than from memory. `build_groups.py` refuses entries without `verified` and turns these fields into a visible "Source check" line in the callout, so the verification status is auditable from the front matter.

Body sections, in order: source callout (with the generated "Filed under" line), What it is, Why it matters, How it works, Simulated example, Key takeaways, Related entries, Source. In the simulation: import helpers (in a cell with `//| echo: false`, so readers see fewer code toggles), then `viewof` controls (including a "Random seed" slider passed to `rng(seed)` whenever the simulation uses random draws; deterministic models, such as the Javert Paradox or McBroom's Law, have no seed control), then pure computation, then `Plot.plot`, then a readout `html\`<div class="sim-readout">${md\`...\`}</div>\`` cell with `//| echo: false`.

**Quotations.** Quotation marks are only for words someone actually said or wrote (Gelman, other named people, proverbs, film lines). Hypothetical lines that illustrate a point go in *italics*, never in quotation marks; `about.qmd` states this convention. When the explanation goes beyond the source, say so ("our reading", "a toy model, our own") and add a `source-note`.

**Accuracy against the source.** "What it is" should reflect what Gelman's source post actually says, with short quotes where possible. Several entries are not what their names suggest. For example, "Uncertainty: it greases the wheels of commerce" is about adding an error term so a sampler can move, and "Seeds of its own destruction" is about histograms that show their own noise. The blog and its JSON API block automated requests (don't work around that, for example with a browser user agent), so check posts through Wayback Machine snapshots, paced at a request a minute or so because the archive rate-limits (the CDX API at `web.archive.org/cdx/search/cdx`, then `web.archive.org/web/<timestamp>id_/<url>`). Posts from 2004–2009 are often archived under `andrewgelman.com` with the day in the path. For aphorism-style entries about research culture, the simulation is an explicitly labelled toy model of the mechanism. Never claim more about Gelman's argument than the source supports.

## OJS pitfalls found while building

- Never name a cell `window`, `width`, `document` or any other browser or Observable-stdlib global. `window` fails to parse.
- A cell cannot reference itself, so recursive helpers defined as cells fail with "circular definition".
- Every `Plot.plot({...})` must start with `ariaLabel:` (entry title plus chart name) and `ariaDescription:` (axes, and a pointer to the text summary under the chart). Screen readers depend on them, and `check_entries.py` enforces it.
- Use `"currentColor"` rather than `"black"` for reference lines and text in Plot, so they stay visible in dark mode.
- Defaults matter: every simulation's default slider values and seed should visibly demonstrate the entry's point. Check the readout text after changing anything.
- When scripting edits that touch LaTeX, use raw strings. `\t` and `\f` in `\theta` and `\frac` otherwise become control characters.
- Raw HTML blocks in markdown (like the home-page cards) should go in a single ```` ```{=html} ```` block, or Pandoc wraps them in paragraphs.
