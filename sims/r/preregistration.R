# Preregistration: a plan that adjusts for a baseline covariate.
rho <- 0.7 # correlation of the baseline covariate with the outcome # <1>
n <- 60 # participants per arm
set.seed(133) # <2>

effect <- 0.3
res <- t(replicate(500, {
  z <- rep(1:0, each = n)
  x <- rnorm(2 * n)
  y <- effect * z + rho * x + sqrt(1 - rho^2) * rnorm(2 * n)
  floor <- t.test(y[z == 1], y[z == 0]) # difference in means # <3>
  adj <- summary(lm(y ~ z + x))$coefficients["z", 1:2] # <4>
  c(
    floor_est = unname(diff(rev(floor$estimate))),
    floor_se = floor$stderr, adj_est = adj[[1]], adj_se = adj[[2]]
  )
}))
cover <- function(e, s) mean(abs(res[, e] - effect) < 1.96 * res[, s]) # <5>
cat("Difference in means: average se ", round(mean(res[, "floor_se"]), 3),
  ", coverage ", round(100 * cover("floor_est", "floor_se")), "%\n",
  "Adjusted for baseline: average se ", round(mean(res[, "adj_se"]), 3),
  ", coverage ", round(100 * cover("adj_est", "adj_se")), "%\n",
  sep = ""
)

boxplot(res[, c("floor_est", "adj_est")], # <6>
  col = c("grey70", "#2166ac"),
  names = c("Difference in means", "Adjusted for baseline"),
  ylab = "Estimated effect"
)
abline(h = effect, lty = 2)

# Annotations
# 1. The page's controls: how strongly the baseline covariate predicts the outcome, and the participants per arm.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The preregistered floor: a plain difference in means.
# 4. The preregistered plan's better analysis: adjust for the baseline covariate, which was named in advance.
# 5. Coverage of each method's intervals, to show the adjustment is honest.
# 6. Both estimates across 500 trials. Preregistration is a floor, not a ceiling: the planned adjustment is more precise and just as valid.
