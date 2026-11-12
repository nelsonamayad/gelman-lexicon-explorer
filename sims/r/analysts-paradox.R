# The Analyst's Paradox: 29 teams, one dataset, different choices.
choice_impact <- 0.12 # how much each analytic choice moves the estimate # <1>
set.seed(127) # <2>

se <- 0.1
base <- 0.3
shifts <- matrix(rnorm(12, 0, choice_impact), nrow = 4) # 4 choices x 3 # <3>
est <- replicate(29, {
  picks <- cbind(1:4, sample(3, 4, replace = TRUE)) # one option per choice # <4>
  base + sum(shifts[picks]) + rnorm(1, 0, 0.02)
})
est <- sort(est)

cat(
  "Estimates range from", round(min(est), 2), "to", round(max(est), 2),
  "(sd across teams", round(sd(est), 2), ")\n"
)
cat("Each team's own standard error:", se, "\n")
cat(
  "Teams finding a significant positive effect:",
  sum(est - 1.96 * se > 0), "of 29\n" # <5>
)

plot(1:29, est, # <6>
  pch = 19, col = "#2166ac",
  ylim = range(est - 1.96 * se, est + 1.96 * se),
  xlab = "Team (sorted by estimate)",
  ylab = "Estimate with the team's own 95% interval"
)
segments(1:29, est - 1.96 * se, 1:29, est + 1.96 * se, col = "#2166ac")
abline(h = 0)

# Annotations
# 1. The page's control: how much each analytic choice moves the estimate.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Four analytic choices with three options each, and how much each option shifts the estimate.
# 4. Each of the 29 teams picks one option per choice, as the teams in the many-analysts study did.
# 5. How many teams would report a significant positive effect, each using its own standard error.
# 6. The 29 estimates with their own intervals. The spread across teams is much wider than any one team's interval.
