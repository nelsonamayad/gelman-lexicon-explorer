# Kangaroo: weighing a feather on a bouncing kangaroo.
bounce <- 3 # kangaroo bounce: sd of one reading (kg) # <1>
n <- 30 # readings with the feather, and again without it
feather <- 0.005 # true weight of the feather (kg)
set.seed(52) # <2>

# 1,000 experiments: the difference between the two average readings
est <- replicate(1000, mean(rnorm(n, 40 + feather, bounce)) - # <3>
  mean(rnorm(n, 40, bounce)))
se <- bounce * sqrt(2 / n) # <4>
sig <- abs(est) > 1.96 * se # <5>

cat("Significant experiments:", sum(sig), "of 1000\n")
cat(
  "Their estimates average", round(mean(abs(est[sig])) / feather),
  "times the true weight\n"
)
cat("Significant estimates with negative weight:", sum(est[sig] < 0), "\n")

breaks <- hist(est, breaks = 50, plot = FALSE)$breaks
hist(est, # <6>
  breaks = breaks, col = "grey80", border = "white", main = "",
  xlab = "Estimated feather weight (kg)", ylab = "Experiments"
)
hist(est[sig], breaks = breaks, col = "#d6604d", border = "white", add = TRUE)
abline(v = feather, col = "#2166ac", lwd = 2)

# Annotations
# 1. The page's controls: how much the kangaroo's bouncing makes each reading vary, how many readings are taken, and the feather's true weight.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A thousand experiments. Each weighs the kangaroo n times with the feather and n times without, and takes the difference of the averages.
# 4. The standard error of that difference, which the bouncing dominates.
# 5. Which experiments come out statistically significant.
# 6. The histogram of estimated feather weights, significant ones in red. The blue line is the feather's true weight, invisible at this scale.
