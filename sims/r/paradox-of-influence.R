# The Paradox of Influence: pander more, get heeded more, add less.
my_w <- 0.7 # how much you pander (w) # <1>
set.seed(68) # <2>

truth <- rnorm(3000)
pref <- rnorm(3000) # what's right; what boss wants
signal <- truth + rnorm(3000, 0, 0.5) # your honest read
w <- seq(0, 1, by = 0.05)
heeded <- 0.2 + 0.75 * w # pandering gets you listened to # <3>
info <- sapply(w, function(wk) { # <4>
  advice <- (1 - wk) * signal + wk * pref
  resid <- advice - wk * pref # what the boss didn't know
  if (wk < 1) max(0, cor(resid, truth)) * (1 - wk) else 0
})
impact <- heeded * info # <5>
me <- which.min(abs(w - my_w))
best <- which.max(impact)
cat("At w = ", my_w, ": heeded ", round(100 * heeded[me]),
  "%, impact ", round(impact[me], 2), "\nImpact is largest at w = ",
  w[best], " (", round(impact[best], 2), ")\n",
  sep = ""
)

matplot(w, cbind(heeded, info, impact), # <6>
  type = "l", lty = 1, lwd = 2,
  col = c("grey50", "#2166ac", "#d6604d"),
  xlab = "How much you pander (w)", ylab = ""
)
legend("top", c("Heeded", "Information added", "Real impact"),
  col = c("grey50", "#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's control: how much you pander to what the boss already wants.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Pandering gets your advice heeded more often.
# 4. But advice that repeats the boss's preferences adds less information.
# 5. Your real impact is the product: how often you are heeded, times how much you add.
# 6. The three curves. Impact peaks at moderate pandering and collapses at full agreement: the paradox.
