# Uncertainty Interval: confidence and credible intervals cover alike, and
# fail alike.
prior_sd <- 5 # prior sd for the Bayesian interval # <1>
clustered <- FALSE # do the data have unmodeled clustering?
set.seed(54) # <2>

truth <- 1
res <- t(replicate(400, {
  y <- if (clustered) { # <3>
    rnorm(100, truth + rep(rnorm(10, 0, 0.8), each = 10))
  } else {
    rnorm(100, truth, 1)
  }
  est <- mean(y)
  se <- sd(y) / sqrt(100)
  prec <- 1 / prior_sd^2 + 1 / se^2 # normal prior centered at 0
  post_mean <- (est / se^2) / prec # <4>
  post_sd <- sqrt(1 / prec)
  c(
    classical = abs(est - truth) < 1.96 * se,
    bayesian = abs(post_mean - truth) < 1.96 * post_sd
  )
}))
cat("Coverage over 400 replications: classical ",
  round(100 * mean(res[, 1]), 1), "%, Bayesian ",
  round(100 * mean(res[, 2]), 1), "%",
  if (clustered) " (both too narrow)" else "", "\n",
  sep = ""
)

barplot(100 * colMeans(res), # <5>
  col = c("grey70", "#2166ac"),
  ylab = "Coverage of the 95% interval (%)", ylim = c(0, 100)
)
abline(h = 95, lty = 2)

# Annotations
# 1. The page's controls: the prior standard deviation for the Bayesian interval, and whether the data have clustering the model ignores.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Data with or without an unmodeled cluster structure.
# 4. The Bayesian posterior under a normal prior centered at zero, next to the classical interval from the sample mean.
# 5. Coverage of both intervals. In most applied problems they cover alike; when the model is wrong, they fail alike. The name uncertainty interval fits both.
