# The most important aspect of a statistical method is what data it uses.
rho <- 0.8 # pre-test correlation with the outcome # <1>
n <- 60 # participants per arm
set.seed(66) # <2>

effect <- 0.3
shrink <- function(est, se) (est / se^2) / (1 + 1 / se^2) # N(0, 1) prior # <3>
est <- t(replicate(300, {
  z <- rep(1:0, each = n)
  x <- rnorm(2 * n)
  y <- effect * z + rho * x + sqrt(1 - rho^2) * rnorm(2 * n)
  d <- mean(y[z == 1]) - mean(y[z == 0]) # <4>
  se_d <- sqrt(var(y[z == 1]) / n + var(y[z == 0]) / n)
  adj <- summary(lm(y ~ z + x))$coefficients["z", 1:2] # <5>
  c(
    "Frequentist, outcome only" = d, "Bayesian, outcome only" =
      shrink(d, se_d), "Frequentist + pre-test" = adj[[1]],
    "Bayesian + pre-test" = shrink(adj[[1]], adj[[2]])
  )
}))
rmse <- sqrt(colMeans((est - effect)^2))
print(round(rmse, 3)) # root mean squared error of each method

par(mar = c(4, 12, 1, 1))
barplot(rev(rmse), # <6>
  horiz = TRUE, las = 1, cex.names = 0.8,
  col = c("#2166ac", "#2166ac", "grey70", "grey70"),
  xlab = "Root mean squared error"
)

# Annotations
# 1. The page's controls: how well the pre-test predicts the outcome, and the participants per arm.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The Bayesian ingredient: shrinkage under a standard normal prior.
# 4. The outcome-only estimate.
# 5. The estimate that also uses the pre-test.
# 6. Error of all four methods. Switching philosophy changes little; adding the pre-test data changes a lot. What matters most is what data the method uses.
