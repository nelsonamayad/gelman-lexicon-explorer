# The Fallacy of the One-Sided Bet: weekly lottery tickets over the years.
years <- 20 # years of weekly play # <1>
jackpot_odds <- 6 # jackpot odds: 1 in 10^jackpot_odds
set.seed(30) # <2>

weeks <- years * 52
p_jack <- 10^-jackpot_odds
# Each ticket costs $2: jackpot $1,000,000, $50 with 1%, $4 with 9%
u <- matrix(runif(1000 * weeks), 1000)
prize <- ifelse(u < p_jack, 1e6, ifelse(u < 0.01, 50, ifelse(u < 0.1, 4, 0))) # <3>
net <- rowSums(prize) - 2 * weeks # net winnings of 1000 players # <4>
ev <- -2 + 1e6 * p_jack + 50 * (0.01 - p_jack) + 4 * 0.09 # <5>

cat(sum(net > 0), " of 1000 players come out ahead after ", years,
  " years\nExpected net per ticket: $", round(ev, 2), "\n",
  sep = ""
)

hist(pmax(net, -5000), # <6>
  breaks = 40, col = "#d6604d", border = "white",
  main = "", xlab = "Net winnings ($)", ylab = "Players"
)
abline(v = 0, lty = 2)

# Annotations
# 1. The page's controls: years of weekly play and the jackpot odds.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each ticket's prize: a jackpot, a small prize, a token prize, or nothing.
# 4. Each player's net winnings after all those weeks, with the $2 tickets counted. The one-sided view forgets the tickets.
# 5. The expected value of a ticket, which is negative.
# 6. Net winnings across 1,000 players. The thought *someone wins big* ignores the other side of the bet.
