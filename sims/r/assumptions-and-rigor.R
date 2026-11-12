# Assumptions and Rigor: difference-in-differences without parallel trends.
delta <- 0.4 # violation of parallel trends # <1>
n <- 100 # units per group
set.seed(86) # <2>

did <- t(replicate(300, {
  c_pre <- rnorm(n, 0)
  c_post <- rnorm(n, 0.5) # control group
  t_pre <- rnorm(n, 0.3)
  t_post <- rnorm(n, 0.3 + 0.5 + delta + 1) # <3>
  est <- (mean(t_post) - mean(t_pre)) - (mean(c_post) - mean(c_pre)) # <4>
  se <- sqrt((var(t_post) + var(t_pre) + var(c_post) + var(c_pre)) / n)
  c(est = est, lo = est - 1.96 * se, hi = est + 1.96 * se)
}))
covered <- did[, "lo"] <= 1 & did[, "hi"] >= 1 # the true effect is 1 # <5>

cat("Coverage of the nominal 95% interval: ",
  round(100 * mean(covered), 1), "%\n",
  sep = ""
)
cat("Average estimate:", round(mean(did[, "est"]), 2), "(true effect: 1)\n")

d <- did[1:50, ]
plot(1:50, d[, "est"], # <6>
  pch = 19, cex = 0.6, ylim = range(d[, -1]),
  xlab = "Replication", ylab = "Estimate with 95% interval"
)
segments(1:50, d[, "lo"], 1:50, d[, "hi"],
  col = ifelse(covered[1:50], "#2166ac", "#d6604d")
)
abline(h = 1, lty = 2)

# Annotations
# 1. The page's controls: how far the treated group's trend departs from the control group's, and the group sizes.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The treated group's post-period outcome: its own trend, plus the violation of parallel trends, plus the true effect of 1.
# 4. The difference-in-differences estimate, which is rigorous only if the parallel-trends assumption holds.
# 5. Whether each replication's 95% interval covers the true effect of 1.
# 6. Fifty replications with their intervals. Red intervals miss the truth, and the share that miss is the cost of the violated assumption.
