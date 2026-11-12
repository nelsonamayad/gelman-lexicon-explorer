# The (Lance) Armstrong Principle: promise more than you can deliver.
import numpy as np
import matplotlib.pyplot as plt

promise = 0.5  # promised effect T
kappa = 3      # pressure to deliver
rng = np.random.default_rng(64)

honest = rng.normal(0.2, 0.25, 2000)
p_cheat = np.where(honest < promise, 1 - np.exp(-kappa * (promise - honest)),
                   0)
cheat = rng.uniform(size=2000) < p_cheat
reported = np.where(cheat, promise + np.abs(rng.normal(0, 0.05, 2000)),
                    honest)

print(f"Share who cheat: {100 * cheat.mean():.0f}%")
print(f"Average reported effect: {reported.mean():.2f} "
      "(honest average 0.20)")

bins = np.linspace(reported.min() - 0.05, reported.max() + 0.05, 60)
plt.hist([reported[~cheat], reported[cheat]], bins=bins, stacked=True,
         color=["#2166ac", "#d6604d"], label=["Honest", "Cheated"])
plt.axvline(promise, color="black", linestyle="--")
plt.xlabel("Reported effect")
plt.ylabel("Researchers")
plt.legend()
plt.show()
