# The capacity to be upset: flagging residuals that don't fit.
k <- 2 # how hard to upset: flag residuals beyond k sd # <1>
shift <- 1.2 # size of the real anomaly (sd units)
set.seed(146) # <2>

t <- 0:299
real <- t >= 200 & t < 240 # the real anomaly # <3>
resid <- rnorm(300, ifelse(real, shift, 0), 1) # <4>
flagged <- abs(resid) > k # <5>

cat(
  "Flagged", sum(real & flagged), "of the anomaly's 40 points, with",
  sum(!real & flagged), "false alarms elsewhere\n"
)

plot(t, resid, # <6>
  pch = 19, cex = 0.6,
  col = ifelse(flagged, "#d6604d", "grey50"),
  xlab = "Measurement", ylab = "Residual (sd units)"
)
rect(200, -10, 240, 10, col = adjustcolor("#2166ac", 0.1), border = NA)
abline(h = c(-k, k), lty = 2)

# Annotations
# 1. The page's controls: how far a residual must stray before it upsets you, and how large the real anomaly is.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Forty consecutive measurements where the model is genuinely wrong.
# 4. Residuals: pure noise everywhere except inside the anomaly, where they are shifted.
# 5. The rule for being upset: flag any residual beyond k standard deviations.
# 6. Residuals over time, flagged ones in red, with the true anomaly shaded. Too high a k and the anomaly slips through; too low and false alarms pile up.
