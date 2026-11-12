# Robustness checks: 30 specifications, only a few of them reported.
true_eff <- 0 # true effect # <1>
corr <- 0.7 # correlation among specifications
set.seed(118) # <2>

se <- 0.15
# Only datasets where some specification is significant become a paper
tries <- 0
repeat {
  tries <- tries + 1
  common <- rnorm(1, 0, se)
  est <- true_eff + sqrt(corr) * common + sqrt(1 - corr) * rnorm(30, 0, se) # <3>
  if (any(abs(est) > 1.96 * se) || tries >= 500) break # <4>
}
main <- est[which.max(abs(est))] # the headline specification # <5>
reported <- order(abs(est - main))[1:6] # and five "robustness checks" # <6>
cat("Datasets tried before a significant one: ", tries, "\n",
  "Significant: ", sum(abs(est[reported]) > 1.96 * se), " of 6 reported",
  " specifications, ", sum(abs(est) > 1.96 * se), " of all 30\n",
  sep = ""
)

o <- order(est)
plot(est[o], 1:30, # <7>
  pch = 19, xlim = range(est) + c(-0.3, 0.3),
  col = ifelse(o %in% reported, "#d6604d", "grey50"),
  xlab = "Estimate with 95% interval", ylab = "Specification"
)
segments(est[o] - 1.96 * se, 1:30, est[o] + 1.96 * se, 1:30,
  col = ifelse(o %in% reported, "#d6604d", "grey70")
)
abline(v = c(0, true_eff), lty = c(1, 2))

# Annotations
# 1. The page's controls: the true effect and how correlated the 30 specifications are.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Thirty reasonable specifications of the same analysis, with correlated estimates.
# 4. Only a dataset in which some specification is significant becomes a paper.
# 5. The headline specification: the most significant one.
# 6. The robustness checks: the five specifications that agree most closely with the headline.
# 7. All 30 specifications, the reported six in red. The table was chosen, not discovered.
