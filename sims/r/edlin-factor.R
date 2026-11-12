# The Edlin Factor: how much to scale down published estimates.
tau <- 0.2 # spread of true effects # <1>
se <- 0.25 # standard error of each study
set.seed(51) # <2>

theta <- rnorm(5000, 0, tau)
est <- rnorm(5000, theta, se)
pub <- abs(est) > 1.96 * se # only significant results get published # <3>
factor <- sum(theta[pub] * est[pub]) / sum(est[pub]^2) # slope through 0 # <4>

cat("Published:", sum(pub), "of 5000\n")
cat(
  "Average magnitude: published estimates", round(mean(abs(est[pub])), 2),
  "| their true effects", round(mean(abs(theta[pub])), 2), "\n"
)
cat("Edlin factor: ", round(factor, 2), " (theory: ",
  round(tau^2 / (tau^2 + se^2), 2), ")\n",
  sep = ""
)

plot(est[pub], theta[pub], # <5>
  pch = 16, cex = 0.5,
  col = adjustcolor("#2166ac", 0.4), xlab = "Published estimate",
  ylab = "True effect"
)
abline(0, 1, lty = 2)
abline(0, factor, col = "#d6604d", lwd = 2)

# Annotations
# 1. The page's controls: the spread of true effects across the literature and each study's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Only significant results get published.
# 4. The Edlin factor: the slope through the origin of true effect on published estimate. Multiply a published estimate by it to get the best guess of the truth.
# 5. True effects against published estimates. The red line is the Edlin factor; the dashed line is taking estimates at face value.
