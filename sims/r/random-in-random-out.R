# Random in, random out: regressions on pure noise still find "effects".
n <- 80 # observations per dataset # <1>
real_effect <- 0 # true effect of predictor 1 (the others are zero)
set.seed(79) # <2>

# 25 datasets, each a regression of y on 10 predictors
sig <- t(replicate(25, {
  X <- matrix(rnorm(n * 10), n) # <3>
  y <- real_effect * X[, 1] + rnorm(n)
  tab <- summary(lm(y ~ X))$coefficients[-1, ]
  abs(tab[, 1] / tab[, 2]) > 1.96 # <4>
}))
cat(sum(rowSums(sig) > 0), " of 25 datasets have at least one ",
  "'significant' predictor\nPredictor 1 is significant in ",
  sum(sig[, 1]), " of 25\n",
  sep = ""
)

image(1:10, 1:25, t(sig), # <5>
  col = c("grey90", "#d6604d"),
  xlab = "Predictor", ylab = "Dataset"
)

# Annotations
# 1. The page's controls: observations per dataset and the true effect of the first predictor (the rest are zero).
# 2. Fixes the random numbers so the run is reproducible.
# 3. Ten predictors that are pure noise.
# 4. Which predictors come out significant in each dataset.
# 5. A grid of 25 datasets by 10 predictors. Something is significant in most datasets, and it is a different something each time.
