# TODO: improvements for the Lexicon Explorer

Roughly in priority order within each section. Check items off as they land.

## Launch

- [ ] Create the public GitHub repository `nelsonamayad/gelman-lexicon-explorer` and push (`_quarto.yml` already points `repo-url`, the navbar icon and the "Edit this page"/"Report an issue" links at it).
- [x] Create the Netlify site `gelman-lexicon-explorer` (done with `quarto publish netlify`, recorded in `_publish.yml`).
- [ ] Add the GitHub secret `NETLIFY_AUTH_TOKEN` so every push to `main` publishes automatically.
- [ ] Optionally buy a custom domain, point it at Netlify and put it in `website.site-url`.
- [ ] Once the site is live, send Andrew Gelman the link. He is the best person to catch misreadings.
- [x] Add a `LICENSE` (MIT for code) and a license section in `about.qmd` and `README.md` (CC BY 4.0 for the explanations; entry names, definitions and quotes remain Gelman's).
- [x] Say on the About page and in the footer that the site is independent and not affiliated with or endorsed by Gelman.
- [x] Check, build and deploy in one workflow: checks on every pull request, deploy on every push to `main`.

## Run R in the page with webR

Today every simulation is Observable JS. Readers who know R would get a lot from editing and running the same simulation in R, right in the page and with nothing to install.

- [x] **Pick the extension.** Chose quarto-live, used as a filter with `engine: markdown`, so nothing beyond Quarto is needed at render time. The options were:
  - [`quarto-webr`](https://github.com/coatless/quarto-webr) (`quarto add coatless/quarto-webr`) gives editable `{webr-r}` code cells.
  - [`quarto-live`](https://github.com/r-wasm/quarto-live) (`quarto add r-wasm/quarto-live`), from the webR team, also supports exercises and hints. It can also *read OJS values*, so a single slider could drive both the OJS plot and an R cell. That makes it the more natural fit for this site.
  - Check whether either one needs R installed at render time (`engine: knitr`). If it does, the GitHub Actions workflow needs an `r-lib/actions/setup-r` step.
- [x] **Pilot on 3–5 entries** where R adds the most. Done for the significance filter, 16, multiple comparisons and mathematical simplicity, as separate pages under `r/`. Mister P is still to do. The original list:
  - [The Statistical Significance Filter](concepts/statistical-significance-filter.qmd): `replicate()` plus `mean(abs(est[sig]))`.
  - [Mister P](concepts/mister-p.qmd): a real multilevel fit with `lme4::glmer` instead of the empirical-Bayes shortcut. Check that lme4 is available in the webR package repository.
  - [Multiple Comparisons](concepts/multiple-comparisons.qmd): `lmer` partial pooling compared with `lm` with no pooling.
  - [16](concepts/sixteen.qmd): a power simulation with `lm(y ~ a * b)`.
  - [Mathematical Simplicity](concepts/mathematical-simplicity.qmd): the golf geometry model fitted with `optim`.
- [x] **R and Python code on every entry.** Every entry's "Show simulation code" block has Observable JS, R (base R) and Python (NumPy and Matplotlib) tabs, from `sims/r/` and `sims/python/`; `_template.qmd` describes the scripts and `scripts/check_code.py` runs them all in CI.
- [x] **Tidyverse style and code annotations for the R scripts.** All 155 scripts restyled with `styler` (tidyverse style, one statement per line, no `T`/`C` variable names) and given Quarto code annotations (`# <n>` markers plus a `# Annotations` trailer that `build_groups.py` turns into the numbered list under the R tab; `check_entries.py` enforces both). Single-letter mathematical symbols such as `X`, `N` and `K` keep their case to match the formulas on the pages.
- [ ] **Run the R tab in the page.** The R scripts are copy-and-run today. A "Run in the browser" button could load webR on demand (only when clicked, to keep pages light) and run the entry's script.
- [ ] Check the default seeds of the multiple-comparisons simulation in all three languages: its empirical-Bayes shortcut ignores the uncertainty in the estimated mean, so for some seeds the multilevel model "confidently" claims all 50 effects (R seed 23 does). The defaults are fine; the slider can reach the bad cases.
- [x] **Keep pages light.** webR downloads tens of MB when a page with R cells opens, so the R versions live on separate pages under `r/` and the entry pages stay instant.
- [ ] **Packages.** Use base R plus packages that exist in the webR repository. Stan-based packages (`rstanarm`, `brms`) won't run in the browser, so offer a "copy this script" button for those.
- [ ] Optionally do the same for Python with [`quarto-pyodide`](https://github.com/coatless-quarto/pyodide) or `quarto-live`'s Pyodide support, for entries where NumPy, SciPy or statsmodels versions help.

## Accuracy of the explanations

- [ ] **Finish source verification.** Run `grep -l "verified: false" concepts/*.qmd` for the current list; each page's `source-note` says why it is unchecked. Most remaining posts are archived on the Wayback Machine, which rate-limits automated reading, so check a few at a time. Two can't be checked from the archive: [dark room / dollar bills](concepts/dark-room-dollar-bills.qmd) (no snapshot) and [Making errors inevitable](concepts/making-errors-inevitable.qmd) (a scanned PDF without a text layer).
- [x] Link the papers cited under "Source" (DOI or arXiv), and add the papers that the source posts point to.
- [x] Second review (`reviews/gelman-lexicon-explorer-review.md`): rewrote the entries that misread their sources (#19, #35, #111, #116, #118), fixed the #44 and #80 simulations, restored missing attributions and context, fixed altered quotations, and added the two entries missing from the list (#154, #155).
- [x] Keep quotation marks for real quotations; set illustrative lines in italics (convention stated on the About page).
- [x] Audit the code of every simulation (bugs found and fixed in 6 pages and in `js/stats.js`).
- [ ] Keep the list in sync: Gelman adds entries. The two newest (#154, #155) quote their posts because no archived copy of the updated list exists; replace their descriptions with his one-line definitions when one is available.
- [x] Show "Report an issue" and "Edit this page" links on every page (`repo-actions` in `_quarto.yml`), so readers can send corrections.
- [x] Add a `verified: true/false` front-matter field (plus optional `source-note:`) and show a "Source check" line on every entry.
- [x] Make "Related entries" links bidirectional (`build_groups.py`) and check that every linked page exists (`check_entries.py`).
- [ ] Watch for new lexicon entries: compare the live or archived list with `concepts/*.qmd` and scaffold missing pages from `_template.qmd`.

## Browsing and navigation

- [ ] Consider splitting "Laws and aphorisms" (60 entries) into jokes about research culture and substantive laws.

- [x] Group entries by theme and by kind (method, principle, fallacy, law or aphorism, advice), with a page for each, home-page cards and a sidebar grouped by theme.
- [ ] Show entry numbers in the sidebar, for example "32 · The Statistical Significance Filter" (`scripts/build_groups.py` already writes `_sidebar.yml`, so it could add `text:` labels).
- [ ] More guided paths besides "Start here": for example *For reviewers*, *For survey researchers* and *For Bayesian beginners*.
- [ ] Tag entries by difficulty (introductory, intermediate, advanced) as a third axis.
- [ ] Add search synonyms (for example "type M" → significance filter, "MRP" → Mister P) through hidden keywords in the front matter.
- [ ] Per-entry social preview images, with the title, definition and a thumbnail of the simulation.

## Simulations

- [x] Give every `Plot.plot` an `ariaLabel` and `ariaDescription` (enforced by `check_entries.py`).
- [ ] **Accessibility.** Check the palette for color-blind readers, make sure sliders are keyboard friendly, and test with a real screen reader. (Done: chart labels, named icon links, a labeled filter box, no heading-order problem on the home page, and chart grays, green and gold darkened to pass 3:1 contrast in both modes.)
- [ ] **Performance.** A few pages run 10^5–10^6 random draws on every slider move. Debounce the inputs or move the heavy loops into a Web Worker, and run simulations only when they scroll into view.
- [ ] A "Reset to defaults" button on every simulation.
- [ ] A "Download this simulation" link that exports the parameters and results as CSV, along with the equivalent R script.

## Engineering

- [x] Move the headless-Chrome page checker into `scripts/check_pages.py` and run it in CI after `quarto render`.
- [x] Hide the code of the import cell, so each simulation shows fewer "Show simulation code" toggles.
- [x] Fix the phone layout of the home-page table (it now scrolls inside its own box).
- [ ] Unit-test `js/stats.js` with Node (distribution means and variances, `ols` against known values, `pnorm` and `qnorm` accuracy).
- [ ] Pin Plot and Inputs versions if Quarto upgrades change their defaults.
- [ ] Optionally add privacy-friendly analytics (for example Plausible) to learn which entries people read.
- [ ] Optionally add a Spanish translation, using Quarto profiles.
