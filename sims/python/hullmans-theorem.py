# Hullman's Theorem: experiments measure a proxy, not what we care about.
import numpy as np
import matplotlib.pyplot as plt

rho = 0.5    # correlation of the proxy with the intended construct
noise = 0.3  # experimental noise
rng = np.random.default_rng(94)

charts = ["Bar", "Dot", "Line", "Pie", "Heatmap", "Stacked bar", "Area",
          "Slope"]
target = rng.normal(size=8)                               # what we care about
proxy = rho * target + np.sqrt(1 - rho ** 2) * rng.normal(size=8)
measured = proxy + rng.normal(0, noise, 8)


def ranks(v):
    return np.argsort(np.argsort(-v)) + 1


rank_measured, rank_target = ranks(measured), ranks(target)
rho_rank = np.corrcoef(rank_measured, rank_target)[0, 1]
print(f"Rank correlation between the experiment's ranking and the ranking "
      f"on the intended construct: {rho_rank:.2f}")

for name, a, b in zip(charts, rank_measured, rank_target):
    plt.plot([1, 2], [a, b], linewidth=2,
             color="#d6604d" if abs(a - b) > 2 else "0.6")
    plt.text(0.95, a, name, ha="right", va="center", fontsize=8)
plt.xticks([1, 2], ["Experiment", "Intended construct"])
plt.xlim(0.4, 2.2)
plt.ylim(8.5, 0.5)
plt.ylabel("Rank")
plt.show()
