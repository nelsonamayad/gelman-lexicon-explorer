# Ockhamite Tendencies: zeroing out small effects vs partial pooling.
tau <- 0.4 # spread of true effects # <1>
se <- 0.4 # standard error of each estimate
set.seed(22) # <2>

truth <- rnorm(40, 0, tau)
est <- rnorm(40, truth, se)
tau2_hat <- max(0.0001, mean(est^2) - se^2)
selected <- ifelse(abs(est / se) > 2, est, 0) # keep only "significant" # <3>
pooled <- tau2_hat / (tau2_hat + se^2) * est # shrink everything a bit # <4>

rmse <- function(x) sqrt(mean((x - truth)^2))
cat("Error (RMSE): raw ", round(rmse(est), 2), ", select-or-zero ",
  round(rmse(selected), 2), " (", sum(selected != 0), " of 40 kept), ",
  "partial pooling ", round(rmse(pooled), 2), "\n",
  sep = ""
)

plot(truth, selected, # <5>
  pch = 19, col = "#d6604d", xlab = "True effect",
  ylab = "Estimate", ylim = range(est)
)
points(truth, pooled, pch = 19, col = "#2166ac")
abline(0, 1, lty = 2)
legend("topleft", c("Select or zero", "Partial pooling"),
  pch = 19,
  col = c("#d6604d", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's controls: the spread of the 40 true effects and each estimate's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The Ockhamite move: keep the significant effects at face value and set the rest to exactly zero.
# 4. The alternative: keep every effect, shrunk a little toward zero.
# 5. Both against the truth. Zeroing out small effects is a model with many parameters set to exactly zero, and it loses to shrinking them.
