# Multiple Comparisons: classical tests vs a multilevel model.
tau <- 0.1 # spread of true effects # <1>
sigma <- 0.5 # standard error of each estimate
set.seed(20) # <2>

theta <- rnorm(50, 0, tau) # 50 true effects, mostly tiny
y <- rnorm(50, theta, sigma) # their noisy estimates # <3>

# Multilevel model (empirical Bayes): shrink toward the mean
mu <- mean(y)
tau2 <- max(0, mean((y - mu)^2) - sigma^2) # <4>
B <- tau2 / (tau2 + sigma^2)
pm <- mu + B * (y - mu) # posterior means # <5>
psd <- sqrt(B) * sigma + 1e-9 # posterior sds

claim_classic <- abs(y) > 1.96 * sigma # <6>
claim_ml <- B > 0 & abs(pm) > 1.96 * psd # <7>
cat("Classical: ", sum(claim_classic), " 'significant' effects, ",
  sum(claim_classic & sign(y) != sign(theta)), " with the wrong sign\n",
  "Multilevel: ", sum(claim_ml), " confident claims, ",
  sum(claim_ml & sign(pm) != sign(theta)), " with the wrong sign\n",
  sep = ""
)

plot(theta, y, # <8>
  pch = ifelse(claim_classic, 19, 1), col = "#d6604d",
  xlab = "True effect", ylab = "Estimate"
)
points(theta, pm, pch = 19, col = "#2166ac")
abline(h = c(-1.96, 1.96) * sigma, lty = 2)
legend("topleft", c(
  "Raw estimate (filled if significant)",
  "Multilevel estimate"
),
pch = 19, col = c("#d6604d", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's controls: the spread of the 50 true effects and the standard error of each estimate.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Fifty noisy estimates of fifty mostly tiny effects.
# 4. The multilevel model's estimate of the true spread, from the estimates and their known noise.
# 5. Partial pooling: each estimate shrunk toward the mean by the ratio of true spread to total spread.
# 6. The classical rule: claim an effect when the raw estimate is significant.
# 7. The multilevel rule: claim an effect when the posterior interval excludes zero.
# 8. Raw and pooled estimates against the truth, with the significance thresholds dashed. The pooled estimates make fewer and better claims.
