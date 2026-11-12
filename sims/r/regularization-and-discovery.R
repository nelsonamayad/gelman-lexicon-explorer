# Between regularization and discovery: ranking noisy estimates.
spread_n <- 1.2 # variation in sample sizes (log scale) # <1>
set.seed(122) # <2>

# 300 groups: most effects tiny, 8% large; sample sizes vary
theta <- ifelse(runif(300) < 0.08, rnorm(300, 0, 1.5), rnorm(300, 0, 0.2)) # <3>
n <- round(30 * exp(rnorm(300, 0, spread_n))) + 2
se <- 2 / sqrt(n)
y <- rnorm(300, theta, se)
tau2 <- max(0.01, mean(y^2 - se^2))
shrunk <- tau2 / (tau2 + se^2) * y # <4>

top <- function(v) order(-abs(v))[1:20] # the 20 most extreme groups # <5>
cat("Of the true top 20, the raw estimates find ",
  length(intersect(top(y), top(theta))), " and the regularized ",
  "estimates find ", length(intersect(top(shrunk), top(theta))), "\n",
  sep = ""
)

plot(theta, y, # <6>
  pch = 19, cex = 0.6, col = "grey60",
  xlab = "True effect", ylab = "Estimate"
)
points(theta[top(y)], y[top(y)], col = "#d6604d", cex = 1.4)
points(theta[top(shrunk)], shrunk[top(shrunk)], pch = 19, col = "#2166ac")
legend("topleft", c("Raw top 20", "Regularized top 20"),
  pch = c(1, 19),
  col = c("#d6604d", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's control: how much sample sizes vary across the 300 groups.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Most true effects are tiny; a few are large. Those few are the discoveries worth making.
# 4. Regularized estimates: each shrunk toward zero in proportion to its noise.
# 5. The 20 most extreme groups under each estimator, compared with the true top 20.
# 6. Raw estimates against the truth, with each estimator's top 20 marked. Regularization finds more of the real discoveries, because the raw top 20 is full of noisy small groups.
