# Correlation does not even imply correlation.
n <- 25 # sample size # <1>
selection <- FALSE # only observe units with x + y > 1 (Berkson)
k <- 20 # number of variable pairs examined
set.seed(70) # <2>

draw <- function() { # x and y are independent in the population # <3>
  x <- rnorm(20 * n)
  y <- rnorm(20 * n)
  keep <- if (selection) which(x + y > 1)[1:n] else 1:n # <4>
  data.frame(x = x[keep], y = y[keep])
}
samples <- replicate(k, draw(), simplify = FALSE)
r <- sapply(samples, function(d) cor(d$x, d$y))
best <- which.max(abs(r)) # <5>

cat(
  "True correlation: 0. Most striking of", k, "sample correlations:",
  round(r[best], 2), "\n"
)

plot(samples[[best]], # <6>
  pch = 19, col = "#2166ac",
  main = paste("r =", round(r[best], 2))
)
abline(lm(y ~ x, data = samples[[best]]), col = "#d6604d", lwd = 2)

# Annotations
# 1. The page's controls: the sample size, whether units are selected on x + y, and how many variable pairs are examined.
# 2. Fixes the random numbers so the run is reproducible.
# 3. One sample in which x and y are independent in the population.
# 4. Berkson's selection: keeping only units with a high x + y builds in a negative sample correlation.
# 5. The forking path: of k pairs examined, report the most striking.
# 6. The chosen sample with its fitted line. Its correlation came from noise, selection or search, not from the population.
