# Breadcrumbs: undocumented decisions make results irreproducible.
documented <- 3 # decision points documented (of 10) # <1>
set.seed(78) # <2>

shifts <- matrix(rnorm(40, 0, 0.08), nrow = 10) # 10 decisions x 4 options # <3>
chosen <- sample(4, 10, replace = TRUE) # what the authors did
published <- 0.25 + sum(shifts[cbind(1:10, chosen)]) # <4>
reanalyses <- replicate(300, {
  pick <- chosen
  undocumented <- seq_len(10) > documented
  pick[undocumented] <- sample(4, sum(undocumented), replace = TRUE) # <5>
  0.25 + sum(shifts[cbind(1:10, pick)])
})

cat("Published estimate:", round(published, 3), "\n")
cat(
  "Spread (sd) of re-analyses with", documented, "of 10 steps documented:",
  round(sd(reanalyses), 3), "\n"
)

hist(reanalyses, # <6>
  breaks = 30, col = "#2166ac", border = "white", main = "",
  xlab = "Re-analysis estimate", ylab = "Re-analyses"
)
abline(v = published, col = "#d6604d", lwd = 3)

# Annotations
# 1. The page's control: how many of the ten analytic decisions the authors wrote down.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Ten decision points with four options each, and how much each option shifts the estimate.
# 4. The published estimate comes from the options the authors actually chose.
# 5. A re-analyst follows the documented decisions and guesses the rest.
# 6. The spread of re-analyses around the published estimate (red). More breadcrumbs, less spread.
