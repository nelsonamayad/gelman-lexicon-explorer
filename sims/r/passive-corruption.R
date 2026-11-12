# Passive Corruption: silence lets bad work take over a field.
adv <- 0.12 # growth advantage of bad work # <1>
speak <- 0.05 # probability someone who knows speaks up, per year
# Deterministic: no random numbers. Bad work starts at 10% of the field.

run <- function(s) { # <2>
  bad <- 0.1
  for (t in 1:40) {
    b <- bad[t] * (1 + adv) * (1 - s) # <3>
    bad <- c(bad, b / (b + (1 - bad[t])))
  }
  bad
}
share <- cbind(
  "Your setting" = run(speak), "Total silence" = run(0),
  "Active correction" = run(0.3)
)
cat("Share of the field that is bad work after 40 years (%):\n")
print(round(100 * share[41, ]))

matplot(0:40, share, # <4>
  type = "l", lty = 1, lwd = 2, ylim = c(0, 1),
  col = c("#2166ac", "#d6604d", "#4daf4a"), xlab = "Year",
  ylab = "Share of the field that is bad work"
)
legend("topleft", colnames(share),
  col = c("#2166ac", "#d6604d", "#4daf4a"),
  lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how much faster bad work spreads than good work, and how often someone who knows speaks up. There is no seed: the model is deterministic.
# 2. The share of the field that is bad work over 40 years, for a given rate of speaking up.
# 3. Each year bad work grows by its advantage and shrinks by the share that gets called out.
# 4. Three futures: your setting, total silence, and active correction. Silence is not neutral.
