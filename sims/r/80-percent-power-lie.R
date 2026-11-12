# The 80% Power Lie: planning sample sizes from published effect sizes.
d_true <- 0.2 # true effect size d # <1>
n_pilot <- 30 # n per group in the published original study
set.seed(82) # <2>

se0 <- sqrt(2 / n_pilot)
k <- qnorm(0.975) + qnorm(0.8)
# Published originals are the significant ones: draw 2,000 estimates from
# the normal distribution truncated at the significance threshold.
lo <- pnorm((1.96 * se0 - d_true) / se0)
published <- d_true + se0 * qnorm(runif(2000, lo, 1)) # <3>
n_plan <- ceiling(2 * (k / published)^2) # n per group "for 80% power" # <4>
actual <- 1 - pnorm(1.96 - d_true / sqrt(2 / n_plan)) # <5>

cat("Average published effect size:", round(mean(published), 2), "\n")
cat("True effect size:", d_true, "\n")
cat("Median actual power: ", round(100 * median(actual)), "%\n", sep = "")

hist(actual, # <6>
  breaks = seq(0, 1, 0.025), col = "#d6604d", border = "white",
  main = "", xlab = "Actual power of studies planned for 80% power",
  ylab = "Studies"
)
abline(v = 0.8, lty = 2, lwd = 2)

# Annotations
# 1. The page's controls as plain variables: the true effect and the pilot study's sample size. Change them and rerun.
# 2. Fixes the random numbers so the run is reproducible. A different seed gives a different set of published studies.
# 3. Only significant originals get published, so published estimates are draws from a normal distribution truncated at the significance threshold: the significance filter.
# 4. Each follow-up study plans its sample size for 80% power using the published, inflated effect.
# 5. The power those studies actually have against the true effect.
# 6. The histogram of actual power. The dashed line is the 80% that was promised.
