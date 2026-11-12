# The Status-Reversal Heuristic: would you believe it from a low-status
# source?
bonus <- 1.2 # status bonus (log-odds) # <1>
set.seed(58) # <2>

high <- rep(c(TRUE, FALSE), 2000)
evidence <- rnorm(4000, 0, 1.5) # what the paper shows
correct <- runif(4000) < plogis(evidence) # calibrated truth # <3>
judged <- plogis(evidence + ifelse(high, bonus / 2, -bonus / 2)) # <4>
res <- rbind(
  "High-status source" = c(
    mean(judged[high]),
    mean(correct[high])
  ),
  "Low-status source" = c(
    mean(judged[!high]),
    mean(correct[!high])
  )
)
colnames(res) <- c("confidence", "accuracy")
print(round(100 * res)) # average confidence vs actual accuracy (%)

bin <- cut(judged, seq(0, 1, 0.1))
plot(c(0, 1), c(0, 1), # <5>
  type = "l", lty = 2, xlab = "Judged probability",
  ylab = "Share actually correct"
)
points(tapply(judged[high], bin[high], mean),
  tapply(correct[high], bin[high], mean),
  type = "b", pch = 19,
  col = "#d6604d"
)
points(tapply(judged[!high], bin[!high], mean),
  tapply(correct[!high], bin[!high], mean),
  type = "b", pch = 19,
  col = "#2166ac"
)
legend("topleft", rownames(res),
  col = c("#d6604d", "#2166ac"), pch = 19,
  bty = "n"
)

# Annotations
# 1. The page's control: the status bonus, in log-odds, that a high-status source gets.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Whether each claim is correct depends only on its evidence, not on who made it.
# 4. The reader's judgment adds a bonus for high status and a penalty for low status.
# 5. Calibration by source: high-status claims are believed more than they deserve, low-status ones less. Reversing the status asks what you would think of the evidence alone.
