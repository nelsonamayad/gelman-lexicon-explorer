# Seeds of its own destruction: a histogram that shows its own noise.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

bins = 40  # number of bins between -4 and 4
n = 1000   # sample size
rng = np.random.default_rng(112)

x = rng.normal(size=n)
per_bin = n * (8 / bins) * NormalDist().pdf(0)  # count in a central bin
print(f"With {bins} bins, central bars hold about {per_bin:.0f} points "
      f"each,\nso their heights wobble by about +/-{np.sqrt(per_bin):.0f} "
      f"({100 / np.sqrt(per_bin):.0f}%)")

fig, axes = plt.subplots(2, 2, figsize=(8, 6))
choices = [("Too coarse", 8), ("Default-ish", 20), ("Your choice", bins),
           ("Too fine", 160)]
for ax, (label, k) in zip(axes.flat, choices):
    ax.hist(x, bins=np.linspace(-4, 4, k + 1), color="#2166ac")
    ax.set_title(f"{label}: {k} bins")
plt.tight_layout()
plt.show()
