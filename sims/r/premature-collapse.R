# Premature collapsing of the wave function: decide with the uncertainty.
cost <- 0.2 # cost of implementing an intervention # <1>
se <- 0.4 # standard error of each study
set.seed(152) # <2>

tau <- 0.4
theta <- rnorm(5000, 0.1, tau) # true effects of 5000 interventions
y <- rnorm(5000, theta, se) # one study of each
collapsed <- ifelse(abs(y / se) > 1.96, y, 0) # significant, else zero # <3>
post <- (0.1 / tau^2 + y / se^2) / (1 / tau^2 + 1 / se^2) # posterior mean # <4>

value <- c( # <5>
  "Collapse early (significance, then decide)" =
    sum((theta - cost)[collapsed > cost]),
  "Carry uncertainty to the decision" =
    sum((theta - cost)[post > cost]),
  "Oracle (knows the true effects)" =
    sum((theta - cost)[theta > cost])
) / 5000
print(round(value, 3)) # average net value per intervention

par(mar = c(4, 17, 1, 1))
barplot(value, # <6>
  horiz = TRUE, las = 1, cex.names = 0.7,
  col = c("#d6604d", "#2166ac", "grey70"),
  xlab = "Average net value per intervention"
)

# Annotations
# 1. The page's controls: the cost of implementing an intervention and the standard error of each study.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Premature collapse: each study's estimate is reduced to significant-or-not, and the non-significant ones become exactly zero.
# 4. Carrying the uncertainty: the posterior mean, which keeps every estimate and shrinks it.
# 5. The net value of implementing whatever each rule recommends, with an oracle for comparison.
# 6. Average value per intervention under the three rules. Collapsing early throws away value that the posterior keeps.
