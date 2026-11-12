# The Piranha Principle: there can't be many large independent effects.
r <- 0.3 # claimed correlation of each factor with the outcome # <1>
K <- 20 # number of claimed independent factors
# Deterministic: no random numbers. Independent factors with correlation
# r each explain r^2 of the variance, and the shares can't add past 100%.

explained <- K * r^2 # <2>
max_k <- floor(1 / r^2) # <3>
cat(K, " factors with r = ", r, " would explain ", round(100 * explained),
  "% of the variance\nAt most ", max_k, " such factors can coexist\n",
  sep = ""
)

k <- 1:50
plot(k, k * r^2, # <4>
  type = "h", lwd = 4,
  col = ifelse(k * r^2 > 1, "#d6604d", "#2166ac"),
  xlab = "Number of independent factors",
  ylab = "Share of variance explained"
)
abline(h = 1, lty = 2)
abline(v = K, col = "grey50")

# Annotations
# 1. The page's controls: the claimed correlation of each factor with the outcome, and how many such factors are claimed. There is no seed: the model is deterministic.
# 2. Independent factors each explain r squared of the variance, and the shares add.
# 3. The most such factors that can coexist before the shares exceed 100%.
# 4. Variance explained against the number of factors. The red bars are impossible: the piranhas would have eaten each other.
