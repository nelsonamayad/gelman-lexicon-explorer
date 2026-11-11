# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The **Andrew Gelman Statistical Lexicon Explorer**: a Quarto website with one page for each of the 153 entries in Andrew Gelman's [Handy Statistical Lexicon](https://statmodeling.stat.columbia.edu/2009/05/24/handy_statistic/), as of the March 2026 archived version of the post. Each page explains the concept and runs an interactive simulation written in Observable JS (OJS) in the browser. No R or Python runs at render time. The site is published to Posit Connect Cloud, with Netlify as a manual alternative. Planned improvements, including in-page R with webR, are in `TODO.md`.

## Commands

```bash
quarto preview                          # live-reloading dev server
quarto render                           # full build into _site/
quarto render concepts/<slug>.qmd       # re-render a single page
python scripts/build_groups.py          # regenerate theme/kind pages, cards, sidebar
```

Run `scripts/build_groups.py` after adding an entry or changing any entry's `theme` or `kind`. It regenerates `themes/*.qmd`, `kinds/*.qmd`, the home-page cards (`_group-cards.md`, `_kind-cards.md`) and the sidebar (`_sidebar.yml`), and it syncs each entry's `categories` and its "Filed under" line. Don't edit those generated files by hand.

`quarto render` only checks OJS syntax. Runtime errors, such as a misspelled helper or a bad Plot option, show up only in the browser. To verify a page, open it in `quarto preview` and look for red OJS error boxes, or load the built HTML in headless Chrome (`chrome --headless=new --virtual-time-budget=15000 --dump-dom <url>` against a local HTTP server on `_site/`) and grep the DOM for `observablehq--error`. Don't re-render while such a check is running, because it will report missing files.

## Structure

- `_quarto.yml`: site structure: the navbar (Themes and Kinds menus, Start here, Random entry, About), search, footer, social cards, dates and `metadata-files: [_sidebar.yml]`. The generated sidebar groups entries by theme in Gelman's order, so previous/next links step through a theme. `website.site-url` is commented out until the published URL is known.
- `_brand.yml`: colors (with light/dark values, which gives the dark-mode toggle), Google fonts and the logo (`assets/logo.svg`). `styles.css` adds font fallback stacks and the layout for the home page and its theme and kind cards.
- `index.qmd`: hero section, theme cards and kind cards (included from the generated `_group-cards.md` and `_kind-cards.md`), and the full table listing of `concepts/` sorted by `order`.
- `themes/*.qmd` (six themes, entries split into sections by kind) and `kinds/*.qmd` (five kinds, split by theme): generated grid listings that filter on the custom `theme` and `kind` fields with `include:`. Edit `scripts/build_groups.py`, not these files.
- `start-here.qmd` (a curated tour), `random.qmd` (picks a random entry from `listings.json` at runtime), `404.qmd` and `about.qmd`.
- `_template.qmd`: the required page structure (not rendered, because of the leading underscore). New or rewritten entries should follow it.
- `concepts/<slug>.qmd`: one file per lexicon entry.
- `js/stats.js`: shared simulation helpers, imported on every page with `import {...} from "../js/stats.js"`. It provides a seeded RNG (`rng(seed)` returns a uniform generator with `.normal`, `.normals`, `.binomial`, `.poisson`, `.gamma`, `.beta`, `.t`, `.lognormal` and others attached), summaries (`mean`, `sd`, `quantile`, `cor`), `pnorm`/`qnorm`/`dnorm`, `pValue`, `normalPosterior`, `lm` (simple regression), `ols` (multiple regression with SEs), `ridge` and `twoGroup`. Add a helper here rather than copying it into pages.
- `.github/workflows/publish.yml`: on every push to `main`, restores file modification times from git (for the "Modified" dates), then runs `quarto publish posit-connect-cloud --no-prompt --no-browser` with Quarto 1.10.11. It needs a committed `_publish.yml` (created by the first manual `quarto publish posit-connect-cloud`) and the secrets `POSIT_CONNECT_CLOUD_ACCESS_TOKEN`, `POSIT_CONNECT_CLOUD_REFRESH_TOKEN` and `POSIT_CONNECT_CLOUD_ACCOUNT_ID`. Quarto's Connect Cloud publisher rejects `--token`.
- `.github/workflows/publish-netlify.yml`: manual-only alternative deploy to Netlify (`NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID`). `netlify.toml` stops Netlify from running its own builds.
- Authors are Nelson Amaya D (github.com/nelsonamayad) and Claude Opus 5.5, credited in the footer and in the `author` field of `index.qmd` and `about.qmd`. Every page has `date` (published, set in its front matter) and `date-modified: last-modified` (set site-wide in `_quarto.yml`). New pages need a `date:` line.
- `project.render` is limited to `**/*.qmd`, so `README.md`, `TODO.md` and `CLAUDE.md` are never published.

## Page conventions

Front matter: `title` (the entry name), `date` (published), `description` (Gelman's definition, verbatim), `order` (1-based position in his list), `theme` (one of six) and `kind` (one of five), both listed in `_template.qmd` and `scripts/build_groups.py`, `categories` (always `[theme, kind]`, kept in sync by the script), and `source` (the URL the entry links to in the original list).

Body sections, in order: source callout (with the generated "Filed under" line), What it is, Why it matters, How it works, Simulated example, Key takeaways, Related entries, Source. In the simulation: import helpers, then `viewof` controls (always including a "Random seed" slider), then pure computation, then `Plot.plot`, then a readout `html\`<div class="sim-readout">${md\`...\`}</div>\`` cell with `//| echo: false`.

**Accuracy against the source.** "What it is" should reflect what Gelman's source post actually says, with short quotes where possible. Several entries are not what their names suggest. For example, "Uncertainty: it greases the wheels of commerce" is about adding an error term so a sampler can move, and "Seeds of its own destruction" is about histograms that show their own noise. The blog blocks automated requests, so check posts through Wayback Machine snapshots (the CDX API at `web.archive.org/cdx/search/cdx`, then `web.archive.org/web/<timestamp>id_/<url>`). Posts from 2004–2009 are often archived under `andrewgelman.com` with the day in the path. For aphorism-style entries about research culture, the simulation is an explicitly labelled toy model of the mechanism. Never claim more about Gelman's argument than the source supports.

## OJS pitfalls found while building

- Never name a cell `window`, `width`, `document` or any other browser or Observable-stdlib global. `window` fails to parse.
- A cell cannot reference itself, so recursive helpers defined as cells fail with "circular definition".
- Use `"currentColor"` rather than `"black"` for reference lines and text in Plot, so they stay visible in dark mode.
- Defaults matter: every simulation's default slider values and seed should visibly demonstrate the entry's point. Check the readout text after changing anything.
- When scripting edits that touch LaTeX, use raw strings. `\t` and `\f` in `\theta` and `\frac` otherwise become control characters.
- Raw HTML blocks in markdown (like the home-page cards) should go in a single ```` ```{=html} ```` block, or Pandoc wraps them in paragraphs.
