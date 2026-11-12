# As They Say in the Stagecoach Business: remove the padding and the ride
# gets rough. How much smoothing helps you read the signal?
padding <- 1 # smoothing window (odd number of points) # <1>
set.seed(28) # <2>

n <- 200
i <- 1:n
msg <- sin(i / 18) + 0.5 * sin(i / 7) # the message
obs <- msg + rnorm(n, 0, 0.6) # what arrives # <3>
smooth <- function(w) { # <4>
  sapply(i, function(k) {
    mean(obs[max(1, k - (w - 1) / 2):min(n, k + (w - 1) / 2)])
  })
}
err <- sapply(seq(1, 61, 2), function(w) sqrt(mean((smooth(w) - msg)^2))) # <5>
best <- seq(1, 61, 2)[which.min(err)]
cat("Error with padding ", padding, ": ",
  round(sqrt(mean((smooth(padding) - msg)^2)), 3), "\nBest padding: ",
  best, " (error ", round(min(err), 3), ")\n",
  sep = ""
)

plot(i, obs, # <6>
  col = "grey70", pch = 19, cex = 0.5, xlab = "Time",
  ylab = "Signal"
)
lines(i, msg, lty = 2, lwd = 2)
lines(i, smooth(padding), col = "#2166ac", lwd = 2)

# Annotations
# 1. The page's control: the smoothing window, the padding in the stagecoach line.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The message plus noise: what arrives.
# 4. A running mean over a window of w points.
# 5. The error of the smoothed signal against the true message, for every window width.
# 6. The noisy observations, the true message dashed and the smoothed signal in blue. Too little padding and the ride is rough; too much and the message blurs.
