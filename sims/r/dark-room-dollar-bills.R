# In a dark room with most lights covered, a weak beam looks brilliant.
true_pct <- 0.4 # true percentile of the focal idea # <1>
favored <- 0.7 # how much the covering favors weaker rivals
set.seed(140) # <2>

others <- sort(rnorm(199)) # brightness of 199 rivals
focal <- others[floor(true_pct * 198) + 1] # a middling idea # <3>
visible <- 1 - (0:19) * 0.05 # share of rivals left uncovered # <4>
apparent <- sapply(visible, function(vis) {
  cover <- pmin(1, (1 - vis) * ifelse(others > focal, 1 + favored, # <5>
    1 - favored
  ))
  mean(replicate(200, {
    seen <- others[runif(199) >= cover]
    if (length(seen)) mean(seen < focal) else 1
  }))
})

cat("Truly outshines ", round(100 * true_pct), "% of rivals; appears to ",
  "outshine ", round(100 * apparent[1]), "% with every light visible and ",
  round(100 * apparent[20]), "% with most covered\n",
  sep = ""
)

plot(visible, apparent, # <6>
  type = "l", lwd = 3, col = "#e6ab02",
  xlim = c(1, 0.05), ylim = c(0, 1),
  xlab = "Share of rival lights left uncovered",
  ylab = "Share of visible rivals it outshines"
)
abline(h = true_pct, lty = 2)

# Annotations
# 1. The page's controls: the focal idea's true percentile, and how much the covering favors weaker rivals over stronger ones.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A middling idea among 199 rivals.
# 4. Cover up more and more of the rival lights.
# 5. Brighter rivals are more likely to be covered than dimmer ones: that is what the dollar bills do.
# 6. The share of visible rivals the focal idea outshines, as the room darkens. The dashed line is its true standing.
