# Until it runs twice: two runs of a sampler expose a stuck chain.
gap <- 5 # distance between the two modes # <1>
step <- 0.5 # proposal step size
set.seed(1) # <2>

# A posterior with two well-separated modes; its true mean is 0
logp <- function(x) { # <3>
  log(0.5 * dnorm(x, -gap / 2, 0.7) +
    0.5 * dnorm(x, gap / 2, 0.7) + 1e-300)
}
run <- function(x) { # random-walk Metropolis
  out <- numeric(2000)
  lp <- logp(x)
  for (t in 1:2000) {
    y <- x + rnorm(1, 0, step)
    ly <- logp(y)
    if (log(runif(1)) < ly - lp) {
      x <- y
      lp <- ly
    }
    out[t] <- x
  }
  out
}
r1 <- run(runif(1, -gap, gap)) # <4>
r2 <- run(runif(1, -gap, gap))
m <- c(mean(r1[1001:2000]), mean(r2[1001:2000])) # <5>
cat("Second-half means: run 1 ", round(m[1], 2), ", run 2 ", round(m[2], 2),
  " (true mean 0)\n", if (abs(diff(m)) > 1) {
    "The runs disagree."
  } else {
    "The runs agree."
  }, "\n",
  sep = ""
)

matplot(1:2000, cbind(r1, r2), # <6>
  type = "l", lty = 1,
  col = c("#2166ac", "#d6604d"), xlab = "Iteration", ylab = "x"
)

# Annotations
# 1. The page's controls: the distance between the posterior's two modes and the sampler's step size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A posterior with two well-separated modes.
# 4. Each run of the sampler starts from a random point and may stay in one mode for the whole run.
# 5. The second-half means of the two runs. Running it twice is what reveals that each run was confident and wrong.
# 6. The two chains. If they disagree, neither one can be trusted alone.
