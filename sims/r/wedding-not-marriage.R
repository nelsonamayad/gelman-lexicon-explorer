# The wedding, never about the marriage: corrections get little attention.
delay <- 24 # months until the error is found # <1>
loudness <- 0.08 # correction attention relative to the original
half_life <- 6 # attention half-life (months)
# Deterministic: no random numbers.

t <- 0:120
lam <- log(2) / half_life
wedding <- 100 * exp(-lam * t) # the publication # <2>
marriage <- ifelse(t >= delay, 100 * loudness * exp(-lam * (t - delay)), 0) # <3>
cat("The correction gets ", round(100 * sum(marriage) / sum(wedding), 1),
  "% as much attention as the original\nBy the time the error is ",
  "found, ", round(100 * (1 - exp(-lam * delay))), "% of the paper's ",
  "attention is already spent\n",
  sep = ""
)

matplot(t, cbind(wedding, marriage), # <4>
  type = "l", lty = 1, lwd = 2,
  col = c("#2166ac", "#d6604d"), xlab = "Months since publication",
  ylab = "Attention"
)
legend("topright", c("Original publication", "Correction"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how long until the error is found, how loud the correction is relative to the original, and how fast attention fades. There is no seed: the model is deterministic.
# 2. Attention to the publication, the wedding, decaying from the day it appears.
# 3. Attention to the correction, the marriage: later, quieter, and decaying just as fast.
# 4. Both over ten years. By the time the error is found, most of the attention has already been spent.
