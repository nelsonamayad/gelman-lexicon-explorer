# Scaffolding: complete pooling, no pooling, then partial pooling.
tau <- 0.3 # true between-group sd # <1>
set.seed(21) # <2>

n <- c(2, 3, 5, 8, 12, 20, 35, 60, 100, 200) # group sizes
theta <- rnorm(10, 0, tau)
ybar <- sapply(1:10, function(j) mean(rnorm(n[j], theta[j], 1))) # <4>
v <- 1 / n
grand <- sum(ybar * n) / sum(n) # 1. complete pooling # <3>
mu <- sum(ybar / v) / sum(1 / v)
tau2 <- max(0.002, mean((ybar - mu)^2) - mean(v))
partial <- mu + tau2 / (tau2 + v) * (ybar - mu) # 3. partial pooling # <5>
est <- cbind(complete = grand, none = ybar, partial = partial)
rownames(est) <- paste0("G", 1:10, " (n=", n, ")")
print(round(est, 2))

matplot(1:10, est, # <6>
  type = "b", pch = 19, lty = 1, xaxt = "n",
  col = c("grey50", "#d6604d", "#2166ac"), xlab = "Group (size)",
  ylab = "Estimate"
)
axis(1, 1:10, n)
legend("topright", c("Complete pooling", "No pooling", "Partial pooling"),
  col = c("grey50", "#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's control: the true spread between the ten groups.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The first scaffold: complete pooling, one estimate for everyone.
# 4. The second: no pooling, each group's own mean, noisy for the small groups.
# 5. The model you were building toward: partial pooling, which sits between the two scaffolds.
# 6. All three estimates for each group, from the smallest to the largest. The scaffolds show what the final model is doing.
