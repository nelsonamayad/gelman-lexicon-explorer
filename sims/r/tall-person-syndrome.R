# Tall-Person Syndrome: the view from up there exaggerates the advantage.
real_slope <- 0.1 # real association: outcome per sd of height # <1>
perceived <- 0.8 # perceived importance per sd of height
set.seed(110) # <2>

h <- rnorm(1000)
outcome <- real_slope * h + rnorm(1000) # <3>
feel <- perceived * h + rnorm(1000, 0, 0.5) # <4>
cat("Correlation of height with the actual outcome: ",
  round(cor(h, outcome), 2), "\nWith felt importance: ",
  round(cor(h, feel), 2), "\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <5>
plot(h, outcome,
  pch = 19, cex = 0.4, col = "#2166ac", main = "Reality",
  xlab = "Height (sd)", ylab = "Outcome"
)
abline(lm(outcome ~ h), lwd = 2)
plot(h, feel,
  pch = 19, cex = 0.4, col = "#d6604d", main = "How it feels",
  xlab = "Height (sd)", ylab = "Felt importance"
)
abline(lm(feel ~ h), lwd = 2)

# Annotations
# 1. The page's controls: the real association of height with the outcome, and how important height feels from up there.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Reality: a small association.
# 4. How it feels: a large one, because the tall person notices every time height mattered.
# 5. Reality beside the feeling.
