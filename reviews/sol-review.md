# Sol re-audit of the Gelman Lexicon entries

Reviewed: 2026-11-11 (Europe/Berlin)

## Scope and verdict

This is a fresh audit of all 155 current `concepts/*.qmd` entries, including entries 154 and 155. The live [Handy Statistical Lexicon](https://statmodeling.stat.columbia.edu/2009/05/24/handy_statistic/) was checked for list completeness and its current wording. Source files, generated HTML, the repository checks, a full Quarto build, and headless-browser execution were reviewed.

Overall verdict: **conditional pass**. The previous editorial, chart-label, Related-entry, and seed-policy findings are fixed. The current site builds and all 155 entry pages execute without OJS errors. Four areas remain:

- Two newest descriptions do not yet use the exact wording now visible on the live lexicon.
- Sixteen existing R/Python simulation pairs have not been synchronized into their entry pages.
- Eighteen entries use at least one essential chart-series color below the WCAG 2.1 AA 3:1 non-text contrast threshold in light mode.
- One entry remains explicitly source-unverified because its linked PDF is a scan without extractable text.

Entry outcomes:

- **Pass:** 121
- **A11y contrast:** 15
- **Code tabs:** 14
- **Code tabs + A11y contrast:** 2
- **Source check + A11y contrast:** 1
- **Definition update:** 2

`Pass` means no entry-specific issue was found in metadata, structure, links, OJS source, chart labelling, generated build, or default browser execution. It does not certify every possible slider setting or the runtime behavior of the optional R/Python exports, which could not be executed in the available environment.

## Status of the previous findings

| Previous finding | Re-audit result |
|---|---|
| All plots lacked accessible names/descriptions | **Fixed.** All 164 source `Plot.plot` calls have both fields; all 155 rendered entries drew a labelled chart. |
| Entry 122 overstated what regularization can discard | **Fixed.** The page now says regularization improves ranking on average and that excluded leads are not necessarily false. |
| Entry 145 presented a power law as an empirical implication | **Fixed.** The power-law simulation is repeatedly identified as the site's toy illustration, not evidence about scientific change. |
| Source-verification backlog | **Mostly fixed.** There are 154 `verified: true` entries and one transparent `verified: false` entry (#136). |
| Related-entry links were one-way and some entries had no inbound link | **Fixed.** All 738 links resolve and are reciprocal; every entry has an inbound link. |
| Seed convention lacked a deterministic exception | **Fixed.** The template and checker now require a seed only when random draws are used. |

## Current findings

### Medium - entries 154 and 155 no longer match the live list verbatim

The project convention says each `description` is Gelman's one-line definition verbatim. The live list now includes both additions. Entry 154 should add the opening clause “We learn when stories confound our expectations, but”; entry 155 should use “This is how tech investors have absorbed the prestige of information science.” Their `source-note` values also still say the descriptions quote the linked posts because no archived updated list exists. That note is now stale even if no archive snapshot exists, because the current list is readable.

Affected entries: [The paradox of storytelling](../concepts/paradox-of-storytelling.qmd) and [The transitive property of money](../concepts/transitive-property-of-money.qmd).

### Medium - 16 R/Python code exports are not present on their pages

There are 17 R/Python simulation pairs under `sims/`. Only Kangaroo's generated entry block currently includes its R and Python tabs. A read-only comparison against `sync_sim_code()` found 16 stale entry files, leaving 139 of 155 generated blocks in sync. Running `python scripts/build_groups.py` should expose the existing scripts. CI should also check generated-block consistency so this drift cannot recur.

Affected entries: 10, 14, 17, 23, 24, 33, 34, 64, 75, 82, 86, 97, 98, 118, 119, and 127.

### Medium - 18 charts use series colors below 3:1 contrast in light mode

Against the light background `#fbfaf7`, several colors used for data series do not meet the WCAG 2.1 AA 3:1 threshold for meaningful graphical objects: `#999999` is 2.73:1, green `#5aae61` is 2.63:1, gold `#e6ab02` is 1.97:1, `#bbbbbb` is 1.84:1, and `#cccccc` is 1.54:1. Some multi-series charts also depend on color alone to map marks to legend entries. Use darker colors and add redundant encodings such as dash patterns, symbols, outlines, or direct labels.

Affected entries: 23, 68, 73, 88-90, 92, 102, 119, 123, 125, 131, 133, 135-136, 139, 143, and 151.

The site-level body, secondary text, and link colors pass AA contrast in both light and dark modes. All source controls have labels, and the standard range/radio/checkbox controls are keyboard-operable. This was not a real-screen-reader certification or an exhaustive zoom/reflow test.

### Low - one source remains unverified

[Making errors is inevitable](../concepts/making-errors-inevitable.qmd) is correctly and visibly marked `verified: false`: the linked *Chance* PDF is a scanned image without extractable text. A separate Gelman post supports the core aphorism, but that does not verify the entry against its declared source. This is transparent rather than a hidden defect, but the source-verification objective is not literally complete.

### Low - optional R/Python execution is not covered by the current gate

All 17 Python files pass an AST syntax parse, and all 17 R files pass a simple delimiter check. Full execution was unavailable: the installed Python lacks NumPy/Matplotlib, and no Rscript executable was available. `scripts/check_code.py` is also not run by the publish workflow. Add the required runtimes and this check to CI if the exported code is meant to be a supported feature.

## Verification performed

- Confirmed the live lexicon currently contains 155 entries and the repository has a unique, complete order sequence 1-155.
- Ran `python scripts/check_entries.py`: **155 entries checked, 0 problems**.
- Confirmed required metadata and sections, valid themes/kinds, synchronized categories and source-status callouts, seeded stochastic simulations, no `Math.random`, resolved local links, and reciprocal Related-entry links.
- Counted **164/164** source plots with `ariaLabel` and `ariaDescription`; all source controls include labels.
- Rendered the complete project with Quarto 1.12.1: **176/176 pages built successfully**.
- Loaded all entry pages in headless Chrome with a 10-second virtual-time budget: **155 pages checked, 0 with problems**.
- Compared generated simulation blocks with `sync_sim_code()`: **139/155 in sync**; the 16 mismatches are listed above.
- Checked 17 Python exports for syntax and 17 R exports for balanced delimiters; runtime verification remains limited as described above.

## Entry-by-entry outcomes

| # | Entry | Outcome | Entry-specific note |
|---:|---|---|---|
| 1 | [Mister P](../concepts/mister-p.qmd) | Pass | - |
| 2 | [The Secret Weapon](../concepts/secret-weapon.qmd) | Pass | - |
| 3 | [The Superplot](../concepts/superplot.qmd) | Pass | - |
| 4 | [Institutional decision making](../concepts/institutional-decision-making.qmd) | Pass | - |
| 5 | [The Folk Theorem of Statistical Computing](../concepts/folk-theorem.qmd) | Pass | - |
| 6 | [The Pinch-Hitter Syndrome](../concepts/pinch-hitter-syndrome.qmd) | Pass | - |
| 7 | [Weakly Informative Priors](../concepts/weakly-informative-priors.qmd) | Pass | - |
| 8 | [P-values and U-values](../concepts/p-values-and-u-values.qmd) | Pass | - |
| 9 | [Conservatism](../concepts/conservatism.qmd) | Pass | - |
| 10 | [The Backseat Driver Principle](../concepts/backseat-driver-principle.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 11 | [WWJD](../concepts/wwjd.qmd) | Pass | - |
| 12 | [Theoretical and Applied Statisticians, how to tell them apart](../concepts/theoretical-vs-applied-statisticians.qmd) | Pass | - |
| 13 | [The Fallacy of the One-Sided Bet](../concepts/one-sided-bet.qmd) | Pass | - |
| 14 | [Alabama First](../concepts/alabama-first.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 15 | [The USA Today Fallacy](../concepts/usa-today-fallacy.qmd) | Pass | - |
| 16 | [Second-Order Availability Bias](../concepts/second-order-availability-bias.qmd) | Pass | - |
| 17 | [The "All Else Equal" Fallacy](../concepts/all-else-equal-fallacy.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 18 | [The Self-Cleaning Oven](../concepts/self-cleaning-oven.qmd) | Pass | - |
| 19 | [The Taxonomy of Confusion](../concepts/taxonomy-of-confusion.qmd) | Pass | - |
| 20 | [The Blessing of Dimensionality](../concepts/blessing-of-dimensionality.qmd) | Pass | - |
| 21 | [Scaffolding](../concepts/scaffolding.qmd) | Pass | - |
| 22 | [Ockhamite Tendencies](../concepts/ockhamite-tendencies.qmd) | Pass | - |
| 23 | [Bayesian](../concepts/bayesian.qmd) | Code tabs + A11y contrast | Regenerate the R/Python tabs; one chart series is below 3:1 contrast. |
| 24 | [Bayesians](../concepts/bayesians-are-frequentists.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 25 | [Multiple Comparisons](../concepts/multiple-comparisons.qmd) | Pass | - |
| 26 | [Taking a Model Too Seriously](../concepts/taking-a-model-too-seriously.qmd) | Pass | - |
| 27 | [God is in Every Leaf of Every Tree](../concepts/god-is-in-every-leaf.qmd) | Pass | - |
| 28 | [As They Say in the Stagecoach Business](../concepts/stagecoach-business.qmd) | Pass | - |
| 29 | [Story Time](../concepts/story-time.qmd) | Pass | - |
| 30 | [The Foxhole Fallacy](../concepts/foxhole-fallacy.qmd) | Pass | - |
| 31 | [The Pinocchio Principle](../concepts/pinocchio-principle.qmd) | Pass | - |
| 32 | [The Statistical Significance Filter](../concepts/statistical-significance-filter.qmd) | Pass | - |
| 33 | [Arrow's Other Theorem (weak form)](../concepts/arrows-other-theorem-weak.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 34 | [Arrow's Other Theorem (strong form)](../concepts/arrows-other-theorem-strong.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 35 | [The Ramanujan Principle](../concepts/ramanujan-principle.qmd) | Pass | - |
| 36 | [The Paradox of Philosophizing](../concepts/paradox-of-philosophizing.qmd) | Pass | - |
| 37 | [Defaults](../concepts/defaults.qmd) | Pass | - |
| 38 | [Default, the greatest trick it ever pulled](../concepts/default-greatest-trick.qmd) | Pass | - |
| 39 | [Defaults, once set](../concepts/defaults-once-set.qmd) | Pass | - |
| 40 | [The Methodological Attribution Problem](../concepts/methodological-attribution-problem.qmd) | Pass | - |
| 41 | [The John Yoo Line](../concepts/john-yoo-line.qmd) | Pass | - |
| 42 | [The Chris Rock Effect](../concepts/chris-rock-effect.qmd) | Pass | - |
| 43 | [The Freshman Fallacy](../concepts/freshman-fallacy.qmd) | Pass | - |
| 44 | [The Garden of Forking Paths](../concepts/garden-of-forking-paths.qmd) | Pass | - |
| 45 | [The One-Way Street Fallacy](../concepts/one-way-street-fallacy.qmd) | Pass | - |
| 46 | [The Pluralist's Dilemma](../concepts/pluralists-dilemma.qmd) | Pass | - |
| 47 | [More Vampirical Than Empirical](../concepts/more-vampirical-than-empirical.qmd) | Pass | - |
| 48 | [Statistical Chemotherapy](../concepts/statistical-chemotherapy.qmd) | Pass | - |
| 49 | [Tell Me What You Don't Know](../concepts/tell-me-what-you-dont-know.qmd) | Pass | - |
| 50 | [Salad Tongs](../concepts/salad-tongs.qmd) | Pass | - |
| 51 | [The Edlin Factor](../concepts/edlin-factor.qmd) | Pass | - |
| 52 | [Kangaroo](../concepts/kangaroo.qmd) | Pass | - |
| 53 | [The Speed Racer Principle](../concepts/speed-racer-principle.qmd) | Pass | - |
| 54 | [Uncertainty Interval](../concepts/uncertainty-interval.qmd) | Pass | - |
| 55 | [What would you do if you had all the data?](../concepts/if-you-had-all-the-data.qmd) | Pass | - |
| 56 | [What were you doing before you had any data?](../concepts/before-you-had-any-data.qmd) | Pass | - |
| 57 | [The Time-Reversal Heuristic](../concepts/time-reversal-heuristic.qmd) | Pass | - |
| 58 | [The Status-Reversal Heuristic](../concepts/status-reversal-heuristic.qmd) | Pass | - |
| 59 | [Clarke's Law](../concepts/clarkes-law.qmd) | Pass | - |
| 60 | [The wedding, never about the marriage](../concepts/wedding-not-marriage.qmd) | Pass | - |
| 61 | [The problem with peer review](../concepts/problem-with-peer-review.qmd) | Pass | - |
| 62 | [The "What does not kill my statistical significance makes it stronger" fallacy](../concepts/what-does-not-kill.qmd) | Pass | - |
| 63 | [Reverse Poe](../concepts/reverse-poe.qmd) | Pass | - |
| 64 | [The (Lance) Armstrong Principle](../concepts/armstrong-principle.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 65 | [The Chestertonian Principle](../concepts/chestertonian-principle.qmd) | Pass | - |
| 66 | [The most important aspect of a statistical method](../concepts/what-data-it-uses.qmd) | Pass | - |
| 67 | [The Pandora Principle](../concepts/pandora-principle.qmd) | Pass | - |
| 68 | [The Paradox of Influence](../concepts/paradox-of-influence.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 69 | [Cantor's Corner](../concepts/cantors-corner.qmd) | Pass | - |
| 70 | [Correlation](../concepts/correlation-does-not-imply-correlation.qmd) | Pass | - |
| 71 | [The Javert Paradox](../concepts/javert-paradox.qmd) | Pass | - |
| 72 | [Eureka bias](../concepts/eureka-bias.qmd) | Pass | - |
| 73 | [A picture plus 1000 words](../concepts/picture-plus-1000-words.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 74 | [The Piranha Principle](../concepts/piranha-principle.qmd) | Pass | - |
| 75 | [The Australia principle](../concepts/australia-principle.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 76 | [Just because something is counterintuitive](../concepts/counterintuitive-not-true.qmd) | Pass | - |
| 77 | [Honesty and transparency](../concepts/honesty-and-transparency.qmd) | Pass | - |
| 78 | [Breadcrumbs](../concepts/breadcrumbs.qmd) | Pass | - |
| 79 | [Random in](../concepts/random-in-random-out.qmd) | Pass | - |
| 80 | [16](../concepts/sixteen.qmd) | Pass | - |
| 81 | [The Horse](../concepts/the-horse.qmd) | Pass | - |
| 82 | [The 80% Power Lie](../concepts/80-percent-power-lie.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 83 | [The Causal Identification Kool-Aid](../concepts/causal-identification-kool-aid.qmd) | Pass | - |
| 84 | [Strongest-link Fallacy](../concepts/strongest-link-fallacy.qmd) | Pass | - |
| 85 | [Evidence and Truth](../concepts/evidence-and-truth.qmd) | Pass | - |
| 86 | [Assumptions and Rigor](../concepts/assumptions-and-rigor.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 87 | [Deference Trap](../concepts/deference-trap.qmd) | Pass | - |
| 88 | [Looking for a needle in a pile of needles](../concepts/needle-in-pile-of-needles.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 89 | [Research Incumbency Rule](../concepts/research-incumbency-rule.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 90 | [Mathematical Simplicity](../concepts/mathematical-simplicity.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 91 | [Cheeseburger-snarfing diet gurus](../concepts/cheeseburger-snarfing-diet-gurus.qmd) | Pass | - |
| 92 | [That toothpaste feeling](../concepts/toothpaste-feeling.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 93 | [A bunch of hoops to jump through](../concepts/bunch-of-hoops.qmd) | Pass | - |
| 94 | [Hullman's Theorem](../concepts/hullmans-theorem.qmd) | Pass | - |
| 95 | [McBroom's Law](../concepts/mcbrooms-law.qmd) | Pass | - |
| 96 | [Mistakes](../concepts/mistakes.qmd) | Pass | - |
| 97 | [The Bayesian cringe](../concepts/bayesian-cringe.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 98 | [Basketball, or knitting](../concepts/basketball-or-knitting.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 99 | [Camel that is the likelihood](../concepts/camel-likelihood.qmd) | Pass | - |
| 100 | [If zero is in the neighborhood](../concepts/zero-in-the-neighborhood.qmd) | Pass | - |
| 101 | [sqrt(12^2 + 5^2)](../concepts/sqrt-12-5-13.qmd) | Pass | - |
| 102 | [Freedom](../concepts/freedom-not-user-friendly.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 103 | [Disbelief](../concepts/disbelief.qmd) | Pass | - |
| 104 | [Your closest collaborator](../concepts/closest-collaborator.qmd) | Pass | - |
| 105 | [Brilliance](../concepts/brilliance.qmd) | Pass | - |
| 106 | [Web of Trust](../concepts/web-of-trust.qmd) | Pass | - |
| 107 | [Schoolyard Evolutionary Biology](../concepts/schoolyard-evolutionary-biology.qmd) | Pass | - |
| 108 | [What to include](../concepts/what-to-include.qmd) | Pass | - |
| 109 | [The worst visual display of all time](../concepts/worst-visual-display.qmd) | Pass | - |
| 110 | [Tall-Person Syndrome](../concepts/tall-person-syndrome.qmd) | Pass | - |
| 111 | [Context](../concepts/context.qmd) | Pass | - |
| 112 | [Seeds of its own destruction](../concepts/seeds-of-its-own-destruction.qmd) | Pass | - |
| 113 | [Probability](../concepts/probability.qmd) | Pass | - |
| 114 | [A probability isn't just a number](../concepts/probability-not-just-a-number.qmd) | Pass | - |
| 115 | [When researchers say "guarantee"](../concepts/guarantee-is-assumption.qmd) | Pass | - |
| 116 | [Panglossian Fallacy](../concepts/panglossian-fallacy.qmd) | Pass | - |
| 117 | [Canary variable](../concepts/canary-variable.qmd) | Pass | - |
| 118 | [A chicken](../concepts/a-chicken.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 119 | [Anthropic principle](../concepts/anthropic-principle.qmd) | Code tabs + A11y contrast | Regenerate the R/Python tabs; one chart series is below 3:1 contrast. |
| 120 | [Robustness checks](../concepts/robustness-checks.qmd) | Pass | - |
| 121 | [Theoretical statistics](../concepts/theoretical-statistics.qmd) | Pass | - |
| 122 | [Between regularization and discovery](../concepts/regularization-and-discovery.qmd) | Pass | Previous overstatement is corrected. |
| 123 | [Passive Corruption](../concepts/passive-corruption.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 124 | [Gresham's Law of bad science](../concepts/greshams-law-bad-science.qmd) | Pass | - |
| 125 | [The Click-Through Solution](../concepts/click-through-solution.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 126 | [Marginal](../concepts/marginal.qmd) | Pass | - |
| 127 | [The Analyst's Paradox](../concepts/analysts-paradox.qmd) | Code tabs | R/Python scripts exist but are absent from the generated page block. |
| 128 | [Meritocracy won't happen](../concepts/meritocracy.qmd) | Pass | - |
| 129 | [Until it runs twice](../concepts/until-it-runs-twice.qmd) | Pass | - |
| 130 | [Torment executioner](../concepts/torment-executioner.qmd) | Pass | - |
| 131 | [End of novel. Beginning of job.](../concepts/end-of-novel.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 132 | [In high-dimensional space](../concepts/high-dimensional-space.qmd) | Pass | - |
| 133 | [Preregistration](../concepts/preregistration.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 134 | [Uncertainty](../concepts/uncertainty-greases-commerce.qmd) | Pass | - |
| 135 | [That narrow beach](../concepts/narrow-beach.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 136 | [Making errors is inevitable](../concepts/making-errors-inevitable.qmd) | Source check + A11y contrast | The linked PDF remains unverified; one chart series is below 3:1 contrast. |
| 137 | [Two sides, no vig](../concepts/two-sides-no-vig.qmd) | Pass | - |
| 138 | [The house](../concepts/the-house.qmd) | Pass | - |
| 139 | [Replication and firefighting](../concepts/replication-and-firefighting.qmd) | A11y contrast | Chart lines use low-contrast green/red and depend on color to distinguish the series. |
| 140 | [In a dark room with many of the lights covered up by opaque dollar bills](../concepts/dark-room-dollar-bills.qmd) | Pass | - |
| 141 | [Objects of the class](../concepts/objects-of-the-class.qmd) | Pass | - |
| 142 | [Steelmanning](../concepts/steelmanning.qmd) | Pass | - |
| 143 | [Physics is like Brazil](../concepts/physics-is-like-brazil.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 144 | [The Error-Reversal Heuristic](../concepts/error-reversal-heuristic.qmd) | Pass | - |
| 145 | [Scientific revolutions](../concepts/scientific-revolutions-fractal.qmd) | Pass | Previous empirical overclaim is corrected and the source is marked verified. |
| 146 | [The capacity to be upset](../concepts/capacity-to-be-upset.qmd) | Pass | - |
| 147 | [The year Jesus was born](../concepts/year-jesus-was-born.qmd) | Pass | - |
| 148 | [The Edgelord's Dilemma](../concepts/edgelords-dilemma.qmd) | Pass | - |
| 149 | [The Groovy Grandma Problem](../concepts/groovy-grandma-problem.qmd) | Pass | Source is now marked verified with its limitation disclosed. |
| 150 | [You have no obligation to share your data and code](../concepts/no-obligation-to-share.qmd) | Pass | - |
| 151 | [The combination of originality, ambition, and lack of scruple](../concepts/originality-ambition-scruple.qmd) | A11y contrast | A chart series is below 3:1 contrast in light mode. |
| 152 | [Premature collapsing of the wave function](../concepts/premature-collapse.qmd) | Pass | - |
| 153 | [Noem's Razor](../concepts/noems-razor.qmd) | Pass | - |
| 154 | [The paradox of storytelling](../concepts/paradox-of-storytelling.qmd) | Definition update | Use the exact current live-list definition and update the stale source note. |
| 155 | [The transitive property of money](../concepts/transitive-property-of-money.qmd) | Definition update | Use the exact current live-list definition and update the stale source note. |
