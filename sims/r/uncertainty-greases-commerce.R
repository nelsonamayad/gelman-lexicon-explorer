# Uncertainty: it greases the wheels of commerce. An added error term
# lets a Metropolis sampler move.
tau <- 0 # added error term; try 0.03 # <1>
set.seed(134) # <2>

x <- 2:20
se <- 0.003 * (1 + (0:18) / 3) # very precise data # <3>
y <- 2 - 0.15 * x + 0.004 * x^2 + rnorm(19, 0, se) # slightly curved
lp <- function(a, b) -0.5 * sum((y - a - b * x)^2 / (se^2 + tau^2)) # <4>

run <- function(a, b) { # random-walk Metropolis # <5>
  l <- lp(a, b)
  acc <- 0
  draws <- matrix(NA, 3000, 2)
  for (t in 1:3000) {
    a2 <- a + rnorm(1, 0, 0.02)
    b2 <- b + rnorm(1, 0, 0.002)
    l2 <- lp(a2, b2)
    if (log(runif(1)) < l2 - l) {
      a <- a2
      b <- b2
      l <- l2
      acc <- acc + 1
    }
    draws[t, ] <- c(a, b)
  }
  list(draws = draws, acc = acc / 3000)
}
c1 <- run(1.5, -0.1)
c2 <- run(2.5, -0.05)
b_hat <- mean(c(c1$draws[1501:3000, 2], c2$draws[1501:3000, 2]))
cat("With tau = ", tau, ", the sampler accepts ",
  round(100 * (c1$acc + c2$acc) / 2, 1), "% of proposals; fitted ",
  "slope ", round(b_hat, 4), "\n",
  sep = ""
)

matplot(1:3000, cbind(c1$draws[, 2], c2$draws[, 2]), # <6>
  type = "l", lty = 1,
  col = c("#2166ac", "#d6604d"), xlab = "Iteration",
  ylab = "Slope b"
)

# Annotations
# 1. The page's control: the added error term. With zero, the model claims to be exact.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Very precise data, as in the golf-putting bins with huge counts.
# 4. The log posterior of a straight line fitted to slightly curved data, with the error term added to each bin's variance. That is the grease.
# 5. A random-walk Metropolis sampler.
# 6. Two chains' draws of the slope. With no error term they crawl; with a little uncertainty they mix, and the line balances all the bins.
