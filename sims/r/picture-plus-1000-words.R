# A picture plus 1000 words: the same scatterplot, with and without words.
words <- TRUE # add grouping and annotation # <1>
set.seed(73) # <2>

# Three clinics: within each, more dose means a better outcome
clinic <- rep(c("Clinic A", "Clinic B", "Clinic C"), each = 60)
k <- rep(0:2, each = 60)
x <- rnorm(180, 2 + 2.5 * k, 0.8)
y <- 10 - 3 * k + 1.2 * (x - 2 - 2.5 * k) + rnorm(180, 0, 0.7) # <3>

cat("Slope ignoring clinics:", round(coef(lm(y ~ x))[[2]], 2), "\n")
cat(
  "Slope within clinics:",
  round(coef(lm(y ~ x + clinic))[["x"]], 2), "\n"
)

cols <- c("#2166ac", "#d6604d", "#1a9850")
plot(x, y, # <4>
  pch = 19, col = if (words) cols[k + 1] else "grey40",
  xlab = "Dose", ylab = "Outcome"
)
abline(lm(y ~ x), lty = 2)
if (words) { # <5>
  for (j in 0:2) {
    abline(lm(y[k == j] ~ x[k == j]),
      col = cols[j + 1],
      lwd = 2
    )
  }
  legend("topright", unique(clinic), col = cols, pch = 19, bty = "n")
  text(7.5, 9.5, "Within each clinic,\nmore dose -> better outcome",
    adj = 0, cex = 0.8
  )
}

# Annotations
# 1. The page's control: whether to add the words (grouping and annotation).
# 2. Fixes the random numbers so the run is reproducible.
# 3. Three clinics: within each, more dose means a better outcome, but clinics with higher doses have worse outcomes overall.
# 4. The picture alone, with one overall line that slopes the wrong way.
# 5. The thousand words: colors, per-clinic lines, a legend and a sentence that says what to see.
