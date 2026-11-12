# Panglossian Fallacy: assuming the odds were right because they're odds.
k <- 4 # how much long shots are underpriced # <1>
n_events <- 20000 # priced events in the track record
set.seed(116) # <2>

# Implied probabilities from 1 in 5,000 to 1 in 2, even on the log scale
implied <- exp(log(1 / 5000) + runif(n_events) * log(5000 / 2))
true_odds <- k * implied / (1 - implied) # true odds k times implied odds # <3>
won <- runif(n_events) < true_odds / (1 + true_odds)

edges <- c(1 / 5000, 1 / 1000, 1 / 200, 1 / 50, 1 / 10, 1 / 2)
bin <- cut(implied, edges, right = FALSE)
calib <- data.frame( # <4>
  implied = tapply(implied, bin, mean),
  observed = tapply(won, bin, mean)
)
print(signif(calib, 2))

long <- as.integer(bin) <= 3 # long shots: worse than 1 in 50
ratio <- sum(won[long]) / sum(implied[long]) # <5>
se <- sqrt(max(sum(won[long]), 1)) / sum(implied[long])
cat("Long shots won ", round(ratio, 1), " times as often as the odds ",
  "implied\n", if (ratio - 2 * se > 1) {
    "The odds were wrong."
  } else {
    "Consistent with calibrated odds."
  }, "\n",
  sep = ""
)

plot(calib$implied, calib$observed, # <6>
  log = "xy", pch = 19, col = "#d6604d",
  xlab = "Implied probability", ylab = "Observed win rate"
)
abline(0, 1, lty = 2)

# Annotations
# 1. The page's controls: how much the market underprices long shots, and how many priced events are in the record.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The true odds of each event, k times the odds the market implied: the market is wrong about long shots.
# 4. Calibration: the observed win rate in bins of implied probability.
# 5. How much more often long shots won than the odds implied, and whether the gap is beyond chance.
# 6. Observed against implied win rates. Points above the diagonal are the market's long-shot error, visible only because someone checked.
