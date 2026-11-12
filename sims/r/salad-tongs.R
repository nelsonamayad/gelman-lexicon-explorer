# Salad Tongs: the p-value from a replication of a study with given power.
power <- 0.5 # power of the study # <1>
set.seed(50) # <2>

delta <- qnorm(0.975) + qnorm(power) # true effect, in standard errors # <3>
z <- rnorm(200, delta, 1) # 200 replications
p <- 2 * (1 - pnorm(abs(z))) # <4>
cat("Share significant: ", round(100 * mean(p < 0.05)), "%\n",
  "Middle 80% of p-values: ", signif(quantile(p, 0.1), 2), " to ",
  signif(quantile(p, 0.9), 2), "\n",
  sep = ""
)

plot(1:200, p, # <5>
  log = "y", pch = 19, cex = 0.6,
  col = ifelse(p < 0.05, "#2166ac", "#d6604d"),
  xlab = "Replication", ylab = "p-value (log scale)"
)
abline(h = 0.05, lty = 2)

# Annotations
# 1. The page's control: the power of the study.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The true effect, in standard errors, that gives the study that power.
# 4. The p-value of each of 200 exact replications of the same study.
# 5. The p-values on a log scale. Identical studies, identical truth, and p-values spread over several orders of magnitude: salad tongs.
