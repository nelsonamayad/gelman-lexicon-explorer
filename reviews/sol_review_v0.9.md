# Sol review v0.9

Reviewed: 2026-11-12 (Europe/Berlin)

## Scope and verdict

This is a fresh review of version 0.9 of the Andrew Gelman Statistical Lexicon Explorer. It covers all 155 current `concepts/*.qmd` entries, all generated simulation-code tabs, the 155 R and 155 Python exports, the full rendered site, browser execution, the current public deployment, and the live [Handy Statistical Lexicon](https://statmodeling.stat.columbia.edu/2009/05/24/handy_statistic/).

Overall verdict: **conditional pass**. The repository is structurally strong and the full static, simulation, render, and browser gates pass. Three content/accessibility issues affect eight entries, one quotation remains independently unconfirmed, and the public homepage does not match the v0.9 source.

Entry outcomes:

- **Pass:** 146
- **Export contrast:** 5
- **Definition update:** 2
- **Source check:** 1
- **Quote check:** 1

`Pass` means no entry-specific issue was found in required metadata and sections, source-code structure, internal links, OJS runtime behavior, chart naming, generated code-tab synchronization, or default browser execution. It does not mean every linked source was downloaded again or every possible control setting was exhaustively tested.

## Findings

### Medium - entries 154 and 155 do not use the live list's exact definitions

The project convention says each front-matter `description` is Gelman's one-line definition verbatim. The current live list now supplies the wording for both additions.

- Entry 154 omits the opening clause “We learn when stories confound our expectations, but”.
- Entry 155 uses a longer sentence from the linked post instead of “This is how tech investors have absorbed the prestige of information science.”

Both `source-note` fields also still say the description quotes the linked post because no archived updated list exists. That no longer explains the choice now that the current list is readable.

Affected entries: [The paradox of storytelling](../concepts/paradox-of-storytelling.qmd) and [The transitive property of money](../concepts/transitive-property-of-money.qmd).

### Medium - five R/Python exports retain the inaccessible pre-fix palette

The browser OJS charts have been corrected, but five pairs of exported R/Python scripts still use `#e6ab02` or `#5aae61`. On Matplotlib/base-R's white background those colors have contrast ratios of approximately 2.06:1 and 2.74:1, below the WCAG 2.1 AA 3:1 threshold for meaningful graphical objects. Use the same corrected `#b8860b` and `#1a9850` colors as the OJS charts, then regenerate the code blocks.

Affected entries: 55, 59, 73, 115, and 140.

### Medium - the public homepage is not the v0.9 homepage in source

The current source and local render contain `Version 0.9, 12 November 2026.`, but a cache-busted fetch of the public Netlify homepage does not contain either the text or the `site-version` class. Public entry pages do contain the new R/Python tabs, annotations, and corrected OJS palette, so the deployment is internally inconsistent rather than wholly stale.

Both current GitHub workflows completed successfully, but the publish step deliberately exits successfully when `NETLIFY_AUTH_TOKEN` is absent. The public job log is not readable without authentication, so a green workflow alone does not prove a publish occurred. The repository TODO still says the secret must be added, but its statement that the live site lacks R/Python tabs is now stale.

### Low - one source remains transparently unverified

[Making errors is inevitable](../concepts/making-errors-inevitable.qmd) is the sole `verified: false` entry. Its callout correctly explains that the declared *Chance* PDF is a scanned image without extractable text. A separate Gelman post supports the aphorism, but that does not verify the page against its declared source.

### Low - one quotation remains on the project's verification TODO

[Arrow's Other Theorem (weak form)](../concepts/arrows-other-theorem-weak.qmd) presents an imagined editor's line as a direct quotation. The project TODO already asks whether it is Gelman's wording. The live source was blocked by its anti-bot challenge and the exact quotation was not independently retrievable through search, so this review cannot close that check.

### Low - three simulations remain expensive on interaction

Garden of Forking Paths, `sqrt(12^2 + 5^2)`, and Theoretical statistics rerun substantial Monte Carlo or regression work on every control change. All completed within the browser check's 10-second virtual-time budget at their defaults. Debouncing or a worker remains a sensible improvement, not a release blocker.

## Accessibility review

- All **164/164** source `Plot.plot` calls have both `ariaLabel` and `ariaDescription`.
- All Observable source controls have labels.
- No legacy low-contrast gray, green, or gold remains in the OJS source.
- Site body, link, and secondary-text colors retain AA contrast in light and dark modes.
- Standard HTML inputs are keyboard-operable; navbar focus-visible styling is present.
- The five exported-script palette mismatches above remain.
- This was not a real NVDA/VoiceOver session, and touch targets and 200% zoom were not exhaustively measured. The prior mobile review found no layout break at 380 px.

## Correctness, security, and maintainability

- No entry uses unseeded `Math.random`; stochastic OJS simulations expose and pass a seed.
- No entry source contains `eval`, `new Function`, `document.write`, insecure external `http://` links, or obvious credential material.
- All R/Python files exist, meet the line/annotation conventions, and are present in their generated tabs.
- A read-only generator comparison found **155/155** simulation-code blocks synchronized.
- The v0.9 GitHub workflow passed entry validation, R/Python execution, rendering, browser checks, and its guarded publish step.
- The latest `main` workflow also completed successfully on 2026-11-12.

## Verification performed

- Confirmed the live lexicon still contains 155 entries and ends with entries 154 and 155.
- Confirmed 155 unique titles and a complete unique order sequence 1-155.
- Ran `python scripts/check_entries.py`: **155 entries checked, 0 problems**.
- Confirmed valid themes/kinds, synchronized categories, exactly three takeaways per entry, 738 reciprocal Related-entry links, and zero entries without an inbound Related link.
- Parsed all 155 Python exports successfully. Local execution lacked NumPy/Matplotlib and R; the successful v0.9 CI run supplies the full execution evidence for all 310 scripts.
- Rendered with Quarto 1.12.1: **176/176 pages built successfully**, including the post-render script.
- Ran the fresh headless-Chrome sweep: **176 pages checked, 0 with problems**.
- Confirmed the worktree was clean before creating this report.

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
| 10 | [The Backseat Driver Principle](../concepts/backseat-driver-principle.qmd) | Pass | - |
| 11 | [WWJD](../concepts/wwjd.qmd) | Pass | - |
| 12 | [Theoretical and Applied Statisticians, how to tell them apart](../concepts/theoretical-vs-applied-statisticians.qmd) | Pass | - |
| 13 | [The Fallacy of the One-Sided Bet](../concepts/one-sided-bet.qmd) | Pass | - |
| 14 | [Alabama First](../concepts/alabama-first.qmd) | Pass | - |
| 15 | [The USA Today Fallacy](../concepts/usa-today-fallacy.qmd) | Pass | - |
| 16 | [Second-Order Availability Bias](../concepts/second-order-availability-bias.qmd) | Pass | - |
| 17 | [The "All Else Equal" Fallacy](../concepts/all-else-equal-fallacy.qmd) | Pass | - |
| 18 | [The Self-Cleaning Oven](../concepts/self-cleaning-oven.qmd) | Pass | - |
| 19 | [The Taxonomy of Confusion](../concepts/taxonomy-of-confusion.qmd) | Pass | - |
| 20 | [The Blessing of Dimensionality](../concepts/blessing-of-dimensionality.qmd) | Pass | - |
| 21 | [Scaffolding](../concepts/scaffolding.qmd) | Pass | - |
| 22 | [Ockhamite Tendencies](../concepts/ockhamite-tendencies.qmd) | Pass | - |
| 23 | [Bayesian](../concepts/bayesian.qmd) | Pass | - |
| 24 | [Bayesians](../concepts/bayesians-are-frequentists.qmd) | Pass | - |
| 25 | [Multiple Comparisons](../concepts/multiple-comparisons.qmd) | Pass | - |
| 26 | [Taking a Model Too Seriously](../concepts/taking-a-model-too-seriously.qmd) | Pass | - |
| 27 | [God is in Every Leaf of Every Tree](../concepts/god-is-in-every-leaf.qmd) | Pass | - |
| 28 | [As They Say in the Stagecoach Business](../concepts/stagecoach-business.qmd) | Pass | - |
| 29 | [Story Time](../concepts/story-time.qmd) | Pass | - |
| 30 | [The Foxhole Fallacy](../concepts/foxhole-fallacy.qmd) | Pass | - |
| 31 | [The Pinocchio Principle](../concepts/pinocchio-principle.qmd) | Pass | - |
| 32 | [The Statistical Significance Filter](../concepts/statistical-significance-filter.qmd) | Pass | - |
| 33 | [Arrow's Other Theorem (weak form)](../concepts/arrows-other-theorem-weak.qmd) | Quote check | The imagined editor quotation remains on the project TODO; automated source access was blocked. |
| 34 | [Arrow's Other Theorem (strong form)](../concepts/arrows-other-theorem-strong.qmd) | Pass | - |
| 35 | [The Ramanujan Principle](../concepts/ramanujan-principle.qmd) | Pass | - |
| 36 | [The Paradox of Philosophizing](../concepts/paradox-of-philosophizing.qmd) | Pass | - |
| 37 | [Defaults](../concepts/defaults.qmd) | Pass | - |
| 38 | [Default, the greatest trick it ever pulled](../concepts/default-greatest-trick.qmd) | Pass | - |
| 39 | [Defaults, once set](../concepts/defaults-once-set.qmd) | Pass | - |
| 40 | [The Methodological Attribution Problem](../concepts/methodological-attribution-problem.qmd) | Pass | - |
| 41 | [The John Yoo Line](../concepts/john-yoo-line.qmd) | Pass | - |
| 42 | [The Chris Rock Effect](../concepts/chris-rock-effect.qmd) | Pass | - |
| 43 | [The Freshman Fallacy](../concepts/freshman-fallacy.qmd) | Pass | - |
| 44 | [The Garden of Forking Paths](../concepts/garden-of-forking-paths.qmd) | Pass | Default passed; interactive changes rerun 1,000 studies across multiple analyses. |
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
| 55 | [What would you do if you had all the data?](../concepts/if-you-had-all-the-data.qmd) | Export contrast | The R/Python plot still uses the former low-contrast gold or green palette. |
| 56 | [What were you doing before you had any data?](../concepts/before-you-had-any-data.qmd) | Pass | - |
| 57 | [The Time-Reversal Heuristic](../concepts/time-reversal-heuristic.qmd) | Pass | - |
| 58 | [The Status-Reversal Heuristic](../concepts/status-reversal-heuristic.qmd) | Pass | - |
| 59 | [Clarke's Law](../concepts/clarkes-law.qmd) | Export contrast | The R/Python plot still uses the former low-contrast gold or green palette. |
| 60 | [The wedding, never about the marriage](../concepts/wedding-not-marriage.qmd) | Pass | - |
| 61 | [The problem with peer review](../concepts/problem-with-peer-review.qmd) | Pass | - |
| 62 | [The "What does not kill my statistical significance makes it stronger" fallacy](../concepts/what-does-not-kill.qmd) | Pass | - |
| 63 | [Reverse Poe](../concepts/reverse-poe.qmd) | Pass | - |
| 64 | [The (Lance) Armstrong Principle](../concepts/armstrong-principle.qmd) | Pass | - |
| 65 | [The Chestertonian Principle](../concepts/chestertonian-principle.qmd) | Pass | - |
| 66 | [The most important aspect of a statistical method](../concepts/what-data-it-uses.qmd) | Pass | - |
| 67 | [The Pandora Principle](../concepts/pandora-principle.qmd) | Pass | - |
| 68 | [The Paradox of Influence](../concepts/paradox-of-influence.qmd) | Pass | - |
| 69 | [Cantor's Corner](../concepts/cantors-corner.qmd) | Pass | - |
| 70 | [Correlation](../concepts/correlation-does-not-imply-correlation.qmd) | Pass | - |
| 71 | [The Javert Paradox](../concepts/javert-paradox.qmd) | Pass | - |
| 72 | [Eureka bias](../concepts/eureka-bias.qmd) | Pass | - |
| 73 | [A picture plus 1000 words](../concepts/picture-plus-1000-words.qmd) | Export contrast | The R/Python plot still uses the former low-contrast gold or green palette. |
| 74 | [The Piranha Principle](../concepts/piranha-principle.qmd) | Pass | - |
| 75 | [The Australia principle](../concepts/australia-principle.qmd) | Pass | - |
| 76 | [Just because something is counterintuitive](../concepts/counterintuitive-not-true.qmd) | Pass | - |
| 77 | [Honesty and transparency](../concepts/honesty-and-transparency.qmd) | Pass | - |
| 78 | [Breadcrumbs](../concepts/breadcrumbs.qmd) | Pass | - |
| 79 | [Random in](../concepts/random-in-random-out.qmd) | Pass | - |
| 80 | [16](../concepts/sixteen.qmd) | Pass | - |
| 81 | [The Horse](../concepts/the-horse.qmd) | Pass | - |
| 82 | [The 80% Power Lie](../concepts/80-percent-power-lie.qmd) | Pass | - |
| 83 | [The Causal Identification Kool-Aid](../concepts/causal-identification-kool-aid.qmd) | Pass | - |
| 84 | [Strongest-link Fallacy](../concepts/strongest-link-fallacy.qmd) | Pass | - |
| 85 | [Evidence and Truth](../concepts/evidence-and-truth.qmd) | Pass | - |
| 86 | [Assumptions and Rigor](../concepts/assumptions-and-rigor.qmd) | Pass | - |
| 87 | [Deference Trap](../concepts/deference-trap.qmd) | Pass | - |
| 88 | [Looking for a needle in a pile of needles](../concepts/needle-in-pile-of-needles.qmd) | Pass | - |
| 89 | [Research Incumbency Rule](../concepts/research-incumbency-rule.qmd) | Pass | - |
| 90 | [Mathematical Simplicity](../concepts/mathematical-simplicity.qmd) | Pass | - |
| 91 | [Cheeseburger-snarfing diet gurus](../concepts/cheeseburger-snarfing-diet-gurus.qmd) | Pass | - |
| 92 | [That toothpaste feeling](../concepts/toothpaste-feeling.qmd) | Pass | - |
| 93 | [A bunch of hoops to jump through](../concepts/bunch-of-hoops.qmd) | Pass | - |
| 94 | [Hullman's Theorem](../concepts/hullmans-theorem.qmd) | Pass | - |
| 95 | [McBroom's Law](../concepts/mcbrooms-law.qmd) | Pass | - |
| 96 | [Mistakes](../concepts/mistakes.qmd) | Pass | - |
| 97 | [The Bayesian cringe](../concepts/bayesian-cringe.qmd) | Pass | - |
| 98 | [Basketball, or knitting](../concepts/basketball-or-knitting.qmd) | Pass | - |
| 99 | [Camel that is the likelihood](../concepts/camel-likelihood.qmd) | Pass | - |
| 100 | [If zero is in the neighborhood](../concepts/zero-in-the-neighborhood.qmd) | Pass | - |
| 101 | [sqrt(12^2 + 5^2)](../concepts/sqrt-12-5-13.qmd) | Pass | Default passed; each interaction runs four 20,000-draw Monte Carlo calculations. |
| 102 | [Freedom](../concepts/freedom-not-user-friendly.qmd) | Pass | - |
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
| 115 | [When researchers say "guarantee"](../concepts/guarantee-is-assumption.qmd) | Export contrast | The R/Python plot still uses the former low-contrast gold or green palette. |
| 116 | [Panglossian Fallacy](../concepts/panglossian-fallacy.qmd) | Pass | - |
| 117 | [Canary variable](../concepts/canary-variable.qmd) | Pass | - |
| 118 | [A chicken](../concepts/a-chicken.qmd) | Pass | - |
| 119 | [Anthropic principle](../concepts/anthropic-principle.qmd) | Pass | - |
| 120 | [Robustness checks](../concepts/robustness-checks.qmd) | Pass | - |
| 121 | [Theoretical statistics](../concepts/theoretical-statistics.qmd) | Pass | Default passed; each interaction refits 1,000 simulated regressions. |
| 122 | [Between regularization and discovery](../concepts/regularization-and-discovery.qmd) | Pass | The earlier overstatement is corrected. |
| 123 | [Passive Corruption](../concepts/passive-corruption.qmd) | Pass | - |
| 124 | [Gresham's Law of bad science](../concepts/greshams-law-bad-science.qmd) | Pass | - |
| 125 | [The Click-Through Solution](../concepts/click-through-solution.qmd) | Pass | - |
| 126 | [Marginal](../concepts/marginal.qmd) | Pass | - |
| 127 | [The Analyst's Paradox](../concepts/analysts-paradox.qmd) | Pass | - |
| 128 | [Meritocracy won't happen](../concepts/meritocracy.qmd) | Pass | - |
| 129 | [Until it runs twice](../concepts/until-it-runs-twice.qmd) | Pass | - |
| 130 | [Torment executioner](../concepts/torment-executioner.qmd) | Pass | - |
| 131 | [End of novel. Beginning of job.](../concepts/end-of-novel.qmd) | Pass | - |
| 132 | [In high-dimensional space](../concepts/high-dimensional-space.qmd) | Pass | - |
| 133 | [Preregistration](../concepts/preregistration.qmd) | Pass | - |
| 134 | [Uncertainty](../concepts/uncertainty-greases-commerce.qmd) | Pass | - |
| 135 | [That narrow beach](../concepts/narrow-beach.qmd) | Pass | - |
| 136 | [Making errors is inevitable](../concepts/making-errors-inevitable.qmd) | Source check | The declared scanned-PDF source remains transparently unverified. |
| 137 | [Two sides, no vig](../concepts/two-sides-no-vig.qmd) | Pass | - |
| 138 | [The house](../concepts/the-house.qmd) | Pass | - |
| 139 | [Replication and firefighting](../concepts/replication-and-firefighting.qmd) | Pass | - |
| 140 | [In a dark room with many of the lights covered up by opaque dollar bills](../concepts/dark-room-dollar-bills.qmd) | Export contrast | The R/Python plot still uses the former low-contrast gold or green palette. |
| 141 | [Objects of the class](../concepts/objects-of-the-class.qmd) | Pass | - |
| 142 | [Steelmanning](../concepts/steelmanning.qmd) | Pass | - |
| 143 | [Physics is like Brazil](../concepts/physics-is-like-brazil.qmd) | Pass | - |
| 144 | [The Error-Reversal Heuristic](../concepts/error-reversal-heuristic.qmd) | Pass | - |
| 145 | [Scientific revolutions](../concepts/scientific-revolutions-fractal.qmd) | Pass | The power-law construction is explicitly a toy illustration. |
| 146 | [The capacity to be upset](../concepts/capacity-to-be-upset.qmd) | Pass | - |
| 147 | [The year Jesus was born](../concepts/year-jesus-was-born.qmd) | Pass | - |
| 148 | [The Edgelord's Dilemma](../concepts/edgelords-dilemma.qmd) | Pass | - |
| 149 | [The Groovy Grandma Problem](../concepts/groovy-grandma-problem.qmd) | Pass | - |
| 150 | [You have no obligation to share your data and code](../concepts/no-obligation-to-share.qmd) | Pass | - |
| 151 | [The combination of originality, ambition, and lack of scruple](../concepts/originality-ambition-scruple.qmd) | Pass | - |
| 152 | [Premature collapsing of the wave function](../concepts/premature-collapse.qmd) | Pass | - |
| 153 | [Noem's Razor](../concepts/noems-razor.qmd) | Pass | - |
| 154 | [The paradox of storytelling](../concepts/paradox-of-storytelling.qmd) | Definition update | Use the exact current live-list definition and update the stale source note. |
| 155 | [The transitive property of money](../concepts/transitive-property-of-money.qmd) | Definition update | Use the exact current live-list definition and update the stale source note. |

