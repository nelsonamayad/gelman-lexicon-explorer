# Probability: a long-run frequency, and a degree of belief that learns.
p <- 0.3 # true probability of heads # <1>
flips <- 200 # number of flips
set.seed(10) # <2>

heads <- cumsum(rbinom(flips, 1, p)) # <3>
n <- 1:flips
a <- 1 + heads
b <- 1 + n - heads # Beta posterior, uniform prior
post <- a / (a + b) # <4>
sdv <- sqrt(a * b / ((a + b)^2 * (a + b + 1)))
lo <- pmax(0, post - 1.645 * sdv)
hi <- pmin(1, post + 1.645 * sdv)
cat("After ", flips, " flips: frequency ", round(heads[flips] / flips, 3),
  ", 90% interval ", round(lo[flips], 2), " to ", round(hi[flips], 2),
  "\n",
  sep = ""
)

plot(n, heads / n, # <5>
  type = "l", col = "grey50", ylim = c(0, 1),
  xlab = "Flips", ylab = "Probability of heads"
)
polygon(c(n, rev(n)), c(lo, rev(hi)),
  col = adjustcolor("#2166ac", 0.2),
  border = NA
)
lines(n, post, col = "#2166ac", lwd = 2)
abline(h = p, lty = 2)

# Annotations
# 1. The page's controls: the coin's true probability of heads and the number of flips.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The running count of heads: the long-run frequency view.
# 4. The posterior mean under a uniform prior: the degree-of-belief view, which learns from the same flips.
# 5. Frequency and posterior with its 90% band, converging on the truth from different directions.
