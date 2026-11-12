# That narrow beach: where statistics beats eyeballing the data.
n <- 30 # observations per decision # <1>
set.seed(135) # <2>

# For each signal-to-noise ratio, 600 decisions about the sign of an effect
snr <- 10^(-2 + 0:24 * 0.125) # <3>
res <- t(sapply(snr, function(s) {
  hits <- replicate(600, {
    sign <- if (runif(1) < 0.5) 1 else -1
    y <- rnorm(n, sign * s, 1)
    glance <- median(y[1:3]) # eyeball: a quick look at 3 points # <4>
    c(eye = sign(glance) == sign, stat = sign(mean(y)) == sign)
  })
  rowMeans(hits)
}))
gap <- res[, "stat"] - res[, "eye"] # <5>
cat("Statistics helps most at signal/noise ", signif(snr[which.max(gap)], 2),
  ": ", round(100 * res[which.max(gap), "stat"]), "% right vs ",
  round(100 * res[which.max(gap), "eye"]), "% by eye\n",
  sep = ""
)

matplot(snr, res, # <6>
  type = "l", lty = 1, lwd = 2, log = "x",
  col = c("#d6604d", "#2166ac"), ylim = c(0.5, 1),
  xlab = "Signal-to-noise ratio", ylab = "Share of correct decisions"
)
legend("topleft", c("Eyeball", "Statistics"),
  col = c("#d6604d", "#2166ac"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's control: observations per decision.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Signal-to-noise ratios from hopeless to obvious.
# 4. Eyeballing: a quick look at three points. Statistics: the mean of all n.
# 5. How much statistics adds, at each ratio.
# 6. Both methods' accuracy. At the left nothing works; at the right anyone can see it; statistics matters only on the narrow beach between.
