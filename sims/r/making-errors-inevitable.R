# Making errors is inevitable; learning from them is not.
detect <- 0.5 # probability an error is detected # <1>
report <- 0.2 # probability a detected error is reported openly
set.seed(136) # <2>

run <- function(q) { # error rate over 30 years, 100 analyses a year # <3>
  rate <- 0.2
  path <- rate
  for (y in 1:30) {
    lessons <- sum(runif(100) < rate & runif(100) < detect & # <4>
      runif(100) < q)
    rate <- max(0.01, rate * 0.97^lessons) # each shared lesson helps # <5>
    path <- c(path, rate)
  }
  path
}
paths <- cbind(yours = run(report), all_reported = run(1), hidden = run(0))
cat("Error rate after 30 years (%):\n")
print(round(100 * paths[31, ], 1))

matplot(0:30, paths, # <6>
  type = "l", lty = 1, lwd = 2,
  col = c("#2166ac", "#1a9850", "#d6604d"), ylim = c(0, 0.22),
  xlab = "Year", ylab = "Share of analyses with an error"
)
legend("topright", c(
  "Your setting", "Every detected error reported",
  "Errors hidden"
),
col = c("#2166ac", "#1a9850", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: the chance an error is detected, and the chance a detected error is reported openly.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Thirty years of 100 analyses, under a given probability of open reporting.
# 4. A lesson is learned only when an error happens, is detected and is shared.
# 5. Each shared lesson lowers the field's error rate a little.
# 6. The error rate over time under your setting, with full reporting, and with errors hidden. Errors happen in all three; learning happens in two.
