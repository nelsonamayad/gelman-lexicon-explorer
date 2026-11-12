# The Pluralist's Dilemma: which method is best depends on your problems.
my_ratio <- 0.7 # typical signal/noise in my problems # <1>
J <- 8 # groups per problem
set.seed(46) # <2>

ratios <- c(0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5) # <3>
rmse <- t(sapply(ratios, function(ratio) {
  err <- replicate(300, {
    th <- rnorm(J, 0, ratio)
    y <- rnorm(J, th, 1)
    m <- mean(y)
    B <- max(0, mean((y - m)^2) - 1)
    B <- B / (B + 1)
    c(separate = mean((y - th)^2), pooled = mean((m + B * (y - m) - th)^2)) # <4>
  })
  sqrt(rowMeans(err))
}))
near <- which.min(abs(log(ratios / my_ratio))) # <5>
cat("At signal/noise ", ratios[near], ": separate estimates RMSE ",
  round(rmse[near, 1], 2), ", partial pooling ", round(rmse[near, 2], 2),
  "\n",
  sep = ""
)

matplot(ratios, rmse, # <6>
  type = "b", pch = 19, lty = 1, log = "x",
  col = c("#d6604d", "#2166ac"), xlab = "Signal/noise ratio",
  ylab = "Root mean squared error"
)
abline(v = my_ratio, lty = 2)
legend("bottomright", c("Separate estimates", "Partial pooling"),
  col = c("#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: the typical signal-to-noise ratio in your problems, and the number of groups per problem.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A range of problem types, from nearly pure noise to strong signal.
# 4. For each problem, the error of separate estimates and of partial pooling.
# 5. The problem type closest to yours.
# 6. Error against signal-to-noise. Which method is best depends on where your problems fall, and that is a bet you can check.
