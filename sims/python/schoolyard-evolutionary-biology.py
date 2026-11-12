# Schoolyard Evolutionary Biology: a group difference amid individual
# variation.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

d = 0.3  # average group difference (Cohen's d)
rng = np.random.default_rng(107)

a, b = rng.normal(0, 1, 3000), rng.normal(d, 1, 3000)
Phi = NormalDist().cdf
print(f"Overlap of the two distributions: {100 * 2 * Phi(-d / 2):.0f}%")
print(f"A random B exceeds a random A {100 * Phi(d / np.sqrt(2)):.0f}% of "
      f"the time (simulated: "
      f"{100 * np.mean(rng.permutation(b) > a):.0f}%)")
print(f"Variance explained by group: {100 * d ** 2 / (d ** 2 + 4):.1f}%")

bins = np.arange(-5, 6.01, 0.2)
plt.hist(a, bins=bins, color="#2166ac", alpha=0.5, label="Group A")
plt.hist(b, bins=bins, color="#d6604d", alpha=0.5, label="Group B")
plt.xlabel("Trait")
plt.ylabel("People")
plt.legend()
plt.show()
