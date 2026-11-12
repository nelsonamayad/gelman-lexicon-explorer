# Bayesians are frequentists: coverage averaged over the prior.
se <- 1 # data standard error # <1>
set.seed(24) # <2>

# Prior N(0, 1); the 90% posterior interval for theta given y
covers <- function(theta, y) { # <3>
  w1 <- 1 / se^2
  m <- w1 * y / (1 + w1)
  s <- sqrt(1 / (1 + w1))
  abs(m - theta) < 1.645 * s
}
grid <- seq(-3, 3, by = 0.2)
cov_fixed <- sapply(grid, function(th) mean(covers(th, rnorm(800, th, se)))) # <4>
theta <- rnorm(5000) # theta drawn from the prior
averaged <- mean(covers(theta, rnorm(5000, theta, se))) # <5>

cat("Coverage at theta = 0: ", round(100 * cov_fixed[grid == 0]),
  "%; at theta = 3: ", round(100 * cov_fixed[length(grid)]), "%\n",
  sep = ""
)
cat("Averaged over the prior: ", round(100 * averaged, 1), "%\n", sep = "")

plot(grid, cov_fixed, # <6>
  type = "l", lwd = 2, col = "#2166ac", ylim = c(0, 1),
  xlab = "True value of theta", ylab = "Coverage of the 90% interval"
)
polygon(c(grid, rev(grid)), c(dnorm(grid), rep(0, length(grid))),
  col = adjustcolor("#2166ac", 0.12), border = NA
)
abline(h = 0.9, col = "#d6604d", lty = 2)

# Annotations
# 1. The page's control: the data's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Whether the 90% posterior interval under a N(0, 1) prior covers the true value.
# 4. Frequentist coverage at each fixed true value: too high near the prior's center, too low in its tails.
# 5. Coverage averaged over true values drawn from the prior. This is the frequency property a Bayesian interval does have.
# 6. Coverage as a function of the true value, with the prior density shaded. The dashed line is the nominal 90%.
