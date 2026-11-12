# Marginal: an integral in statistics, a derivative in economics.
b <- 1.2 # slope (log-odds per unit x) # <1>
x0 <- 0.5 # point for the derivative
set.seed(126) # <2>

a <- -0.5
x <- rnorm(5000, 0.3, 1) # the distribution of x
p <- function(x) plogis(a + b * x)
stat_marginal <- mean(p(x)) # Pr(y = 1), averaging over x # <3>
slope <- b * p(x0) * (1 - p(x0)) # dPr/dx at x0 # <4>
ame <- mean(b * p(x) * (1 - p(x))) # average marginal effect # <5>

cat("Statistics' marginal: Pr(y = 1) =", round(stat_marginal, 3), "\n")
cat("Economics' marginal at x0:", round(slope, 3), "per unit x\n")
cat("Average marginal effect over x:", round(ame, 3), "\n")

curve(p, -4, 4, # <6>
  lwd = 2, col = "#2166ac", xlab = "x", ylab = "Pr(y = 1)",
  ylim = c(0, 1)
)
abline(h = stat_marginal, col = "#2166ac", lty = 2)
segments(x0 - 1, p(x0) - slope, x0 + 1, p(x0) + slope,
  col = "#d6604d",
  lwd = 2
)
rug(x[1:800], col = "grey60")

# Annotations
# 1. The page's controls: the slope of the logistic model and the point at which to take the derivative.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The statistician's marginal: the probability of y = 1 averaged (integrated) over the distribution of x.
# 4. The economist's marginal: the derivative of the probability with respect to x, at one point.
# 5. The average marginal effect, which averages the derivative over x.
# 6. The logistic curve with both marginals: the dashed horizontal line is the integral, the red tangent is the derivative.
