# Salad Tongs: the p-value from a replication of a study with given power.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

power = 0.5  # power of the study
rng = np.random.default_rng(50)

N = NormalDist()
delta = N.inv_cdf(0.975) + N.inv_cdf(power)  # true effect, in se units
z = rng.normal(delta, 1, 200)               # 200 replications
p = np.array([2 * (1 - N.cdf(abs(v))) for v in z])
print(f"Share significant: {100 * np.mean(p < 0.05):.0f}%")
print(f"Middle 80% of p-values: {np.quantile(p, 0.1):.2g} to "
      f"{np.quantile(p, 0.9):.2g}")

plt.scatter(np.arange(1, 201), p, s=10,
            c=np.where(p < 0.05, "#2166ac", "#d6604d"))
plt.yscale("log")
plt.axhline(0.05, color="black", linestyle="--")
plt.xlabel("Replication")
plt.ylabel("p-value (log scale)")
plt.show()
