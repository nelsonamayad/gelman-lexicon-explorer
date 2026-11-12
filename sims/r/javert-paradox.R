# The Javert Paradox: persistent enough to work, not so much as to be Javert.
responsiveness <- 0.06 # how much each push moves the authors # <1>
tolerance <- 4 # pushes the community tolerates before "obsessive"
# Deterministic: no random numbers.

pushes <- 0:20
corrected <- 1 - exp(-responsiveness * pushes^2 / 4) # chance of a fix # <2>
obsessive <- plogis(pushes - tolerance) # seen as a Javert # <3>
sweet <- pushes[corrected > 0.5 & obsessive < 0.5] # <4>

if (length(sweet)) {
  cat("Sweet spot:", min(sweet), "to", max(sweet), "pushes\n")
} else {
  cat("No persistence level works without looking like Javert\n")
}

matplot(pushes, cbind(corrected, obsessive), # <5>
  type = "l", lty = 1, lwd = 2,
  col = c("#2166ac", "#d6604d"), xlab = "Times the critic pushes",
  ylab = "Probability"
)
abline(h = 0.5, lty = 2)
legend("right", c("Error gets corrected", "Critic seen as obsessive"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how much each push moves the authors, and how many pushes the community tolerates. There is no seed: the model is deterministic.
# 2. The chance that the error gets corrected, which rises slowly with persistence.
# 3. The chance that the critic is seen as a Javert, which rises past the community's tolerance.
# 4. The sweet spot, if any: persistence that probably works without looking obsessive.
# 5. Both curves. When they cross before correction becomes likely, no level of persistence is both effective and respectable.
