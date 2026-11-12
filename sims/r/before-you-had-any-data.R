# What were you doing before you had any data? A prior predictive check.
s <- 10 # prior sd on each logistic regression coefficient # <1>
K <- 5 # number of standardized predictors
set.seed(56) # <2>

# Linear predictor under the prior: intercept + sum of beta_k * x_k
eta <- rnorm(4000) + rowSums(matrix(rnorm(4000 * K, 0, s) * rnorm(4000 * K), # <3>
  ncol = K
))
p <- plogis(eta) # implied predicted probabilities # <4>
extreme <- mean(p < 0.01 | p > 0.99) # <5>

cat("Predicted probabilities below 1% or above 99%: ",
  round(100 * extreme), "%\n",
  sep = ""
)
cat("Try s <- 1 for a prior that implies a reasonable spread.\n")

hist(p, # <6>
  breaks = seq(0, 1, 0.025), col = "#2166ac", border = "white",
  main = "", xlab = "Predicted probability implied by the prior",
  ylab = "Draws"
)

# Annotations
# 1. The page's controls: the prior standard deviation of each coefficient, and the number of standardized predictors.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Draw coefficients from the prior and predictors from their distribution, and form the linear predictor. Its spread is about s times the square root of K.
# 4. The predicted probabilities the prior implies, before any data.
# 5. The share of predictions that are essentially 0 or 1. A wide prior says almost every case is a certainty.
# 6. The prior predictive histogram. Set s to 1 and the pile-up at the edges disappears.
