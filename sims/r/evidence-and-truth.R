# Evidence and Truth: they're different.
pi_true <- 0.3 # share of claims that are true # <1>
signal <- 1.5 # typical evidence strength (z) for true claims
set.seed(85) # <2>

true_claim <- runif(3000) < pi_true
z <- rnorm(3000, ifelse(true_claim, signal, 0), 1) # each claim's evidence # <3>
strong <- z > 1.96 # <4>

cat("Claims with strong evidence that are false: ",
  round(100 * mean(!true_claim[strong])), "%\n",
  sep = ""
)
cat("True claims with only weak evidence: ",
  round(100 * mean(!strong[true_claim])), "%\n",
  sep = ""
)

breaks <- seq(floor(min(z)), ceiling(max(z)), by = 0.25)
hist(z[!true_claim], # <5>
  breaks = breaks, col = adjustcolor("#d6604d", 0.5),
  border = "white", main = "", xlab = "Strength of evidence (z)",
  ylab = "Claims"
)
hist(z[true_claim],
  breaks = breaks, col = adjustcolor("#2166ac", 0.5),
  border = "white", add = TRUE
)
abline(v = 1.96, lty = 2)
legend("topright", c("False claims", "True claims"),
  fill = adjustcolor(c("#d6604d", "#2166ac"), 0.5), bty = "n"
)

# Annotations
# 1. The page's controls: what share of claims are true, and how strong the evidence for a true claim typically is.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each claim's evidence: shifted upward if the claim is true, pure noise otherwise.
# 4. Which claims have strong evidence, by the usual threshold.
# 5. Evidence for false and for true claims overlaps. Strong evidence for a false claim and weak evidence for a true one both happen all the time.
