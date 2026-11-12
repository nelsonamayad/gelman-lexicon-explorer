# The Superplot: rich people vote Republican, rich states vote Democratic.
state_shift <- 0.9 # state-wealth effect (toward Democrats) # <1>
within <- 0.35 # within-state income slope
set.seed(3) # <2>

centers <- c("Poor states" = 2.2, "Middle states" = 3, "Rich states" = 3.8)
alpha <- c(0, -state_shift / 2, -state_shift)
g <- rep(1:3, each = 3000)
inc <- pmin(5, pmax(1, round(rnorm(9000, centers[g], 1)))) # categories
vote <- rbinom(9000, 1, plogis(alpha[g] + within * (inc - 3))) # Rep. # <3>

avg_inc <- tapply(inc, g, mean)
avg_vote <- tapply(vote, g, mean)
between <- coef(lm(avg_vote ~ avg_inc))[[2]] # <4>
cat("Within each kind of state, richer people vote more Republican.\n",
  "Across state averages, the slope is ", round(between, 3),
  " per income category\n",
  sep = ""
)

cols <- c("#d6604d", "grey50", "#2166ac")
plot(NA, # <5>
  xlim = c(1, 5), ylim = c(0, 1), xlab = "Income category",
  ylab = "Share voting Republican"
)
for (k in 1:3) {
  lines(1:5, plogis(alpha[k] + within * (1:5 - 3)),
    col = cols[k], lwd = 2
  )
}
points(avg_inc, avg_vote, pch = 19, col = cols, cex = 1.5)
lines(avg_inc, avg_vote, lty = 2)
legend("topleft", names(centers), col = cols, lwd = 2, bty = "n")

# Annotations
# 1. The page's controls: how much richer states lean Democratic, and the within-state slope of voting on income.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each voter's choice depends on their own income (richer, more Republican) and on their state (richer state, less Republican).
# 4. The slope across state averages, which runs the other way.
# 5. The superplot: one line per kind of state, all sloping up, and the state averages connected by a dashed line sloping down. Both patterns in one picture.
