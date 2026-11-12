# The Time-Reversal Heuristic: what if the big replication had come first?
n_orig <- 20 # original study n per group # <1>
n_rep <- 800 # replication n per group
anchor <- 8 # how much the anchored reader over-weights the original
set.seed(57) # <2>

theta <- 0.05
se1 <- sqrt(2 / n_orig)
se2 <- sqrt(2 / n_rep)
repeat { # the famous significant original
  est1 <- rnorm(1, theta, se1)
  if (est1 >= 1.96 * se1) break # <3>
}
est2 <- rnorm(1, theta, se2) # <4>
combine <- function(wa = 1) { # <5>
  (wa * est1 / se1^2 + est2 / se2^2) /
    (wa / se1^2 + 1 / se2^2)
}
est <- c(
  Original = est1, Replication = est2,
  "Combined (either order)" = combine(),
  "Anchored on the original" = combine(anchor)
)
print(round(est, 3)) # the truth is 0.05

par(mar = c(4, 12, 1, 1))
plot(est, 4:1, # <6>
  pch = 19, yaxt = "n", ylab = "", xlab = "Estimate",
  xlim = range(est, est1 + c(-1.96, 1.96) * se1)
)
segments(est[1:2] - 1.96 * c(se1, se2), 4:3, est[1:2] +
  1.96 * c(se1, se2), 4:3)
axis(2, 4:1, names(est), las = 1, cex.axis = 0.8)
abline(v = theta, lty = 2)

# Annotations
# 1. The page's controls: the sample sizes of the original and the replication, and how much an anchored reader over-weights the original.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The famous original: small, and selected to be significant.
# 4. The large replication.
# 5. A precision-weighted combination. It is symmetric in the two studies, so the order of publication doesn't enter; the anchored reader multiplies the original's weight.
# 6. All four estimates with the truth dashed. Imagine the big study had come first.
