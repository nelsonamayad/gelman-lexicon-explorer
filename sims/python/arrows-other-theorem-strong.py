# Arrow's Other Theorem (strong form): one result counted m times.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

m = 5  # times each result is published
K = 6  # independent studies, all of a true effect of zero
rng = np.random.default_rng(34)
N = NormalDist()

fpr = []
for mm in range(1, 6):
    pooled = rng.normal(size=(2000, K)).mean(axis=1)  # 2,000 analyses
    se = 1 / np.sqrt(K * mm)     # naive standard error, counting copies
    p = np.array([2 * N.cdf(-abs(v) / se) for v in pooled])
    fpr.append((p < 0.05).mean())
print(f"False-positive rate with each result published {m} times: "
      f"{100 * fpr[m - 1]:.1f}%")

plt.bar(range(1, 6), fpr,
        color=["#d6604d" if i == m else "0.7" for i in range(1, 6)])
plt.axhline(0.05, color="black", linestyle="--")
plt.ylim(0, 0.6)
plt.xlabel("Publications per result (m)")
plt.ylabel("False-positive rate of the meta-analysis")
plt.show()
