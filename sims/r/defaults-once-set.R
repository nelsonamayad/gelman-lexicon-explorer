# Defaults, once set, are hard to change: adoption with switching costs.
gap <- 0.3 # quality advantage of the new method # <1>
cost <- 1.1 # individual switching cost
coord <- 1 # coordination benefit (grows with the share who switched)
set.seed(39) # <2>

N <- 1000
switched <- runif(N) < 0.02 # a few early adopters # <3>
share <- numeric(61)
for (t in 0:60) {
  share[t + 1] <- mean(switched)
  tempted <- gap + coord * mean(switched) - cost + rnorm(N, 0, 0.3) > 0 # <4>
  switched <- switched | (tempted & runif(N) < 0.3)
}
half <- which(share >= 0.5)[1] - 1 # <5>

if (is.na(half)) {
  cat("Never reaches half adoption within 60 years\n")
} else {
  cat("Half the field switches after", half, "years\n")
}
cat("Final share: ", round(100 * share[61]), "%\n", sep = "")

plot(0:60, share, # <6>
  type = "l", lwd = 2, col = "#2166ac", ylim = c(0, 1),
  xlab = "Years after the better method appears",
  ylab = "Share using the new method"
)
abline(h = 0.5, lty = 2)

# Annotations
# 1. The page's controls: how much better the new method is, what switching costs an individual, and how much the benefit of switching grows with the share who already have.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A few early adopters.
# 4. Each year, a person is tempted to switch if the quality gap plus the coordination benefit outweighs the switching cost, give or take.
# 5. When half the field has switched, if ever.
# 6. Adoption over 60 years. A better method with a high switching cost can stall below the tipping point for decades.
