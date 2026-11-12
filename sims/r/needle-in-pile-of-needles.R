# Looking for a needle in a pile of needles: a placebo test.
beta <- 0.05 # true effect of the intervention # <1>
confound <- 0.6 # correlation of the intervention with background growth
set.seed(88) # <2>

# 500 replications of a 43-city study
est <- t(replicate(500, {
  g <- rnorm(43) # background growth of each city
  x <- confound * g + sqrt(1 - confound^2) * rnorm(43) # intervention # <3>
  pre <- g + rnorm(43, 0, 0.5) # growth before 1918 # <4>
  post <- g + beta * x + rnorm(43, 0, 0.5) # growth after 1918
  c(placebo = coef(lm(pre ~ x))[[2]], claimed = coef(lm(post ~ x))[[2]]) # <5>
}))
avg <- sprintf("%.2f", colMeans(est))
cat("Average estimate: claimed effect ", avg[2], ", placebo (before 1918) ",
  avg[1], ", true effect ", beta, "\n",
  sep = ""
)

boxplot(est, # <6>
  names = c("Placebo: before 1918", "Claimed: after 1918"),
  col = c("grey70", "#2166ac"), ylab = "Estimated effect"
)
abline(h = beta, lty = 2)

# Annotations
# 1. The page's controls: the intervention's true effect, and how correlated it is with the cities' background growth.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Cities that were already growing were likelier to adopt the intervention.
# 4. The placebo outcome: growth before the intervention, which it cannot have caused.
# 5. The claimed effect and the placebo estimate, from the same regression on each period.
# 6. The two estimates across 500 replications. The placebo finds the same effect, so the needle is just another needle.
