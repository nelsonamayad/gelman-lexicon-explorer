# The paradox of storytelling: the best stories are often the errors.
q <- 0.01 # share of cases where the theory fails # <1>
err_rate <- 0.005 # share of reports with gross errors
set.seed(154) # <2>

N <- 10000
real <- runif(N) < q # the theory fails for this case
truth <- ifelse(real, 3, 0) # deviation, in sd units
gross <- runif(N) < err_rate # a detail that won't stand up
report <- truth + rnorm(N) + ifelse(gross, rnorm(N, 0, 4), 0) # <3>

avg <- sample(report, 200, replace = TRUE) # a random sample of cases # <4>
top <- order(-abs(report))[1:30] # the 30 most striking stories # <5>
recheck <- truth[top] + rnorm(30) # measure again, no gross error # <6>
cat("Random sample: average deviation ", round(mean(avg), 2), " (se ",
  round(sd(avg) / sqrt(200), 2), ")\nOf the 30 most striking stories, ",
  sum(real[top]), " are real anomalies and ", sum(abs(recheck) > 2),
  " hold up when rechecked\n",
  sep = ""
)

plot(1:30, abs(report[top]), # <7>
  pch = 19,
  col = ifelse(real[top], "#2166ac", "#d6604d"),
  xlab = "Rank among the most striking stories",
  ylab = "Reported deviation (sd units)"
)
legend("topright", c("Real anomaly", "Not a real anomaly"),
  pch = 19,
  col = c("#2166ac", "#d6604d"), bty = "n"
)

# Annotations
# 1. The page's controls: the share of cases where the theory really fails, and the share of reports with gross errors.
# 2. Fixes the random numbers so the run is reproducible.
# 3. What gets reported: the truth plus ordinary noise, plus a gross error now and then.
# 4. The statistician's route: a representative sample, averaged. On average the theory looks fine.
# 5. The storyteller's route: the 30 most striking cases, which are the anomalies and the errors together.
# 6. Immutability: check the details by measuring again. Real anomalies survive; errors don't.
# 7. The most striking stories, real anomalies in blue. The anomalies show where the theory fails, which the average cannot, once the errors are weeded out.
