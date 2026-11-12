# Institutional decision making: when to test homes for radon.
test_cost <- 50 # cost of a test ($) # <1>
fix_cost <- 1500 # cost of remediation ($)
benefit <- 700 # health value per unit of radon removed ($)
set.seed(5) # <2>

s <- 0.6 # model's predictive sd (log scale)
pred <- rnorm(2000, 0.4, 0.7) # predicted log radon for each home # <3>
level <- exp(rnorm(2000, pred, s)) # true radon level
gain <- function(l) pmax(benefit * (l - 1) - fix_cost, 0) # test, then fix
fix_gain <- function(l) benefit * pmax(l - 1, 0) - fix_cost # fix, no test

# Expected values over each home's predictive distribution (grid over z)
z <- seq(-4, 4, by = 0.05)
wz <- dnorm(z) * 0.05
L <- exp(outer(pred, s * z, "+"))
e_fix <- benefit * (pmax(L - 1, 0) %*% wz) - fix_cost # <4>
e_test <- gain(L) %*% wz - test_cost # <5>
best <- pmax(0, e_fix, e_test) # <6>
decision <- ifelse(best == 0, 0, ifelse(best == e_fix, fix_gain(level),
  gain(level) - test_cost
))
per_home <- c(
  "Do nothing" = 0, "Remediate all" = mean(fix_gain(level)),
  "Test all" = mean(gain(level) - test_cost),
  "Decision analysis" = mean(decision)
)
print(round(per_home)) # net value per home ($)

par(mar = c(4, 9, 1, 1))
barplot(per_home, # <7>
  horiz = TRUE, las = 1,
  col = c("grey70", "grey70", "grey70", "#2166ac"),
  xlab = "Net value per home ($)"
)

# Annotations
# 1. The page's controls: the cost of a radon test, the cost of remediation, and the health value of each unit of radon removed.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A model's prediction of each home's radon level, with uncertainty.
# 4. The expected value of remediating without testing, averaged over the home's predictive distribution.
# 5. The expected value of testing first and remediating only if the test warrants it.
# 6. The decision analysis: for each home, do nothing, remediate, or test, whichever has the highest expected value.
# 7. Net value per home of the four policies. Making the decision home by home, from the model's uncertainty, beats every blanket rule.
