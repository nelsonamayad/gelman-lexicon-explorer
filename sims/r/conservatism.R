# Conservatism: is the familiar method (no pooling) the cautious one?
tau <- 0.3 # true between-group sd # <1>
avg_n <- 10 # average group size
set.seed(19) # <2>

theta <- rnorm(40, 0, tau) # 40 groups' true means
n_j <- pmax(2, rpois(40, avg_n))
ybar <- sapply(1:40, function(j) mean(rnorm(n_j[j], theta[j], 1))) # <3>
v <- 1 / n_j # sampling variance of each mean
mu <- sum(ybar / v) / sum(1 / v)
tau2 <- max(0.001, mean((ybar - mu)^2) - mean(v))
pooled <- mu + tau2 / (tau2 + v) * (ybar - mu) # partial pooling # <4>

rmse <- function(est) sqrt(mean((est - theta)^2))
cat(
  "RMSE: no pooling", round(rmse(ybar), 3), "| partial pooling",
  round(rmse(pooled), 3), "\n"
)
best <- which.max(ybar) # <5>
cat(
  "No pooling's 'best' group: estimate", round(ybar[best], 2),
  "but true mean", round(theta[best], 2), "\n"
)

plot(theta, ybar, # <6>
  pch = 19, cex = 0.8, col = "#d6604d",
  xlim = range(theta, ybar, pooled), ylim = range(ybar, pooled),
  xlab = "True group mean", ylab = "Estimate"
)
points(theta, pooled, pch = 19, cex = 0.8, col = "#2166ac")
abline(0, 1, lty = 2)
legend("topleft", c("No pooling", "Partial pooling"),
  col = c("#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: the true spread between groups and the average group size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The familiar method: each of 40 groups gets its own sample mean, with no pooling.
# 4. The newer method: each mean is shrunk toward the overall mean by an amount that depends on how noisy it is.
# 5. The group the familiar method calls best, and its true mean. Taking a noisy extreme at face value is overclaiming.
# 6. Estimates against true means. The red (unpooled) points scatter further from the diagonal than the blue ones.
