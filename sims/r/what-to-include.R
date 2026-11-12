# What to include: print only the digits that survive replication.
se <- 0.3 # standard error of the estimate # <1>
set.seed(108) # <2>

est <- 3.141593 + rnorm(15, 0, se) # 15 replications of the estimate # <3>
print(formatC(est, format = "f", digits = 6, width = 10), quote = FALSE)
dec <- max(0, -floor(log10(se))) # decimals worth reporting # <4>
cat("A sensible report: ", formatC(est[1], format = "f", digits = dec),
  " (", formatC(se, format = "f", digits = dec), ")\n",
  sep = ""
)

# Annotations
# 1. The page's control: the estimate's standard error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Fifteen replications of the estimate, printed to six decimals. Only the first digit or two survive from one replication to the next.
# 4. The number of decimals worth reporting, set by the standard error.
