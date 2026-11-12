# The Fallacy of the One-Sided Bet: weekly lottery tickets over the years.
import numpy as np
import matplotlib.pyplot as plt

years = 20        # years of weekly play
jackpot_odds = 6  # jackpot odds: 1 in 10^jackpot_odds
rng = np.random.default_rng(30)

weeks, p_jack = years * 52, 10.0 ** -jackpot_odds
# Each ticket costs $2: jackpot $1,000,000, $50 with 1%, $4 with 9%
u = rng.uniform(size=(1000, weeks))
prize = np.select([u < p_jack, u < 0.01, u < 0.1], [1e6, 50, 4], 0)
net = prize.sum(axis=1) - 2 * weeks  # net winnings of 1000 players
ev = -2 + 1e6 * p_jack + 50 * (0.01 - p_jack) + 4 * 0.09

print(f"{np.sum(net > 0)} of 1000 players come out ahead after {years} "
      f"years\nExpected net per ticket: ${ev:.2f}")

plt.hist(np.maximum(net, -5000), bins=40, color="#d6604d")
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("Net winnings ($)")
plt.ylabel("Players")
plt.show()
