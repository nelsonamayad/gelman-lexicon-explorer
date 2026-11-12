# P-values and U-values: posterior predictive p-values are not uniform.
stat <- "Sample maximum" # or "Sample mean", "Sample variance" # <1>
n <- 20 # observations per dataset
set.seed(12) # <2>

T_stat <- switch(stat,
  "Sample mean" = mean,
  "Sample maximum" = max,
  "Sample variance" = function(y) mean((y - mean(y))^2)
)
res <- t(replicate(1000, {
  y <- rnorm(n, 0, 1)
  ybar <- mean(y) # data from the true model
  classical <- 1 - pnorm(ybar * sqrt(n)) # a u-value: uniform # <3>
  th <- rnorm(200, ybar, 1 / sqrt(n)) # posterior, flat prior # <4>
  yrep <- matrix(rnorm(200 * n, th, 1), 200) # replicated datasets
  ppp <- mean(apply(yrep, 1, T_stat) >= T_stat(y)) # <5>
  c(classical = classical, ppp = ppp)
}))
extreme <- colMeans(res < 0.05 | res > 0.95)
cat("Share of p-values below 0.05 or above 0.95 (uniform: 10%):\n",
  "classical ", round(100 * extreme[1]), "%, posterior predictive ",
  round(100 * extreme[2]), "%\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <6>
hist(res[, 1],
  breaks = 20, col = "grey70", border = "white",
  main = "Classical p-value", xlab = "p"
)
hist(res[, 2],
  breaks = 20, col = "#2166ac", border = "white",
  main = "Posterior predictive p-value", xlab = "p"
)

# Annotations
# 1. The page's controls: the test statistic and the observations per dataset.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A classical p-value, computed from the sampling distribution of the mean. Under the true model it is uniform: a u-value.
# 4. Draws from the posterior, with a flat prior.
# 5. The posterior predictive p-value: how often a replicated dataset's statistic exceeds the observed one. It need not be uniform.
# 6. The two histograms. The classical one is flat; the posterior predictive one piles up in the middle, because the data were used twice.
