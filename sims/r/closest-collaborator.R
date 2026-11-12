# Your closest collaborator: you, six months ago.
doc_frac <- 0.3 # fraction of decisions documented # <1>
tau <- 4 # memory half-life (months)
set.seed(104) # <2>

D <- 40
lambda <- log(2) / tau
months <- 0:24
expected <- D * (doc_frac + (1 - doc_frac) * exp(-lambda * months)) # <3>
recovered <- sapply(months, function(t) { # <4>
  sum(seq_len(D) <= doc_frac * D | runif(D) < exp(-lambda * t))
})

cat(
  "Decisions you can reconstruct after 6 months: about",
  round(expected[months == 6]), "of 40\n"
)
cat("After two years: about", round(expected[months == 24]), "of 40\n")

plot(months, recovered, # <5>
  pch = 19, col = "#2166ac", ylim = c(0, D),
  xlab = "Months later", ylab = "Decisions you can reconstruct"
)
lines(months, expected, col = "#2166ac")
abline(h = doc_frac * D, col = "#d6604d", lty = 2) # documentation's floor

# Annotations
# 1. The page's controls: the fraction of decisions you wrote down, and how fast memory of the rest fades (its half-life in months).
# 2. Fixes the random numbers so the run is reproducible.
# 3. The expected number of the 40 decisions you can reconstruct: the documented ones, plus the undocumented ones you still remember.
# 4. One simulated you at each delay: documented decisions survive, undocumented ones are remembered with decaying probability.
# 5. Reconstructable decisions over two years. The dashed line is the floor set by documentation.
