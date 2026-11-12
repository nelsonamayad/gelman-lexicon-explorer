# The Pinocchio Principle: a half-t prior on a group-level scale.
A <- 2.5 # scale of the prior # <1>
nu <- 1 # degrees of freedom (1 = half-Cauchy)
set.seed(31) # <2>

# |N(0, A)| * sqrt(nu / chi-squared(nu)) is A times the absolute value of a
# t variable with nu degrees of freedom: a half-t prior
tau <- A * abs(rt(20000, nu)) # <3>
print(round(quantile(tau, c(0.5, 0.9, 0.95, 0.99)), 1))

cap <- quantile(tau, 0.95)
hist(tau[tau < cap], # <4>
  breaks = 50, freq = FALSE, col = "grey80",
  border = "white", main = "", xlab = "Group-level scale tau"
)
curve(2 / A * dt(x / A, nu), 0, cap, add = TRUE, col = "#2166ac", lwd = 2)

# Annotations
# 1. The page's controls: the scale of the prior and its degrees of freedom (1 gives a half-Cauchy).
# 2. Fixes the random numbers so the run is reproducible.
# 3. Draws from the half-t prior: the absolute value of a t variable, scaled by A. The redundant multiplicative parameterization that motivates the principle collapses to this.
# 4. The histogram of draws with the density overlaid, showing the prior's heavy tail.
