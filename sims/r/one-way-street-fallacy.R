# The One-Way Street Fallacy: an average effect hides effects in both
# directions.
mu <- -0.2 # average effect # <1>
sigma <- 1 # spread of individual effects
set.seed(45) # <2>

tau <- rnorm(5000, mu, sigma) # each person's own effect # <3>
cat("Average effect: ", round(mean(tau), 2), "\n",
  round(100 * mean(tau > 0)), "% are helped (average +", # <4>
  round(mean(tau[tau > 0]), 2), "), ", round(100 * mean(tau <= 0)),
  "% are hurt (average ", round(mean(tau[tau <= 0]), 2), ")\n",
  sep = ""
)

hist(tau, # <5>
  breaks = 60, col = ifelse(seq(-5, 5, length = 60) > 0,
    "#2166ac", "#d6604d"
  ),
  border = "white", main = "", xlab = "Individual effect",
  ylab = "People"
)
abline(v = c(0, mean(tau)), lty = c(2, 1), lwd = c(1, 2))

# Annotations
# 1. The page's controls: the average effect and how much individual effects vary around it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each person's own effect, drawn around the average.
# 4. The share helped and the share hurt, with the average effect in each group.
# 5. The distribution of individual effects. An average on one side of zero does not make it a one-way street.
