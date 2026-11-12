# Arrow's Other Theorem (weak form): no result is published more than 5 times.
p <- 0.5 # probability a result is repackaged once more # <1>
set.seed(33) # <2>

pubs <- replicate(500, {
  k <- 1
  while (k < 5 && runif(1) < p) k <- k + 1 # <3>
  k
})
theory <- if (p == 1) 5 else (1 - p^5) / (1 - p) # <4>

cat("500 distinct results produced", sum(pubs), "publications\n")
cat(
  "Redundancy ratio:", round(mean(pubs), 2),
  "(theory:", round(theory, 2), ")\n"
)

barplot(table(factor(pubs, levels = 1:5)), # <5>
  col = "#2166ac",
  xlab = "Publications per result", ylab = "Results"
)

# Annotations
# 1. The page's control: the probability that a result is repackaged once more.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each result is republished with probability p, up to the theorem's cap of five publications.
# 4. The expected number of publications per result under the cap: the geometric series truncated at five terms.
# 5. How many results reached each number of publications.
