# Anthropic principle: which effects can statistics study at all?
n_max <- 3 # log10 of the largest feasible sample size # <1>
obvious <- 2 # naked-eye threshold (effect in sd units)
set.seed(119) # <2>

detect <- 2.8 / sqrt(10^n_max) # effect detectable with ~80% power # <3>
eff <- 10^runif(4000, -4, 1) # effects spread over five orders of magnitude # <4>
zone <- ifelse(eff < detect, "Too small to detect", # <5>
  ifelse(eff > obvious, "Obvious without statistics",
    "Statistics territory"
  )
)
print(round(100 * prop.table(table(zone))))

breaks <- seq(-4, 1, length.out = 51)
mid <- (head(breaks, -1) + tail(breaks, -1)) / 2
cols <- ifelse(10^mid < detect, "grey70",
  ifelse(10^mid > obvious, "#d6604d", "#2166ac")
)
hist(log10(eff), # <6>
  breaks = breaks, col = cols, border = "white", main = "",
  xlab = "True effect size (sd units, log10 scale)", ylab = "Phenomena"
)
legend("topleft", c("Too small", "Statistics territory", "Obvious"),
  fill = c("grey70", "#2166ac", "#d6604d"), cex = 0.8, bty = "n"
)

# Annotations
# 1. The page's controls: the largest feasible sample size, as a power of ten, and the effect size that is obvious without statistics.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The smallest effect a study of the largest feasible size can detect with about 80% power.
# 4. True effects spread evenly over five orders of magnitude.
# 5. Each effect lands in one of three zones. Only the middle one is where statistics is needed and can work.
# 6. The histogram on a log scale, colored by zone. The blue band is the anthropic window.
