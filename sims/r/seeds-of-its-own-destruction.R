# Seeds of its own destruction: a histogram that shows its own noise.
bins <- 40 # number of bins between -4 and 4 # <1>
n <- 1000 # sample size
set.seed(112) # <2>

x <- rnorm(n)
per_bin <- n * (8 / bins) * dnorm(0) # count in a central bin # <3>
cat("With ", bins, " bins, central bars hold about ", round(per_bin),
  " points each,\nso their heights wobble by about +/-",
  round(sqrt(per_bin)), " (", round(100 / sqrt(per_bin)), "%)\n",
  sep = ""
)

par(mfrow = c(2, 2), mar = c(3, 3, 2, 1)) # <4>
for (k in c(
  "Too coarse" = 8, "Default-ish" = 20, "Your choice" = bins,
  "Too fine" = 160
)) {
  hist(x[abs(x) < 4],
    breaks = seq(-4, 4, length = k + 1),
    col = "#2166ac", border = "white", main = paste(k, "bins"),
    xlab = "", ylab = ""
  )
}

# Annotations
# 1. The page's controls: the number of bins and the sample size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The expected count in a central bin, whose square root is the wobble in the bar heights: the noise the graph should let you see.
# 4. The same sample binned four ways. Too coarse hides the noise, too fine drowns the shape; in between, the bar-to-bar jitter is the seed of its own destruction.
