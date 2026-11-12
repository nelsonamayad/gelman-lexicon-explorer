# WWJD (What would Jennifer Hill do?): restrict to the region of overlap.
separation <- 2 # covariate gap between groups # <1>
curvature <- 0.5 # nonlinearity in the outcome
set.seed(6) # <2>

z <- rbinom(600, 1, 0.5)
x <- ifelse(z == 1, rnorm(600, separation, 0.6), rnorm(600, 0, 1.2)) # <3>
y <- curvature * x^2 + 1 * z + rnorm(600) # true treatment effect: 1

naive <- coef(lm(y ~ z + x))[["z"]] # <4>
lo <- max(tapply(x, z, min))
hi <- min(tapply(x, z, max))
cs <- x >= lo & x <= hi # common support # <5>
restricted <- coef(lm(y ~ z + x + I(x^2), subset = cs))[["z"]] # <6>
cat("Naive linear regression, all units: ", round(naive, 2), "\n",
  "Overlap only (", sum(cs), " units), with a quadratic: ",
  round(restricted, 2), "\nTrue effect: 1\n",
  sep = ""
)

plot(x, y, # <7>
  pch = 19, cex = 0.5, col = ifelse(z == 1, "#d6604d", "#2166ac"),
  xlab = "Covariate x", ylab = "Outcome y"
)
rect(lo, -100, hi, 100, col = adjustcolor("grey", 0.2), border = NA)
legend("topleft", c("Treated", "Control"),
  pch = 19,
  col = c("#d6604d", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's controls: how far apart the treated and control groups sit on the covariate, and how curved the outcome is.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Treated units cluster at high values of the covariate; controls spread more widely.
# 4. The naive answer: a linear regression on everyone, which extrapolates into regions where one group has no data.
# 5. The WWJD check: where do both groups have data?
# 6. The answer restricted to that region, with a flexible fit.
# 7. The data with the region of common support shaded.
