# Meritocracy won't happen: selection on merit turns into inheritance.
gamma <- 2.5 # advantage passed on by elite status # <1>
noise <- 0.7 # measurement noise in the merit score
set.seed(128) # <2>

N <- 3000
elite <- rep(FALSE, N)
res <- t(sapply(1:10, function(g) {
  merit <- rnorm(N)
  score <- merit + gamma * elite + rnorm(N, 0, noise) # <3>
  new_elite <- score > sort(score, decreasing = TRUE)[N * 0.1 + 1] # <4>
  inherited <- if (g == 1) 0.1 else mean(elite[new_elite]) # <5>
  r <- cor(as.numeric(new_elite), merit)
  elite <<- new_elite
  c(generation = g, inherited = inherited, merit_cor = r)
}))
cat("Generation 10: ", round(100 * res[10, "inherited"]),
  "% of the elite had elite parents (10% = no inheritance)\n",
  sep = ""
)
cat(
  "Correlation of elite status with true merit: generation 1",
  round(res[1, "merit_cor"], 2), "| generation 10",
  round(res[10, "merit_cor"], 2), "\n"
)

matplot(res[, 1], res[, 2:3], # <6>
  type = "b", pch = 19, lty = 1,
  col = c("#d6604d", "#2166ac"), ylim = c(0, 1),
  xlab = "Generation", ylab = ""
)
legend("right", c("Elite with elite parents", "Correlation with merit"),
  col = c("#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: how much advantage elite parents pass on, and how noisily merit is measured.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each generation's measured score: true merit, plus the advantage of elite parents, plus noise.
# 4. The top tenth by score becomes the new elite.
# 5. What share of the new elite had elite parents. With no inheritance it would be 10%.
# 6. Over ten generations, elite status becomes inherited and its correlation with merit falls, even though every generation selected on the measured score.
