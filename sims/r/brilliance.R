# Brilliance: an upper bound on the quality of reasoning, but no lower bound.
compromised <- 0.3 # share compromised on this question # <1>
set.seed(105) # <2>

B <- rbeta(1000, 2, 2) # brilliance # <3>
comp <- runif(1000) < compromised # motivated or out of field
M <- ifelse(comp, rbeta(1000, 4, 1.5), rbeta(1000, 1, 8)) # how compromised # <4>
Q <- B * (1 - M) # quality of reasoning # <5>

top <- B > 0.8
cat(
  "Of the", sum(top), "most brilliant thinkers (brilliance > 0.8),",
  sum(Q[top] < 0.3), "reason worse than 0.3 on this question\n"
)

plot(B, Q, # <6>
  pch = 16, cex = 0.6, xlim = c(0, 1), ylim = c(0, 1),
  col = ifelse(comp, "#d6604d", "#2166ac"), xlab = "Brilliance",
  ylab = "Quality of reasoning on this question"
)
abline(0, 1, lty = 2) # brilliance is a ceiling
legend("topleft", c("Compromised", "Not compromised"),
  col = c("#d6604d", "#2166ac"), pch = 16, bty = "n"
)

# Annotations
# 1. The page's control: the share of thinkers who are compromised on this question, by motivated reasoning or by being out of their field.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each thinker's brilliance, between 0 and 1.
# 4. How compromised each one is: heavily if compromised, hardly at all otherwise.
# 5. The quality of reasoning on this question. Brilliance sets the ceiling; being compromised brings it down to any level.
# 6. Quality against brilliance. Everything lies under the diagonal, and red points can be anywhere under it.
