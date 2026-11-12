# Weakly Informative Priors: logistic regression with small samples.
n <- 20 # observations per study # <1>
true_beta <- 1.5 # true slope
prior_sd <- 2.5 # prior sd on the slope
set.seed(14) # <2>

# Posterior mode by Newton-Raphson; intercept prior sd 10, slope prior sd s
# (s = 0 means a flat prior, which gives the maximum likelihood estimate)
fit_logit <- function(x, y, s) { # <3>
  prec <- c(1 / 100, if (s > 0) 1 / s^2 else 0)
  beta <- c(0, 0)
  X <- cbind(1, x)
  for (it in 1:60) {
    p <- plogis(X %*% beta)
    grad <- t(X) %*% (y - p) - prec * beta
    H <- -t(X) %*% (X * as.vector(p * (1 - p))) - diag(prec)
    step <- tryCatch(solve(H, grad), error = function(e) NULL)
    if (is.null(step)) {
      beta[2] <- beta[2] + sign(grad[2]) * 5
      next
    }
    beta <- beta - as.vector(step)
    if (abs(beta[2]) > 1e3) break
  }
  max(-50, min(50, beta[2]))
}
est <- t(replicate(200, {
  x <- rnorm(n)
  y <- rbinom(n, 1, plogis(-0.3 + true_beta * x))
  c(flat = fit_logit(x, y, 0), weak = fit_logit(x, y, prior_sd)) # <4>
}))
rmse <- sqrt(colMeans((est - true_beta)^2)) # <5>
cat("Flat prior: ", round(100 * mean(abs(est[, 1]) > 20)), "% of ",
  "estimates blow up past +/-20; RMSE ", round(rmse[1], 2), "\n",
  "Weakly informative N(0, ", prior_sd, "): RMSE ", round(rmse[2], 2),
  "\n",
  sep = ""
)

boxplot(pmin(pmax(est, -10), 10), # <6>
  col = c("grey70", "#2166ac"),
  names = c("Flat prior (MLE)", "Weakly informative"),
  ylab = "Estimated slope (clipped at +/-10)"
)
abline(h = true_beta, lty = 2)

# Annotations
# 1. The page's controls: observations per study, the true slope and the prior standard deviation on the slope.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A logistic regression fitted by Newton-Raphson to the posterior mode. A prior sd of zero means a flat prior, which gives maximum likelihood.
# 4. Each of 200 small studies fitted both ways.
# 5. Root-mean-square error of each estimator against the truth.
# 6. The two sets of estimates, clipped for display. Under a flat prior, separated datasets send the slope toward infinity; the weakly informative prior keeps it finite without pulling it far.
