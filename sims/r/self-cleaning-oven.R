# The Self-Cleaning Oven: fake-data simulation catches a bug.
buggy <- TRUE # introduce the standard-error bug # <1>
n_fake <- 300 # fake datasets
set.seed(18) # <2>

truth <- 0.4
n <- 50
res <- t(replicate(n_fake, { # <3>
  tr <- rnorm(n, truth, 1)
  ct <- rnorm(n, 0, 1)
  est <- mean(tr) - mean(ct)
  se <- if (buggy) {
    sqrt(var(tr) / n) # <4>
  } # bug: forgets the control
  else {
    sqrt(var(tr) / n + var(ct) / n)
  }
  c(est = est, lo = est - 1.96 * se, hi = est + 1.96 * se)
}))
covered <- res[, "lo"] <= truth & truth <= res[, "hi"] # <5>
cat("95% intervals cover the true effect ", round(100 * mean(covered)),
  "% of the time", if (buggy) " (the bug shows up)" else "", "\n",
  sep = ""
)

k <- 1:min(100, n_fake)
plot(res[k, "est"], k, # <6>
  pch = 19, cex = 0.5, xlim = range(res[k, -1]),
  col = ifelse(covered[k], "#2166ac", "#d6604d"),
  xlab = "Estimate with 95% interval", ylab = "Fake dataset"
)
segments(res[k, "lo"], k, res[k, "hi"], k,
  col = ifelse(covered[k], "#2166ac", "#d6604d")
)
abline(v = truth, lty = 2)

# Annotations
# 1. The page's controls: whether to plant the standard-error bug, and how many fake datasets to simulate.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Fake-data simulation: generate data from known parameters, run the analysis, and check that it recovers them.
# 4. The planted bug: the standard error forgets the control group's variance.
# 5. Coverage of the nominal 95% intervals. With the bug, it falls well short, and the oven has cleaned itself.
# 6. Intervals from the first 100 fake datasets, misses in red.
