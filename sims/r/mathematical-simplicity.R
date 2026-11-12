# Mathematical Simplicity: the golf-putting geometry model vs a logistic fit.
sigma_deg <- 1.5 # true angular error (degrees) # <1>
n_per <- 200 # putts per distance
set.seed(90) # <2>

r_hole <- 4.25 / 2 / 12
r_ball <- 1.68 / 2 / 12 # radii, in feet
p_geo <- function(x, sigma) 2 * pnorm(asin((r_hole - r_ball) / x) / sigma) - 1 # <3>
sigma_true <- sigma_deg * pi / 180
x <- 2:20
n <- rep(n_per, length(x))
y <- rbinom(length(x), n, p_geo(x, sigma_true))

# Geometric model: one parameter, fitted by maximum likelihood
nll <- function(s) -sum(dbinom(y, n, p_geo(x, s), log = TRUE))
sigma_hat <- optimize(nll, c(0.005, 0.1))$minimum # <4>
# Logistic regression: two parameters
fit <- glm(cbind(y, n - y) ~ x, family = binomial) # <5>

cat("Geometric model: sigma = ", round(sigma_hat * 180 / pi, 2),
  " degrees (truth: ", sigma_deg, ")\n",
  sep = ""
)
at40 <- c( # <6>
  truth = p_geo(40, sigma_true), geometry = p_geo(40, sigma_hat),
  logistic = unname(predict(fit, data.frame(x = 40),
    type = "response"
  ))
)
print(round(at40, 3)) # success probability at 40 feet

grid <- seq(2, 40, by = 0.5)
plot(x, y / n, # <7>
  pch = 19, xlim = c(2, 40), ylim = c(0, 1),
  xlab = "Distance (feet)", ylab = "Probability of success"
)
rect(20, -1, 42, 2, col = adjustcolor("grey", 0.2), border = NA)
lines(grid, p_geo(grid, sigma_true), lty = 2, col = "grey40")
lines(grid, p_geo(grid, sigma_hat), col = "#2166ac", lwd = 2)
lines(grid, predict(fit, data.frame(x = grid), type = "response"),
  col = "#d6604d", lwd = 2
)
legend("topright", c(
  "Geometry (1 parameter)", "Logistic (2 parameters)",
  "Truth"
),
col = c("#2166ac", "#d6604d", "grey40"),
lty = c(1, 1, 2), lwd = c(2, 2, 1), bty = "n"
)

# Annotations
# 1. The page's controls: the golfer's true angular error and the number of putts per distance.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The geometry model: a putt goes in if its angle is within the window set by the hole's and the ball's radii. One parameter, derived from first principles.
# 4. That parameter fitted by maximum likelihood.
# 5. The competitor: a logistic regression with two parameters and no geometry.
# 6. Both models' predictions at 40 feet, outside the data. The geometric model extrapolates sensibly; the logistic one does not.
# 7. The data, both fits and the truth, with the extrapolation region shaded.
