# Honesty and transparency are not enough: noisy studies stay uninformative.
meas_noise <- 3 # measurement noise (sd) # <1>
n <- 60 # participants per arm
set.seed(77) # <2>

theta <- 0.2 # small true effect
se <- meas_noise * sqrt(2 / n)
est <- rnorm(200, theta, se) # 200 honest, preregistered studies # <3>
lo <- est - 1.96 * se
hi <- est + 1.96 * se
# Informative: rules out negligible effects (< 0.05), or meaningful ones
informative <- lo > 0.05 | hi < 0.05 # <4>

cat("Each interval is", round(2 * 1.96 * se, 2), "wide; true effect 0.2\n")
cat("Studies that can tell a meaningful effect from a negligible one: ",
  round(100 * mean(informative)), "%\n",
  sep = ""
)

plot(1:50, est[1:50], # <5>
  pch = 19, cex = 0.6, ylim = range(lo[1:50], hi[1:50]),
  xlab = "Study", ylab = "Estimate with 95% interval"
)
segments(1:50, lo[1:50], 1:50, hi[1:50], col = "#2166ac")
abline(h = theta, col = "#d6604d", lwd = 2)
abline(h = 0, lty = 2)

# Annotations
# 1. The page's controls: the measurement noise and the number of participants per arm.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Two hundred honest, preregistered, fully reported studies of a small true effect.
# 4. A study is informative if its interval can tell a meaningful effect from a negligible one.
# 5. Fifty of the studies with their intervals. Honest and transparent, and most of them say nothing.
