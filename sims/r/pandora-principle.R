# The Pandora Principle: once you think of a confounder, you can't unthink it.
confound <- 0.6 # strength of confounding by U # <1>
p_matters <- 0.5 # your belief that U matters
set.seed(67) # <2>

u <- rnorm(500)
z <- rbinom(500, 1, plogis(confound * 1.5 * u)) # treatment depends on U # <3>
y <- 0.3 * z + confound * u + rnorm(500) # true effect 0.3

A <- summary(lm(y ~ z))$coefficients["z", 1:2] # ignores U # <4>
B <- summary(lm(y ~ z + u))$coefficients["z", 1:2] # adjusts for U # <5>
# Honest answer: a mixture of the two models, weighted by belief
mix <- (1 - p_matters) * A[1] + p_matters * B[1] # <6>
sd_mix <- sqrt((1 - p_matters) * (A[2]^2 + A[1]^2) +
  p_matters * (B[2]^2 + B[1]^2) - mix^2)
est <- rbind(
  "Ostrich (never thought of U)" = A[1] + c(0, -1.96, 1.96) * A[2],
  "Adjusted for U" = B[1] + c(0, -1.96, 1.96) * B[2],
  "Honest (unsure whether U matters)" =
    mix + c(0, -1.96, 1.96) * sd_mix
)
colnames(est) <- c("estimate", "lower", "upper")
print(round(est, 2)) # true effect: 0.3

par(mar = c(4, 14, 1, 1))
plot(est[, 1], 3:1, # <7>
  xlim = range(est), pch = 19, yaxt = "n", ylab = "",
  xlab = "Estimated effect of z (95% interval)"
)
segments(est[, 2], 3:1, est[, 3], 3:1, lwd = 2)
axis(2, 3:1, rownames(est), las = 1, cex.axis = 0.8)
abline(v = 0.3, lty = 2)

# Annotations
# 1. The page's controls: how strongly the unobserved variable U confounds, and how much you believe it matters.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Treatment depends on U, and so does the outcome: U is a confounder.
# 4. The ostrich estimate, which never thought of U.
# 5. The estimate that adjusts for U. In real life U would be unmeasured, so this is the box that cannot be reopened.
# 6. The honest answer once you have thought of U: a mixture of the two, weighted by how much you believe U matters, with the extra uncertainty that implies.
# 7. The three estimates with their intervals. Having thought of U, you can't go back to the ostrich's narrow interval.
