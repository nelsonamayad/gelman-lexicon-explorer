# The Folk Theorem: computational trouble often means a model problem.
log_tau <- 3.5 # log10 of the prior sd; large means nearly unidentified # <1>
iters <- 3000 # iterations per chain
set.seed(21) # <2>

y <- rnorm(50, 1.5, 1)
ybar <- mean(y)
n <- 50
tau <- 10^log_tau
# y depends on a + b only, so a and b are identified only by the prior
log_post <- function(a, b) { # <3>
  -0.5 * n * (ybar - a - b)^2 -
    0.5 * (a^2 + b^2) / tau^2
}
run <- function(a, b) { # random-walk Metropolis # <4>
  out <- numeric(iters)
  lp <- log_post(a, b)
  for (t in 1:iters) {
    a2 <- a + rnorm(1, 0, 0.3)
    b2 <- b + rnorm(1, 0, 0.3)
    lp2 <- log_post(a2, b2)
    if (log(runif(1)) < lp2 - lp) {
      a <- a2
      b <- b2
      lp <- lp2
    }
    out[t] <- a
  }
  out
}
c1 <- run(-5, 5)
c2 <- run(5, -5)
h <- (iters / 2 + 1):iters # second halves
m <- length(h)
W <- (var(c1[h]) + var(c2[h])) / 2
B <- m * (mean(c1[h]) - mean(c2[h]))^2 / 2
rhat <- sqrt(((m - 1) / m * W + B / m) / W) # <5>

cat("R-hat for a:", round(rhat, 2), "(well above 1.01: chains disagree)\n")
cat("Try log_tau <- 0: a weakly informative prior fixes the computation.\n")

matplot(1:iters, cbind(c1, c2), # <6>
  type = "l", lty = 1,
  col = c("#2166ac", "#d6604d"), xlab = "Iteration",
  ylab = "Parameter a"
)

# Annotations
# 1. The page's controls: the prior standard deviation (as a power of ten) and the number of iterations per chain.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The log posterior. The data see only a + b, so with a nearly flat prior the posterior is a long ridge.
# 4. A random-walk Metropolis sampler, started from a given point.
# 5. R-hat from the second halves of the two chains. Values well above 1.01 mean the chains disagree.
# 6. The two chains' draws of a. When the computation struggles, the problem is the model: a and b are not identified.
