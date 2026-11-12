# A probability isn't just a number: correlated outcomes in two states.
p_A <- 0.7 # P(win state A) = P(win state B) # <1>
rho <- 0.7 # correlation between the states' outcomes
set.seed(114) # <2>

N <- 40000
cut <- qnorm(1 - p_A)
z1 <- rnorm(N)
z2 <- rho * z1 + sqrt(1 - rho^2) * rnorm(N) # <3>
A <- z1 > cut
B <- z2 > cut
probs <- c( # <4>
  "P(A)" = mean(A), "P(B)" = mean(B), "P(A and B)" = mean(A & B),
  "P(B | won A)" = mean(B[A]), "P(B | lost A)" = mean(B[!A])
)
print(round(probs, 2))
cat(
  "If the states were independent, P(A and B) would be",
  round(p_A^2, 2), "\n"
)

par(mar = c(4, 8, 1, 1))
barplot(rev(probs), # <5>
  horiz = TRUE, las = 1, xlim = c(0, 1),
  col = "#2166ac", xlab = "Probability"
)

# Annotations
# 1. The page's controls: the probability of winning each state, and the correlation between the two outcomes.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The two states' outcomes share a common component, so they move together.
# 4. The marginal probabilities, the joint probability and the conditionals. The number 0.7 alone determines none of the last three.
# 5. The probabilities side by side. A probability comes with a joint distribution, not just a number.
