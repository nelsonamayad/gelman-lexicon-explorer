# The house: regression with non-normal errors still stands.
err_dist <- "Skewed" # "Normal", "Skewed", "Heavy-tailed" or "Bimodal" # <1>
n <- 50 # sample size
set.seed(138) # <2>

err <- function(m) { # <3>
  switch(err_dist,
    Normal = rnorm(m),
    Skewed = rexp(m) - 1,
    "Heavy-tailed" = rt(m, 3) / sqrt(3),
    Bimodal = sample(c(-1, 1), m, replace = TRUE) + rnorm(m, 0, 0.3)
  )
}
reps <- t(replicate(1500, {
  x <- rnorm(n)
  y <- 1 + 0.5 * x + err(n)
  b <- cov(x, y) / var(x)
  a <- mean(y) - b * mean(x)
  se <- sqrt(sum((y - a - b * x)^2) / (n - 2) / sum((x - mean(x))^2)) # <4>
  c(b = b, cover = abs(b - 0.5) < 1.96 * se)
}))
cat("With ", tolower(err_dist), " errors and n = ", n, ", the 95% ",
  "interval covers the true slope ", round(100 * mean(reps[, "cover"]), 1),
  "% of the time\nAverage slope estimate: ",
  round(mean(reps[, "b"]), 3), " (truth 0.5)\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <5>
hist(err(800),
  breaks = 40, col = "grey70", border = "white",
  main = "The errors", xlab = ""
)
hist(reps[, "b"],
  breaks = 40, col = "#2166ac", border = "white",
  main = "Slope estimates", xlab = ""
)
abline(v = 0.5, lwd = 2)

# Annotations
# 1. The page's controls: the shape of the error distribution and the sample size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Errors that are anything but normal: the foundation the textbook assumes is missing.
# 4. The usual least-squares standard error, derived under normality.
# 5. The errors and the slope estimates. The house stands: the estimates center on the truth and the intervals still cover about 95% of the time.
