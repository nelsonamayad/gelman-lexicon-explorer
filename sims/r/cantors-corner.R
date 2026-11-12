# Cantor's Corner: find the statistic your model can't reproduce.
zero_infl <- 0.25 # share of structural zeros in the truth # <1>
set.seed(69) # <2>

y <- ifelse(runif(300) < zero_infl, 0, rpois(300, rgamma(300, 4, 1))) # <3>
lambda <- mean(y) # fit a Poisson model # <4>
stats <- list(
  Mean = mean, Variance = var,
  "Share of zeros" = function(v) mean(v == 0), Maximum = max
)
reps <- replicate(400, rpois(300, lambda)) # 400 datasets from the fit # <5>
res <- t(sapply(stats, function(f) { # <6>
  sim <- apply(reps, 2, f)
  c(observed = f(y), simulated_mean = mean(sim), p = mean(sim >= f(y)))
}))
print(round(res, 3)) # p near 0 or 1: the model misses this feature

par(mfrow = c(2, 2)) # <7>
for (name in names(stats)) {
  sim <- apply(reps, 2, stats[[name]])
  hist(sim,
    col = "grey80", border = "white", main = name,
    xlim = range(sim, stats[[name]](y)), xlab = "Simulated from the model"
  )
  abline(v = stats[[name]](y), col = "#d6604d", lwd = 3)
}

# Annotations
# 1. The page's control: the share of structural zeros in the real data.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The truth is overdispersed and zero-inflated. The model will be a plain Poisson.
# 4. The Poisson fit: one parameter, the mean.
# 5. Four hundred datasets simulated from the fitted model.
# 6. For each test statistic, where the observed value falls among the simulated ones. A p-value near 0 or 1 marks a feature the model can't reproduce: Cantor's corner.
# 7. One histogram per statistic, with the observed value in red. The mean is always matched; the variance and the zeros are not.
