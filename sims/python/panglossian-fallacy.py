# Panglossian Fallacy: assuming the odds were right because they're odds.
import numpy as np
import matplotlib.pyplot as plt

k = 4             # how much long shots are underpriced
n_events = 20000  # priced events in the track record
rng = np.random.default_rng(116)

# Implied probabilities from 1 in 5,000 to 1 in 2, even on the log scale
implied = np.exp(np.log(1 / 5000) + rng.uniform(size=n_events)
                 * np.log(5000 / 2))
true_odds = k * implied / (1 - implied)  # true odds k times implied odds
won = rng.uniform(size=n_events) < true_odds / (1 + true_odds)

edges = [1 / 5000, 1 / 1000, 1 / 200, 1 / 50, 1 / 10, 1 / 2]
bin_ = np.digitize(implied, edges) - 1
mean_implied = [implied[bin_ == b].mean() for b in range(5)]
observed = [won[bin_ == b].mean() for b in range(5)]
for a, o in zip(mean_implied, observed):
    print(f"implied {a:.2g} -> observed {o:.2g}")

long = bin_ <= 2                        # long shots: worse than 1 in 50
ratio = won[long].sum() / implied[long].sum()
se = np.sqrt(max(won[long].sum(), 1)) / implied[long].sum()
print(f"Long shots won {ratio:.1f} times as often as the odds implied")
print("The odds were wrong." if ratio - 2 * se > 1
      else "Consistent with calibrated odds.")

plt.loglog(mean_implied, np.maximum(observed, 1e-5), "o", color="#d6604d")
plt.plot([2e-4, 0.5], [2e-4, 0.5], "k--")
plt.xlabel("Implied probability")
plt.ylabel("Observed win rate")
plt.show()
