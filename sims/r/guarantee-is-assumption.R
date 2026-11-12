# When researchers say "guarantee", they mean an assumption.
skew <- 1.2 # skewness: sigma of the log-normal distribution # <1>
n <- 15 # sample size
set.seed(115) # <2>

true_mean <- exp(skew^2 / 2)
tcrit <- qt(0.975, n - 1)
miss <- replicate(3000, {
  y <- rlnorm(n, 0, skew) # <3>
  half <- tcrit * sd(y) / sqrt(n) # <4>
  if (mean(y) + half < true_mean) {
    "too low"
  } else if (mean(y) - half > true_mean) "too high" else "covers"
})

cat("Coverage of the 'guaranteed' 95% t-interval: ",
  round(100 * mean(miss == "covers"), 1), "%\n",
  sep = ""
)
cat("Intervals entirely below the true mean: ",
  round(100 * mean(miss == "too low"), 1), "%\n",
  sep = ""
)

barplot(table(factor(miss, c("too low", "covers", "too high"))) / 3000, # <5>
  col = c("#d6604d", "#2166ac", "#b8860b"),
  ylab = "Share of intervals"
)
abline(h = 0.95, lty = 2)

# Annotations
# 1. The page's controls: how skewed the data are and the sample size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Log-normal data: incomes, response times, anything with a long right tail.
# 4. The textbook t-interval, whose 95% guarantee assumes normal data.
# 5. How often the interval covers, falls entirely below, or entirely above the true mean. The dashed line is the guaranteed 95%.
