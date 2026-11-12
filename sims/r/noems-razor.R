# Noem's Razor: when a pattern of convenient errors stops looking innocent.
prior <- 0.05 # prior probability of malice (charitable) # <1>
truth <- "Motivated distortion" # or "Honest mistakes"
set.seed(153) # <2>

# Each error either favors the person's side or not. Honest mistakes favor
# them half the time; motivated distortion 90% of the time.
p_fav <- if (truth == "Honest mistakes") 0.5 else 0.9 # <3>
fav <- runif(15) < p_fav
log_odds <- qlogis(prior) + # <4>
  cumsum(ifelse(fav, log(0.9 / 0.5), log(0.1 / 0.5)))
belief <- c(prior, plogis(log_odds))
cat(sum(fav), " of 15 errors favored their side; belief in malice ",
  "rises from ", round(100 * prior), "% to ", round(100 * belief[16]),
  "%\n",
  sep = ""
)

plot(0:15, belief, # <5>
  type = "b", pch = c(1, ifelse(fav, 19, 1)),
  col = "#d6604d", ylim = c(0, 1), xlab = "Errors observed",
  ylab = "Probability of malice"
)
abline(h = 0.5, lty = 2)

# Annotations
# 1. The page's controls: a charitable prior probability of malice, and what is really going on.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Honest mistakes favor the person's side half the time; motivated distortion, nine times in ten.
# 4. Bayesian updating after each error, with a likelihood ratio of 0.9 to 0.5 for a convenient error and 0.1 to 0.5 for an inconvenient one.
# 5. The posterior probability of malice after each error (filled dots are errors that favored them). One-sided errors overwhelm charity.
