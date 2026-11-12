# The Bayesian cringe: using what the field already knows.
tau <- 0.15 # typical effect size in the field # <1>
se <- 0.3 # standard error of a typical study
set.seed(97) # <2>

theta <- rnorm(2000, 0, tau) # true effects # <3>
y <- rnorm(2000, theta, se) # flat prior: take the estimate as is
informed <- tau^2 / (tau^2 + se^2) * y # posterior mean, field's prior # <4>

rmse <- function(est) sqrt(mean((est - theta)^2)) # <5>
cat(
  "Root-mean-square error: flat prior", round(rmse(y), 3),
  "| informed prior", round(rmse(informed), 3), "\n"
)
cat("Reduction in error: ", round(100 * (1 - rmse(informed) / rmse(y))),
  "%\n",
  sep = ""
)

plot(theta[1:500], y[1:500], # <6>
  pch = 16, cex = 0.5,
  col = adjustcolor("#d6604d", 0.4), xlab = "True effect",
  ylab = "Estimate"
)
points(theta[1:500], informed[1:500],
  pch = 16, cex = 0.5,
  col = adjustcolor("#2166ac", 0.6)
)
abline(0, 1, lty = 2)
legend("topleft", c("Flat prior (cringe)", "Uses prior information"),
  col = c("#d6604d", "#2166ac"), pch = 16, bty = "n"
)

# Annotations
# 1. The page's controls: the typical effect size in the field and the standard error of a typical study.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Two thousand true effects drawn from what the field already knows about effect sizes.
# 4. The posterior mean under the field's prior: each estimate shrunk toward zero by the usual precision ratio.
# 5. Root-mean-square error against the truth, for the cringing (flat-prior) estimate and the informed one.
# 6. Estimates against truth. The blue cloud hugs the line more closely than the red one.
