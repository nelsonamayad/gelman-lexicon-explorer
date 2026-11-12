# Second-Order Availability Bias: your own circle is not the country.
import numpy as np
import matplotlib.pyplot as plt

my_state = 38  # your state (1 = poorest, 40 = richest)
rng = np.random.default_rng(16)

# 40 states, 400 voters each. Income matters a lot in poor states and
# hardly at all in rich ones.
state = np.repeat(np.arange(1, 41), 400)
wealth = (state - 1 - 19.5) / 20                  # -1 .. 1
slope = 0.9 - 0.85 * (wealth + 1) / 2
inc = rng.normal(wealth, 1)
vote = rng.binomial(1, 1 / (1 + np.exp(-(-0.4 * wealth + slope * inc))))

mine = np.flatnonzero(state == my_state)[:200]   # your acquaintances
print(f"Slope of vote on income among your acquaintances: "
      f"{np.polyfit(inc[mine], vote[mine], 1)[0]:.3f}")
print(f"In the whole country: {np.polyfit(inc, vote, 1)[0]:.3f}")

edges = np.arange(-3, 3.01, 0.75)
mids = edges[:-1] + 0.375
for idx, c, label in [(slice(None), "#2166ac", "Whole country"),
                      (mine, "#d6604d", "Your acquaintances")]:
    b = np.digitize(inc[idx], edges) - 1
    p = [vote[idx][b == k].mean() if np.sum(b == k) > 5 else np.nan
         for k in range(8)]
    plt.plot(mids, p, "o-", color=c, label=label)
plt.ylim(0, 1)
plt.xlabel("Income")
plt.ylabel("Share voting for the party")
plt.legend()
plt.show()
