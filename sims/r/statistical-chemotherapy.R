# Statistical Chemotherapy: inflate the standard errors until the
# inconvenient result goes away.
z_key <- 3 # z of the key result (before chemo) # <1>
z_placebo <- 2.3 # z of the placebo test (before chemo)
dose <- 1.3 # chemo dose: standard-error multiplier
# Deterministic: no random numbers.

p_value <- function(z, c) 2 * (1 - pnorm(abs(z) / c)) # <2>
c_grid <- seq(1, 2.5, by = 0.05)
pk <- p_value(z_key, dose) # <3>
pp <- p_value(z_placebo, dose)
cat("At dose ", dose, ": key result p = ", round(pk, 3),
  ", placebo test p = ", round(pp, 3), "\n",
  sep = ""
)
cat(if (pk < 0.05 && pp >= 0.05) {
  "Treatment \"successful\": the placebo
  test has gone away and the key result survives.\n"
} else if (pk < 0.05) {
  "Both still significant: needs a stronger dose.\n"
} else {
  "Too strong: the key result is gone too.\n"
})

matplot(c_grid, cbind(p_value(z_key, c_grid), p_value(z_placebo, c_grid)), # <4>
  type = "l", lty = 1, lwd = 2, log = "y",
  col = c("#2166ac", "#d6604d"), xlab = "Standard-error multiplier",
  ylab = "p-value"
)
abline(h = 0.05, lty = 2)
abline(v = dose, col = "grey60")
legend("bottomright", c("Key result", "Placebo test (should be null)"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: the z statistics of the key result and the placebo test, and the chemo dose, a multiplier on the standard errors. There is no seed: the model is deterministic.
# 2. A p-value after the standard errors have been inflated by c.
# 3. Both p-values at the chosen dose. The data have not changed, only the uncertainty attributed to them.
# 4. Both p-values as the dose rises. A dose between the two crossing points kills the placebo result and spares the key one: the treatment is a success.
