# Default, the greatest trick it ever pulled: silently dropping missing data.
miss_strength <- 1.5 # how strongly low income predicts skipping the question # <1>
set.seed(38) # <2>

educ <- rnorm(2000)
income <- 50 + 12 * educ + rnorm(2000, 0, 10)
missing <- runif(2000) < plogis(-1.5 - miss_strength * (income - 50) / 12) # <3>

fit <- lm(income ~ educ, subset = !missing) # impute from education # <4>
imputed <- ifelse(missing, predict(fit, data.frame(educ = educ)), income)

cat("Skipped the question: ", round(100 * mean(missing)), "%\n", sep = "")
cat(
  "Truth:", round(mean(income), 1), "| drop missing rows (the default):",
  round(mean(income[!missing]), 1), "| impute from education:", # <5>
  round(mean(imputed), 1), "\n"
)

est <- c(
  Truth = mean(income), "Drop missing rows" = mean(income[!missing]),
  "Impute" = mean(imputed)
)
dotchart(est, # <6>
  pch = 19, col = c("black", "#d6604d", "#2166ac"),
  xlab = "Estimated average income"
)

# Annotations
# 1. The page's control: how strongly a low income predicts skipping the income question.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Who skips the question: the poorer, the likelier. Missingness depends on the outcome itself.
# 4. An imputation model: predict the missing incomes from education, which everyone answered.
# 5. Three answers: the truth, the software's silent default of dropping incomplete rows, and the imputed average.
# 6. The default's answer is biased upward, and nothing in the output says a choice was made.
