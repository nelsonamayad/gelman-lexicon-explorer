# The Causal Identification Kool-Aid: forking paths in a discontinuity design.
n <- 200 # observations # <1>
noise_sd <- 1 # outcome noise (sd)
set.seed(83) # <2>

specs <- data.frame( # <3>
  name = c(
    "Local linear, h = 0.25", "Local linear, h = 0.5", "Global linear",
    "Global quadratic", "Global cubic", "Global quartic"
  ),
  h = c(0.25, 0.5, 1, 1, 1, 1), order = c(1, 1, 1, 2, 3, 4)
)
z_jump <- function(d, h, order) { # z statistic of the jump at x = 0 # <4>
  d <- d[abs(d$x) <= h, ]
  f <- lm(y ~ cut * poly(x, order, raw = TRUE), data = d)
  coef(summary(f))["cut", "t value"]
}
sig <- t(replicate(300, {
  x <- runif(n, -1, 1) # the true discontinuity is zero # <5>
  d <- data.frame(x,
    cut = as.numeric(x >= 0),
    y = 0.5 * x^2 + 0.3 * x + rnorm(n, 0, noise_sd)
  )
  mapply(function(h, o) abs(z_jump(d, h, o)) > 1.96, specs$h, specs$order)
}))

rates <- c(colMeans(sig), "Any of the six" = mean(apply(sig, 1, any))) # <6>
names(rates)[1:6] <- specs$name
print(round(100 * rates)) # false-positive rates (%)

par(mar = c(4, 12, 1, 1))
barplot(rev(rates), # <7>
  horiz = TRUE, las = 1, cex.names = 0.8,
  col = c("#d6604d", rep("#2166ac", 6)), xlim = c(0, 0.5),
  xlab = "False-positive rate (true jump is zero)"
)
abline(v = 0.05, lty = 2)

# Annotations
# 1. The page's controls: the number of observations and the noise in the outcome.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Six reasonable specifications of the same regression-discontinuity analysis: two bandwidths and four polynomial orders.
# 4. The z statistic of the estimated jump at the cutoff under one specification.
# 5. Three hundred datasets in which the true jump is exactly zero. The outcome curves gently, which is all a flexible fit needs to find a jump.
# 6. The false-positive rate of each specification, and of a researcher who reports any one that comes out significant.
# 7. The design is identified and the result is still wrong one time in several: identification does nothing about noise or forking paths.
