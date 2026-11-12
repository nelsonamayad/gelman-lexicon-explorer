# Gresham's Law of bad science: bad papers crowd out good ones.
bad_share <- 0.3 # share of incoming papers that are bad # <1>
bad_time <- 4 # hours spent on each bad paper (vs 1 for a good one)
# Deterministic: no random numbers.

budget <- 20
incoming <- 20 # hours a week; papers a week
good_read <- function(share) { # <2>
  n_good <- incoming * (1 - share)
  n_bad <- incoming * share
  frac_read <- min(1, budget / (n_good + n_bad * bad_time)) # random order # <3>
  n_good * frac_read
}
cat(
  "Good papers read per week:", round(good_read(bad_share), 1), "of",
  incoming * (1 - bad_share), "coming in\n"
)

shares <- seq(0, 0.8, by = 0.05)
plot(shares, sapply(shares, good_read), # <4>
  type = "b", pch = 19,
  col = "#2166ac", xlab = "Share of incoming papers that are bad",
  ylab = "Good papers read per week"
)

# Annotations
# 1. The page's controls: what share of incoming papers are bad, and how many hours a bad paper eats compared with a good one. There is no seed: the model is deterministic.
# 2. Good papers read per week, given a fixed reading budget and papers taken in random order.
# 3. The budget runs out sooner the more bad papers there are, because each costs more time.
# 4. Good papers read as the share of bad ones rises. Bad papers crowd out good ones even when nobody prefers them.
