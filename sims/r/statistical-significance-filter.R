# The Statistical Significance Filter: significant estimates are too big.
theta <- 0.2 # true effect # <1>
se <- 0.25 # standard error
set.seed(42) # <2>

est <- rnorm(400, theta, se) # 400 replications of the study # <3>
sig <- abs(est) > 1.96 * se # <4>
power <- 1 - pnorm(1.96 - theta / se) + pnorm(-1.96 - theta / se) # <5>
cat("Power: ", round(100 * power), "%; ", sum(sig), " of 400 significant\n",
  "Average significant estimate: ", round(mean(abs(est[sig])), 2),
  " (", round(mean(abs(est[sig])) / theta, 1), " times the truth); ",
  sum(sig & sign(est) != sign(theta)), " with the wrong sign\n",
  sep = ""
)

plot(1:400, est, # <6>
  pch = 19, cex = 0.6,
  col = ifelse(sig, "#d6604d", "grey70"), xlab = "Replication",
  ylab = "Estimate"
)
abline(h = theta, lwd = 2, col = "#2166ac")
abline(h = c(-1.96, 1.96) * se, lty = 2)

# Annotations
# 1. The page's controls: the true effect and the study's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Four hundred replications of the same study.
# 4. The filter: which replications are statistically significant. Only the large estimates pass.
# 5. The study's power, from the normal distribution.
# 6. Every replication's estimate, significant ones in red, against the truth in blue. The red dots are far from the blue line: the significant estimates are the overestimates.
