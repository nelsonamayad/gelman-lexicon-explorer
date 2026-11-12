# Bayesian: a confident prior in the wrong place.
prior_off <- 1.5 # prior center minus truth # <1>
prior_sd <- 0.4 # prior sd (confidence)
se <- 0.5 # data standard error
set.seed(23) # <2>

truth <- 0
est <- rnorm(500, truth, se)
w0 <- 1 / prior_sd^2
w1 <- 1 / se^2
post_mean <- (w0 * (truth + prior_off) + w1 * est) / (w0 + w1) # <3>
post_sd <- sqrt(1 / (w0 + w1)) # <4>

cat("Coverage of nominal 90% intervals: data only ",
  round(100 * mean(abs(est - truth) < 1.645 * se)), "%, Bayesian ",
  round(100 * mean(abs(post_mean - truth) < 1.645 * post_sd)), "%\n", # <5>
  sep = ""
)

breaks <- seq(min(est, post_mean) - 0.1, max(est, post_mean) + 0.1,
  length.out = 41
)
hist(est, # <6>
  breaks = breaks, col = adjustcolor("#2166ac", 0.5),
  border = "white", main = "", xlab = "Estimate", ylab = "Replications"
)
hist(post_mean,
  breaks = breaks, col = adjustcolor("#d6604d", 0.6),
  border = "white", add = TRUE
)
abline(v = truth, lwd = 2)
abline(v = prior_off, col = "#d6604d", lty = 2)
legend("topright", c("Data only", "Bayesian posterior mean"),
  fill = adjustcolor(c("#2166ac", "#d6604d"), 0.6), bty = "n"
)

# Annotations
# 1. The page's controls: how far the prior's center sits from the truth, how confident the prior is, and the data's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The posterior mean, a precision-weighted average of the prior center and the estimate. A confident prior in the wrong place pulls it off the truth.
# 4. The posterior standard deviation is smaller than the data's, so the interval is narrower, whether or not it is in the right place.
# 5. Coverage of the Bayesian 90% interval, compared with the data-only interval printed just before.
# 6. Histograms of the data-only estimates and the posterior means, with the truth as a solid line and the prior center dashed.
