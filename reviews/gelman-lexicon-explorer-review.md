# Gelman Statistical Lexicon Explorer: full review

Site: https://gelman-lexicon-explorer.netlify.app/ · Reviewed 11 November 2026 · 168 pages (home, About, Start here, Random, 6 themes, 5 kinds, 153 entries)

## 1. Summary

- **Names, definitions and links are faithful.** All 153 titles, definitions and source links match Gelman's live lexicon word for word. The only difference is #74, where the site silently fixes his typo ("Pinciple").
- **The list is out of date.** Gelman's live post (last modified 19 August 2026) has 155 entries. Two are missing from the site.
- **Two flagship simulations are wrong.** #44 (Garden of Forking Paths) simulates fishing while saying it doesn't. #80 (16) has a factor-of-two coding error, so its chart shows a 4× gap while its text says 16×. Both are on the Start here tour.
- **Five entries misread the source:** #19, #35, #111, #116, #118. Two of them (#111, #118) carry the "✓ checked against the source" badge.
- **The source-check badge is unreliable in both directions.** 35 pages say "not verified", including 5 of the 12 tour stops, yet 34 of them link to blog posts that are live. Several "✓" pages contradict their source.
- **About 15 entries drop an attribution or the context** that Gelman's post gives (for example #30 Breiman, #102 Margossian, #131 Clute).
- **One source link is dead** (#140) and 41 use `http://`.
- **Site-wide gaps:** Google Analytics with no privacy notice, no licence or permission statement, several accessibility gaps, an index table that doesn't reflow on phones, and missing canonical/social metadata.

## 2. What was checked, and how

| Scope | Pages | Method | Coverage |
|---|---|---|---|
| Home, About, Start here, Random | 4 | Read in full; HTML inspected | Complete |
| Theme and kind pages | 11 | Text, section counts and links checked by script | Complete |
| Entry titles, definitions, source links | 153 | Compared by script with Gelman's live lexicon post | Complete |
| Source links resolve | 145 blog links | Each fetched from the blog's own domain or looked up in its API | Complete; 8 non-blog links (7 PDFs, 1 Slate) not tested |
| Entry explanations ("What it is", "How it works") | 153 | Read by me | "What it is" for all 153; "How it works" in full for 1–30, and wherever it contains maths for 31–153 |
| "Why it matters", "Key takeaways" | 153 | Scanned by script for quotations only | Not read line by line |
| Quotations | 104 long quotes | Each searched for in the linked post | Complete where the post text was retrievable |
| Explanation versus source post | 153 | Source text read for 36 entries (list in section 9) | Partial |
| Simulations run | 153 | Each page loaded; errors and default read-outs collected | Complete; every default read-out read |
| Simulation code | 153 | Line-by-line audit | 12 pages (the Start here tour) plus `js/stats.js` |
| Mobile layout | 5 pages | Rendered at 380 px | Sample only |

## 3. Corrections to my first report

The first report was based on the home page only, and several of its findings were wrong. Please disregard these:

- **#92 "That toothpaste feeling"** is Gelman's own title. It is not invented.
- **#24 "They are frequentists"**, **#91 "Cheeseburger-snarfing"** and the capitalisation of #106, #107, #110, #116 and #123 all match Gelman's current text.
- **Attributions** I said were missing are on the pages: #44 (Loken, Borges), #51 (Edlin), #59 (Clarke), #74 (Tosh et al.), #94 (Hullman).
- **Theme and kind choices** I called wrong (#43, #84, #134) are defensible once the source posts are read.
- **Author metadata** names both authors, not only the AI model.
- **The About page does** state the list version, say the explanations are not Gelman's, and explain the source-check badges.
- **"Default / # / Entry"** is the table's sort control, not stray text.

## 4. Priority issues

### Major

1. **#44 simulation contradicts its own claim.** The code runs all 12 analyses on each dataset and counts a hit when the smallest p-value is below 0.05. That is fishing. The read-out says "Fishing is not needed, only forks."
2. **#80 simulation has a coding error.** The interaction term is coded so that the simulated difference-in-differences is twice the slider value. At the default "half the main effect" it equals the main effect, so the plotted power curves differ by 4×, not 16×.
3. **Entries that misread Gelman:** #19, #35, #111, #116, #118 (details in section 5.7).
4. **Source-check badges can't be trusted.** ✓ pages with source conflicts: #33, #34, #42, #56, #61, #111, #118. "Not verified" pages whose blog posts are live: 34 of 35 (the other, #136, links to a PDF I didn't test).
5. **Two entries missing** from the live lexicon (section 7).
6. **#140 source link returns 404.** The page also says the post couldn't be accessed. It is live at a different date path.
7. **Analytics and licensing.** Google Analytics loads on every page with no privacy notice or consent prompt. Nothing states a licence for the site's content or permission to reproduce Gelman's definitions.

### Moderate

8. **Missing attribution or context:** #1, #2, #13, #30, #33, #34, #72, #86, #102, #129, #131, #140, #144.
9. **Site-invented material presented as Gelman's:** #6, #11, #100.
10. **Altered quotations:** #17, #61, #143.
11. **Real and illustrative quotations look identical.** 54 of 104 long quoted passages do not appear in the linked post. Most are the site's own hypothetical lines (a few are film or proverb quotes), set in the same quotation marks as Gelman's words.
12. **Simulation defaults that undercut the point or disagree with the text:** #8, #39, #138, #147.
13. **Only 12 of 153 simulation code blocks have been audited,** and 2 of those 12 were wrong. The other 141 need a code review.

### Minor

14. 41 source links use `http://`; 19 link labels are not the post's real title; 42 use the generic label "source post".
15. Accessibility: unnamed icon links, unlabelled filter box, category filters not reachable by keyboard.
16. The index table needs sideways scrolling on a phone.
17. No canonical link, no social image, no meta description on the home page; the sitemap lists `.html` URLs while links use extensionless ones.
18. Mixed British and American spelling (British forms on 22 pages).
19. Small simulation bugs: #29, #32, #57.

## 5. Page by page

### 5.1 Home (`/`)

- **Claim is out of date.** The page says it covers every entry; the live list has 155. Add "as of March 2026", which is currently stated only on About.
- **Numbering is the site's own.** The page says entries are numbered in Gelman's order, which is true, but Gelman's list has no numbers. Say so, because numbers will shift if he inserts an entry.
- **Copy.** The intro's second paragraph ends in a comma splice (", enjoy it"), and "this page" refers to Gelman's page without saying so.
- **Sidebar "Categories".** Themes and kinds are mixed in one alphabetical list. Kind labels are singular there ("Fallacy") and plural in the menu and cards ("Fallacies").
- **Filter box** has a placeholder but no label for screen readers.
- **Category filters** are plain `div` elements with no keyboard focus.
- **Navbar icon links** (GitHub, lexicon) have no text, `aria-label` or title.
- **Heading order.** An `h5` ("Categories") precedes the `h1`.
- **Metadata.** No `meta name="description"`, no canonical link, no `og:image`.
- **Mobile.** At 380 px the four-column table runs past the viewport inside a scroll container, so theme and kind are hidden until you scroll sideways.
- **GitHub link** goes to a profile; I could not find a public repository for this site there.

### 5.2 About (`/about`)

- **Version statement is stale.** It says the site follows the list "archived in March 2026" with 153 entries. Add a "last synced" date and a note that newer entries exist.
- **Titles are not all verbatim.** The page says every title is Gelman's own words; #74 corrects his typo. Either keep the typo with [sic] or note the correction.
- **"Checked against the source" overstates.** See Major issue 4.
- **"No archived copy" is not a reason.** All 145 linked blog posts are live (144 at the linked URL, #140 at a corrected one), and post text is available through the blog's public JSON API.
- **Build instructions without a repository.** The page shows `quarto preview` and `quarto render` but links to no source code.
- **Nothing on licence, permission, privacy or analytics.**
- **No way to report an error.**

### 5.3 Start here (`/start-here`)

- **Five of the twelve stops are flagged "not verified":** #32, #1, #7, #2, #5. I compared four with their posts (#1, #2, #5, #7) and they hold up, with the small fixes listed below. Update the badges.
- **Two stops have wrong simulations:** #44 and #80.
- **The blurb for #118** describes model checking correctly, but the page itself mis-maps the chicken-and-egg analogy.
- "The simplest useful display in statistics" (#2) is the site's judgement, not Gelman's.

### 5.4 Random entry (`/random`)

- Works: it reads `listings.json`, which holds all 153 entries, and redirects.
- The fallback line shows for a moment on every visit, and permanently without JavaScript. Fine, but a `<noscript>` wrapper would be cleaner.
- Failures are swallowed silently (`.catch(() => {})`).

### 5.5 Theme pages (6)

- Counts are correct on all six (18, 31, 14, 18, 39, 33; total 153), and each page's section counts add up.
- Every entry appears exactly once.
- No errors found. The taxonomy is editorial; nothing in it is plainly wrong.

### 5.6 Kind pages (5)

- Counts are correct (11, 50, 19, 59, 14; total 153).
- "Laws and aphorisms" holds 59 entries and works as a catch-all. Consider splitting jokes from substantive laws.
- The "Principles" blurb promises a simulation "showing why it holds". For several entries the simulation is a toy of the site's own, which the pages themselves admit.

### 5.7 Entry pages: patterns across all 153

- **Structure is consistent.** Every page has the same seven sections. All 726 related-entry links work and are reciprocal.
- **All 153 simulations render** with no runtime errors and no NaN or undefined values at default settings.
- **`http://` source links (41 pages):** 31, 32, 35–38, 40, 42–57, 59–70, 72–74, 77, 91, 136. Gelman's post uses `https://` for all.
- **Link labels that are not the post's title (19 pages):** 47, 48, 54, 57, 59, 66, 69, 85, 88, 93, 96, 99, 122, 123, 129, 134, 135, 142, 145. Worst cases: #57 ("More power posing"), #135 ("Statistics in the sweet spot"), #145.
- **"Show simulation code" appears six times per page,** including once for a bare import line. Merge into one block.
- **No seed slider** on 48, 60, 71, 74, 81, 84, 95, 123, 124, 131. These are deterministic calculators, so call them that.
- **Framing Gelman rejects.** #36 and #76 explain their point with "share of hypotheses that are true" arithmetic. Gelman has argued against that true/false framing in favour of sign and magnitude errors. Add a caveat or reframe.
- **`js/stats.js`.** The random-number, distribution and regression helpers are correct. Two notes: `pValue` and `twoGroup` use a normal reference distribution even for small samples, which slightly inflates false-positive rates; `fmt` prints "-0.00" and "NaN" unguarded.

### 5.8 Entry pages one by one

"No issues found" means: title, definition and link match Gelman's; the link resolves; I read the explanation and found nothing inconsistent with the source or Gelman's published position; the simulation runs and its default read-out is sensible. **NV** = the page's own badge says "not verified". **✓** = the page says it was checked.

| # | Entry | Badge | Finding and fix |
|---|---|---|---|
| 1 | Mister P | NV | The Source section calls the link "the original 'Mister P' post". It is "The Next Supreme Court Justice" (9 May 2009), about Kastellec, Lax and Phillips's analysis, which mentions the method in passing. Relabel and credit them. Explanation is accurate; upgrade the badge. |
| 2 | The Secret Weapon | NV | Says it is secret because it is "so simple that people forget to do it". Gelman's reason is that it "seems to be done much less often than it could be". Also add his framing: an approximation to multilevel modelling with the partial pooling done by eye. |
| 3 | The Superplot | NV | "How it works" calls a varying-intercept regression an example of an interaction model. It isn't; an interaction needs varying slopes. The post shows both fits. Reword. |
| 4 | Institutional decision making | ✓ | No issues found. |
| 5 | The Folk Theorem of Statistical Computing | NV | Matches the post. Upgrade the badge. |
| 6 | The Pinch-Hitter Syndrome | NV | Gelman's only example is copy editors, and he ends with a question. The "statistics reviewer" example and the "rhythm" and "incentives" mechanisms are the site's. Label them. |
| 7 | Weakly Informative Priors | NV | Matches the post (a talk abstract for the `bayesglm` paper). Upgrade the badge. Sim label "Flat prior (MLE)" still puts a prior on the intercept. |
| 8 | P-values and U-values | NV | Explanation fine; not compared with the post. Default read-out shows 13% of classical p-values in the outer tenth against a stated 10%. Add replications. |
| 9 | Conservatism | NV | No issues found in the text; not compared with the post. |
| 10 | The Backseat Driver Principle | ✓ | No issues found. Quotes verified. |
| 11 | WWJD | NV | The linked post never expands "WWJD". "What Would Jennifer Do?" and the checklist are the site's inference. Say so, or cite where Gelman spells it out. |
| 12 | Theoretical and Applied Statisticians | NV | Matches the one-line post. Upgrade the badge. |
| 13 | The Fallacy of the One-Sided Bet | NV | Omits Gelman's own examples (refusing a one-in-a-billion risk of death for any sum; torture). The quoted lines are the site's. |
| 14 | Alabama First | ✓ | No issues found. |
| 15 | The USA Today Fallacy | NV | No issues found in the text; not compared with the post. |
| 16 | Second-Order Availability Bias | NV | No issues found in the text; not compared with the post. |
| 17 | The "All Else Equal" Fallacy | NV | Badge says unverified, yet the page quotes the post. One quote is altered: Gelman wrote "its mistaken assumption", the page has "the". Fix and upgrade the badge. |
| 18 | The Self-Cleaning Oven | NV | Matches the post. Upgrade the badge. |
| 19 | The Taxonomy of Confusion | NV | **Wrong.** The taxonomy is Rachel's list for students, quoted by Gelman: six cases (prerequisite statistics, course statistics, unknown function name, unknown function behaviour, code that errors, code that runs but is wrong), each with what to try before asking the TA. The page invents four other categories and credits Gelman. Replace and credit Rachel. |
| 20 | The Blessing of Dimensionality | NV | No issues found in the text; not compared with the post. |
| 21 | Scaffolding | NV | No issues found in the text; not compared with the post. |
| 22 | Ockhamite Tendencies | NV | No issues found in the text; not compared with the post. |
| 23 | Bayesian | ✓ | No issues found. Quotes verified. |
| 24 | Bayesians | ✓ | No issues found. |
| 25 | Multiple Comparisons | ✓ | No issues found. |
| 26 | Taking a Model Too Seriously | NV | No issues found in the text; not compared with the post. |
| 27 | God is in Every Leaf of Every Tree | ✓ | No issues found. Quotes verified. |
| 28 | As They Say in the Stagecoach Business | NV | Matches the post. Upgrade the badge. |
| 29 | Story Time | NV | Text fine; not compared with the post. Read-out is ungrammatical ("especially effective for no college"). |
| 30 | The Foxhole Fallacy | NV | Doesn't say the phrase is the title of Leo Breiman's 1997 article, which the post discusses. The "everyone wants a prior" line is invented. |
| 31 | The Pinocchio Principle | ✓ | Source is a PDF I didn't test. The half-t has scale A only if the inverse-χ² is the scaled version with scale 1. Say so. |
| 32 | The Statistical Significance Filter | NV | Text fine; not compared with the post. Sim: at θ = 0, which the slider allows, every significant result is counted as wrong-signed. |
| 33 | Arrow's Other Theorem (weak) | ✓ | Gelman heard it from a graduate-school friend, "Tex"; not credited. The "working paper, conference paper, …" list is invented. The post is about one result republished in several journals. |
| 34 | Arrow's Other Theorem (strong) | ✓ | Same invented list. The meta-analysis simulation is the site's own; label it. |
| 35 | The Ramanujan Principle | NV | **Misreads the anecdote.** Gelman says Ramanujan supposedly guessed the asymptotic form of the partition function from a table, so he was reading it as a log-scale graph, as everyone does. The page makes him the exception ("Most readers can't") and omits the partition function and the minus signs. |
| 36 | The Paradox of Philosophizing | NV | Text fine; not compared with the post. Uses the true/false-hypothesis framing (see 5.7). |
| 37 | Defaults | ✓ | No issues found. |
| 38 | Default, the greatest trick it ever pulled | ✓ | No issues found. |
| 39 | Defaults, once set | NV | Text fine; not compared with the post. Default sim ends with "Final share: 100%", so the field does switch. Change defaults to show persistence. |
| 40 | The Methodological Attribution Problem | ✓ | No issues found. Source is a PDF I didn't test. |
| 41 | The John Yoo Line | ✓ | No issues found. |
| 42 | The Chris Rock Effect | ✓ | Gelman's example is a map of communication links between U.S. cities. The page uses births by day of year without saying it is the site's example. |
| 43 | The Freshman Fallacy | ✓ | No issues found. |
| 44 | The Garden of Forking Paths | ✓ | **Sim wrong** (Major 1). The formula has "≤" where independent paths give "=", and it describes the take-the-best limit, which is fishing. Simulate one path chosen by a rule that doesn't look at p. |
| 45 | The One-Way Street Fallacy | ✓ | No issues found. |
| 46 | The Pluralist's Dilemma | ✓ | No issues found. Source is a PDF I didn't test. |
| 47 | More Vampirical Than Empirical | ✓ | No issues found. |
| 48 | Statistical Chemotherapy | ✓ | No issues found. |
| 49 | Tell Me What You Don't Know | ✓ | No issues found. |
| 50 | Salad Tongs | ✓ | No issues found. Quotes verified. |
| 51 | The Edlin Factor | ✓ | No issues found. |
| 52 | Kangaroo | ✓ | No issues found. Code audited. |
| 53 | The Speed Racer Principle | ✓ | No issues found. |
| 54 | Uncertainty Interval | ✓ | No issues found. |
| 55 | What would you do if you had all the data? | ✓ | No issues found. The question is in the linked post. |
| 56 | What were you doing before you had any data? | ✓ | The linked post contains only Rubin's first question. The "design and prior" reading is the site's, despite the ✓. Mark it as interpretation or cite a source. |
| 57 | The Time-Reversal Heuristic | ✓ | Text fine. Link label is wrong. Read-out prints "-0.00". |
| 58 | The Status-Reversal Heuristic | ✓ | No issues found. |
| 59 | Clarke's Law | ✓ | No issues found. GRIM example checks out. |
| 60 | The wedding, never about the marriage | ✓ | No issues found. |
| 61 | The problem with peer review | ✓ | Quote altered. Gelman: "the problem with peer review is with the peers". The page drops the second "with" inside quotation marks. |
| 62 | "What does not kill my statistical significance…" | ✓ | No issues found. |
| 63 | Reverse Poe | ✓ | No issues found. |
| 64 | The (Lance) Armstrong Principle | NV | The post is the one-line definition, so there is nothing more to verify. Upgrade the badge. |
| 65 | The Chestertonian Principle | ✓ | No issues found. |
| 66 | The most important aspect of a statistical method | ✓ | No issues found. Arithmetic checks out. |
| 67 | The Pandora Principle | ✓ | No issues found. |
| 68 | The Paradox of Influence | ✓ | No issues found. |
| 69 | Cantor's Corner | ✓ | No issues found. Quotes verified. |
| 70 | Correlation | ✓ | No issues found. |
| 71 | The Javert Paradox | ✓ | No issues found. Source is Slate; not tested. |
| 72 | Eureka bias | ✓ | The term was suggested by a reader who wrote to Gelman. Not credited. |
| 73 | A picture plus 1000 words | ✓ | No issues found. |
| 74 | The Piranha Principle | ✓ | Text fine. Title corrects Gelman's typo without saying so. The "simulation" is a calculator. |
| 75 | The Australia principle | ✓ | No issues found. |
| 76 | Just because something is counterintuitive | NV | The post has a title and no body, so there is nothing to check. Say that. Uses the true/false framing (see 5.7). |
| 77 | Honesty and transparency | ✓ | No issues found. Source is a PDF I didn't test. |
| 78 | Breadcrumbs | ✓ | No issues found. |
| 79 | Random in | ✓ | No issues found. |
| 80 | 16 | ✓ | **Sim wrong** (Major 2). The cell mean uses `gamma*(a-0.5)*(b-0.5)*4/2`; it should be half that. "How it works" also has garbled algebra (a stray "·√2/√2"). |
| 81 | The Horse | ✓ | No issues found. |
| 82 | The 80% Power Lie | ✓ | No issues found. |
| 83 | The Causal Identification Kool-Aid | ✓ | No issues found. |
| 84 | Strongest-link Fallacy | ✓ | No issues found. |
| 85 | Evidence and Truth | ✓ | No issues found. |
| 86 | Assumptions and Rigor | ✓ | The post is a song parody ("Love and Marriage"). The page doesn't say so and adds a line about unchecked assumptions that isn't in it. |
| 87 | Deference Trap | ✓ | No issues found. |
| 88 | Looking for a needle in a pile of needles | ✓ | No issues found. Quotes verified. |
| 89 | Research Incumbency Rule | ✓ | No issues found. |
| 90 | Mathematical Simplicity | ✓ | No issues found. Formula matches the golf model. |
| 91 | Cheeseburger-snarfing diet gurus | ✓ | No issues found. Source is a scanned PDF; not tested. |
| 92 | That toothpaste feeling | ✓ | No issues found. The jargon examples are the site's. |
| 93 | A bunch of hoops to jump through | ✓ | No issues found. |
| 94 | Hullman's Theorem | ✓ | No issues found. |
| 95 | McBroom's Law | ✓ | No issues found. |
| 96 | Mistakes | ✓ | No issues found. |
| 97 | The Bayesian cringe | ✓ | No issues found. |
| 98 | Basketball, or knitting | ✓ | No issues found. |
| 99 | Camel that is the likelihood | ✓ | No issues found. |
| 100 | If zero is in the neighborhood | ✓ | The numeric rule (extend to zero when a < 1.5(b − a)) is the site's invention. Label it. |
| 101 | sqrt(12^2 + 5^2) | ✓ | No issues found. |
| 102 | Freedom | ✓ | The line is Charles Margossian's, said about a Stan feature. Neither he nor Stan is mentioned. Add both, and Gelman's point that regularisation can give more freedom. |
| 103 | Disbelief | ✓ | No issues found. |
| 104 | Your closest collaborator | NV | Matches the post. Upgrade the badge. |
| 105 | Brilliance | ✓ | No issues found. |
| 106 | Web of Trust | ✓ | No issues found. |
| 107 | Schoolyard Evolutionary Biology | ✓ | No issues found. Numbers check out. |
| 108 | What to include | NV | No issues found in the text; not compared with the post. |
| 109 | The worst visual display of all time | ✓ | No issues found. |
| 110 | Tall-Person Syndrome | ✓ | No issues found. |
| 111 | Context | ✓ | **Misreads the post.** Gelman's line is about judging a statement by who says it and where (a sceptic columnist telling a ghost story). The page turns it into "numbers need baselines". Rewrite the text and simulation. |
| 112 | Seeds of its own destruction | ✓ | No issues found. Quotes verified. |
| 113 | Probability | ✓ | No issues found. |
| 114 | A probability isn't just a number | ✓ | No issues found. |
| 115 | When researchers say "guarantee" | ✓ | No issues found. |
| 116 | Panglossian Fallacy | NV | **Misreads the source.** In Gelman's comment on the Leicester odds, the fallacy is assuming the prospective odds must have been right ("the bookies were doing their best"). The page defines it as judging a decision by its outcome and simulates that. Rewrite both. The comment is live, so it can be verified. |
| 117 | Canary variable | ✓ | No issues found. |
| 118 | A chicken | ✓ | **Analogy mis-mapped.** Gelman: "the 'egg' is the model and data", and the chicken is the inferences. The page calls a fitted model "the data's way of making more data". The read-out verdict is hard-coded, not computed. |
| 119 | Anthropic principle | ✓ | No issues found. |
| 120 | Robustness checks | ✓ | No issues found. |
| 121 | Theoretical statistics | ✓ | No issues found. |
| 122 | Between regularization and discovery | ✓ | No issues found. Quotes verified. |
| 123 | Passive Corruption | ✓ | No issues found. |
| 124 | Gresham's Law of bad science | ✓ | No issues found. |
| 125 | The Click-Through Solution | ✓ | No issues found. |
| 126 | Marginal | ✓ | No issues found. |
| 127 | The Analyst's Paradox | ✓ | No issues found. |
| 128 | Meritocracy won't happen | ✓ | No issues found. |
| 129 | Until it runs twice | ✓ | The post is about where the quote comes from: Gelman's own talk at the 2017 New York R Conference. The page omits this. The "lucky seed" reading is the site's. |
| 130 | Torment executioner | ✓ | No issues found. Quotes verified. |
| 131 | End of novel. Beginning of job. | ✓ | The line is critic John Clute's, from a book review. Not credited. |
| 132 | In high-dimensional space | ✓ | No issues found. |
| 133 | Preregistration | ✓ | No issues found. |
| 134 | Uncertainty | ✓ | No issues found. |
| 135 | That narrow beach | ✓ | No issues found. Link label is wrong. |
| 136 | Making errors is inevitable | NV | No issues found in the text. Source is a PDF I didn't test. |
| 137 | Two sides, no vig | ✓ | "You collect whichever way it goes" is wrong. No vig means no fee for taking either side, not a sure win. |
| 138 | The house | NV | Text matches the post. The simulation tests regression under non-normal errors, which is a different "foundation" from the philosophical one in the text. Align them. |
| 139 | Replication and firefighting | ✓ | No issues found. |
| 140 | In a dark room… dollar bills | NV | **Dead link (404).** Correct URL: `/2024/07/11/ancestor-worship-in-academia-where-does-it-happen/`. The line is about economics' adulation of Gary Becker and Lawrence Summers; add that and remove the "couldn't access" note. |
| 141 | Objects of the class | ✓ | No issues found. |
| 142 | Steelmanning | ✓ | No issues found. |
| 143 | Physics is like Brazil | ✓ | Quote silently corrected. Gelman wrote "you on the beach". Use brackets. |
| 144 | The Error-Reversal Heuristic | ✓ | The lexicon links to Dean Eckles's comment, which named the heuristic. Not credited. |
| 145 | Scientific revolutions | ✓ | No issues found. Quotes verified. |
| 146 | The capacity to be upset | ✓ | No issues found. |
| 147 | The year Jesus was born | ✓ | Text gives Gelman's intercept (about 1006 s). The default read-out says 989 s because the data are simulated. Use the real records or say so. |
| 148 | The Edgelord's Dilemma | ✓ | No issues found. |
| 149 | The Groovy Grandma Problem | ✓ | No issues found. |
| 150 | You have no obligation to share… | ✓ | No issues found. |
| 151 | Originality, ambition, and lack of scruple | ✓ | No issues found. |
| 152 | Premature collapsing of the wave function | ✓ | No issues found. |
| 153 | Noem's Razor | ✓ | No issues found. |

## 6. Site-wide issues

**Privacy and legal**

- Google Analytics (`gtag`, IP anonymisation on) loads on every page. There is no privacy notice or consent prompt. Check what Swiss and EU rules require for your audience.
- No licence for the site's text and code, and no statement of permission to reproduce Gelman's definitions.

**Accuracy process**

- Replace "no archived copy" with a live check. The blog's JSON API returns post text for all 145 blog links.
- Add a visible "report an error" link on every page.
- Distinguish Gelman's words from illustrative lines, for example with block quotes for his and italics for the site's.

**Accessibility**

- Navbar icon links need accessible names.
- The filter box needs a label.
- Category filters need keyboard focus and a role.
- Each entry page carries a 160-link sidebar. The skip link is present, which helps.
- Chart descriptions (`ariaLabel`, `ariaDescription`) are set, which is good.

**Mobile**

- No page overflows at 380 px. The home table scrolls sideways; consider a stacked card layout on small screens.

**SEO and metadata**

- No canonical link on any page. Both `/concepts/x` and `/concepts/x.html` return 200, and the sitemap lists the `.html` form.
- No `og:image`; the Twitter card is the small "summary" type.
- Entry pages have no author metadata.

**Third-party scripts**

- MathJax loads from a floating major version (`mathjax@4`). Pin it.
- An ES6 polyfill loads on every page and is probably unnecessary.

**Copy**

- British spellings (colour, favour, behaviour, centre, labelled, neighbouring) on 22 pages; American elsewhere and in every Gelman quote. Pick one.

## 7. Missing entries

Gelman's live list has two entries after Noem's Razor that the site lacks:

| Entry | Gist of his definition | Link |
|---|---|---|
| The paradox of storytelling | We learn from stories that confound expectations, which sits oddly with wanting representative samples. | `/2024/01/18/storytelling-and-scientific-understanding-my-talks-with-thomas-basboll-at-johns-hopkins-on-26-apr/` |
| The transitive property of money | How tech investors have taken on the prestige of information science. | `/2026/08/11/computer-scientists-today-are-like-economists-in-the-early-2000s-and-freudian-psychiatrists-in-the-1950s/` |

No entry on the site is absent from Gelman's list.

## 8. Suggested fix order

1. Fix the #44 and #80 simulations.
2. Rewrite #19, #35, #111, #116 and #118.
3. Fix the #140 link; switch 41 links to `https://`.
4. Re-run the source check against live posts and correct the badges.
5. Add the two missing entries and a "last synced" date.
6. Add attributions (#1, #30, #33, #72, #102, #129, #131, #144) and fix the three altered quotes.
7. Audit the remaining 141 simulation code blocks.
8. Add a privacy notice, a licence and a permission statement.
9. Work through the accessibility, mobile and metadata items.

## 9. Limits of this review

- **Source comparison is partial.** I read source text for 36 entries: 1, 2, 3, 5, 6, 7, 11, 12, 13, 17, 18, 19, 28, 30, 33, 35, 42, 55, 56, 61, 64, 72, 86, 102, 104, 111, 116, 118, 129, 131, 138, 140, 143, 146, 147, 153. For the rest I relied on the automated quote check and my own knowledge of Gelman's writing.
- **"Why it matters" and "Key takeaways" were not read line by line.**
- **Simulation code was audited for 12 pages only.** The other 141 were run and their default read-outs read, which catches crashes and implausible numbers but not logic errors like the one in #80.
- **Seven PDF links and one Slate link were not tested.**
- **Contrast, screen-reader behaviour and real-device rendering were not tested.**
