# Taking a Model Too Seriously: a straight line, extrapolated far away.
curve <- 0.12 # curvature in the truth # <1>
x_far <- 15 # extrapolate to this x
set.seed(26) # <2>

truth <- function(x) 1 + 0.8 * x - curve * x^2
x <- runif(60, 0, 5) # <3>
y <- truth(x) + rnorm(60, 0, 0.6)
fit <- lm(y ~ x)
pred <- predict(fit, data.frame(x = x_far), se.fit = TRUE) # <4>
cat("The line predicts y(", x_far, ") = ", round(pred$fit, 1), " +/- ",
  round(1.96 * pred$se.fit, 1), "; the truth is ",
  round(truth(x_far), 1), "\n",
  sep = ""
)

par(mfrow = c(1, 2))
plot(x, y,
  pch = 19, xlim = c(0, x_far),
  ylim = range(y, truth(x_far), pred$fit), xlab = "x", ylab = "y"
)
abline(fit, col = "#2166ac", lwd = 2)
curve(truth, 0, x_far, add = TRUE, lty = 2, col = "#d6604d", lwd = 2)
plot(x, resid(fit), pch = 19, xlab = "x", ylab = "Residual") # <5>
abline(h = 0, lty = 2)

# Annotations
# 1. The page's controls: how much the truth curves, and how far out to extrapolate.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Data observed only between 0 and 5, where a straight line fits well.
# 4. The line's prediction far outside the data, with the narrow interval the model believes in.
# 5. The residual plot: the check that taking the model seriously demands. Its curvature says not to extrapolate.
