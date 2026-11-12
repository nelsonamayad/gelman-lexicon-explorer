# The Ramanujan Principle: partition numbers and the Hardy-Ramanujan formula.
n_max <- 100 # largest n # <1>
# Deterministic: no random numbers. Values up to n = 200 (about 4e12) fit
# exactly in R's double-precision numbers.

# Euler's pentagonal-number recurrence for p(n), the number of partitions
p <- numeric(201) # <2>
p[1] <- 1 # p[n + 1] holds p(n)
for (n in 1:200) {
  k <- 1
  s <- 0
  while (k * (3 * k - 1) / 2 <= n) { # <3>
    sgn <- if (k %% 2) 1 else -1
    g1 <- k * (3 * k - 1) / 2
    g2 <- k * (3 * k + 1) / 2
    s <- s + sgn * p[n - g1 + 1]
    if (g2 <= n) s <- s + sgn * p[n - g2 + 1]
    k <- k + 1
  }
  p[n + 1] <- s
}
asymptotic <- function(n) exp(pi * sqrt(2 * n / 3)) / (4 * n * sqrt(3)) # <4>

print(
  data.frame(
    n = seq(10, n_max, 10),
    p = format(p[seq(10, n_max, 10) + 1], big.mark = ",")
  ),
  row.names = FALSE
)
cat("Formula / exact at n = ", n_max, ": ",
  round(asymptotic(n_max) / p[n_max + 1], 3), "\n",
  sep = ""
)

plot(1:n_max, log10(p[2:(n_max + 1)]), # <5>
  type = "l", lwd = 2,
  col = "#2166ac", xlab = "n", ylab = "log10 p(n)"
)
lines(1:n_max, log10(asymptotic(1:n_max)),
  col = "#d6604d", lwd = 2,
  lty = 2
)

# Annotations
# 1. The page's control: the largest n to show. There is no seed: the computation is exact.
# 2. The exact partition numbers p(n), computed by recurrence.
# 3. Euler's pentagonal-number recurrence, which gives each p(n) from earlier ones.
# 4. The Hardy-Ramanujan formula: a closed form that is only asymptotically right, and already close.
# 5. Exact values and the formula on a log scale. Ramanujan's principle: a formula can be approximately right and still tell you the truth about the problem.
