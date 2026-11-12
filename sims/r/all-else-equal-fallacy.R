# The "All Else Equal" Fallacy: a regression coefficient vs an intervention.
beta <- 0.5 # direct effect of X on Y # <1>
delta <- -1 # how Z responds to X
gamma <- 0.8 # effect of Z on Y
set.seed(17) # <2>

simulate <- function(shift) {
  x <- rnorm(2000) + shift
  z <- delta * x + rnorm(2000) # <3>
  data.frame(x, z, y = beta * x + gamma * z + rnorm(2000))
}
obs <- simulate(0)
coef <- coef(lm(y ~ x + z, data = obs))[["x"]] # "all else equal" # <4>
after <- simulate(1) # raise X by 1 and let Z respond
total <- mean(after$y) - mean(obs$y) # <5>

cat("Regression coefficient (all else equal):", round(coef, 2), "\n")
cat("Actual effect of raising X by 1:", round(total, 2), "\n")
cat("Theory, beta + gamma * delta:", beta + gamma * delta, "\n")

barplot(c("Regression coefficient" = coef, "Actual effect" = total), # <6>
  horiz = TRUE, col = c("#2166ac", "#d6604d"), xlim = c(-2.5, 2.5),
  xlab = "Change in Y", las = 1, cex.names = 0.8
)
abline(v = 0)

# Annotations
# 1. The page's controls: the direct effect of X on Y, how Z responds to X, and the effect of Z on Y.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Z responds to X. That is what makes holding Z constant different from intervening on X.
# 4. The regression coefficient on X, which holds Z fixed: the all-else-equal comparison.
# 5. What actually happens to Y when X is raised by one unit and Z is allowed to respond.
# 6. The two numbers side by side. They agree only when Z does not respond to X.
