# Theoretical statistics is the theory of applied statistics: analyze the
# procedure people actually use.
beta2 <- 0.2 # true effect of x2 # <1>
rho_x <- 0.7 # correlation between x1 and x2
set.seed(121) # <2>

beta1 <- 0.5
n <- 80
res <- t(replicate(1000, {
  x1 <- rnorm(n)
  x2 <- rho_x * x1 + sqrt(1 - rho_x^2) * rnorm(n)
  y <- beta1 * x1 + beta2 * x2 + rnorm(n)
  full <- summary(lm(y ~ x1 + x2))$coefficients
  in_full <- abs(full["x1", 1] - beta1) < 1.96 * full["x1", 2] # <3>
  drop <- abs(full["x2", 3]) < 1.96 # pretest: drop x2 if n.s. # <4>
  if (drop) {
    red <- summary(lm(y ~ x1))$coefficients # <5>
    in_used <- abs(red["x1", 1] - beta1) < 1.96 * red["x1", 2]
  } else {
    in_used <- in_full
  }
  c(textbook = in_full, practice = in_used, dropped = drop)
}))
cat("x2 dropped in ", round(100 * mean(res[, "dropped"])), "% of datasets\n",
  "Coverage of the reported 95% interval: textbook ",
  round(100 * mean(res[, "textbook"]), 1), "%, as practiced ",
  round(100 * mean(res[, "practice"]), 1), "%\n",
  sep = ""
)

barplot(100 * colMeans(res[, 1:2]), # <6>
  col = c("#2166ac", "#d6604d"),
  names.arg = c("Always fit the full model", "Pretest, drop, report"),
  ylab = "Coverage of the 95% interval (%)", ylim = c(0, 100)
)
abline(h = 95, lty = 2)

# Annotations
# 1. The page's controls: the true effect of the second predictor and its correlation with the first.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The textbook procedure: always fit the full model and report its interval.
# 4. The procedure as practiced: pretest the second predictor and drop it if it isn't significant.
# 5. After dropping it, report the reduced model's interval as if nothing had happened.
# 6. Coverage of the two procedures. The theory that matters is the theory of what analysts actually do.
