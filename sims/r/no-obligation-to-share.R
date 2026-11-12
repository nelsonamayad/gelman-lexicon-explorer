# You have no obligation to share your data and code (but it is a signal).
e <- 0.25 # base rate of serious errors # <1>
s_right <- 0.7 # probability of sharing if the analysis is sound
s_wrong <- 0.35 # probability of sharing if the analysis is flawed
set.seed(150) # <2>

wrong <- runif(5000) < e
shared <- runif(5000) < ifelse(wrong, s_wrong, s_right) # <3>
caught <- shared & wrong & runif(5000) < 0.7 # checkers find 70% of errors # <4>
status <- ifelse(!shared, "Not shared",
  ifelse(caught, "Shared: error found", "Shared: checks out")
)

correct <- tapply(!wrong, status, mean) # <5>
print(round(100 * correct)) # % of analyses that are correct, by status

barplot( # <6>
  100 * correct[c(
    "Shared: checks out", "Not shared",
    "Shared: error found"
  )],
  col = c("#2166ac", "grey70", "#d6604d"),
  ylab = "Analyses that are correct (%)", ylim = c(0, 100)
)

# Annotations
# 1. The page's controls: the base rate of serious errors, and the probability of sharing when the analysis is sound and when it is flawed.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Authors of flawed analyses share less often. That is what makes not sharing a signal.
# 4. Shared analyses get checked, and most errors are found.
# 5. By Bayes' rule, the share of correct analyses in each group.
# 6. Not shared sits between checks-out and error-found: no obligation, but readers may draw their conclusions.
