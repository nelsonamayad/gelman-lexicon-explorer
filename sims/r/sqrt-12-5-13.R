# sqrt(12^2 + 5^2) = 13: independent errors add in quadrature.
s1 <- 12 # error source 1 (sd) # <1>
s2 <- 5 # error source 2 (sd)
set.seed(101) # <2>

mc <- function(a, b) sd(rnorm(20000, 0, a) + rnorm(20000, 0, b)) # <3>
scen <- rbind(
  "As is" = c(s1, s2), "Halve source 1" = c(s1 / 2, s2),
  "Halve source 2" = c(s1, s2 / 2),
  "Eliminate source 2" = c(s1, 0)
)
total <- cbind(
  formula = sqrt(scen[, 1]^2 + scen[, 2]^2), # <4>
  simulated = apply(scen, 1, function(s) mc(s[1], s[2]))
)
print(round(total, 2)) # total error (sd) in each scenario

par(mar = c(4, 9, 1, 1))
barplot(rev(total[, "formula"]), # <5>
  horiz = TRUE, las = 1,
  col = "#2166ac", xlab = "Total error (sd)"
)

# Annotations
# 1. The page's controls: the two error sources' standard deviations.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A Monte Carlo check: the standard deviation of the sum of two independent errors.
# 4. The formula: independent errors add in quadrature, so the larger one dominates.
# 5. Total error in each scenario. Halving the small source barely helps; work on the big one.
