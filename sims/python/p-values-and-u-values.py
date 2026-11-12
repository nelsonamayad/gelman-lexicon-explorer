# P-values and U-values: posterior predictive p-values are not uniform.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

stat = "Sample maximum"  # or "Sample mean", "Sample variance"
n = 20                   # observations per dataset
rng = np.random.default_rng(12)

T = {"Sample mean": lambda y: y.mean(axis=-1),
     "Sample maximum": lambda y: y.max(axis=-1),
     "Sample variance": lambda y: y.var(axis=-1)}[stat]
y = rng.normal(0, 1, (1000, n))  # 1000 datasets from the true model
ybar = y.mean(axis=1)
classical = 1 - np.array([NormalDist().cdf(v) for v in ybar * np.sqrt(n)])
th = rng.normal(ybar[:, None], 1 / np.sqrt(n), (1000, 200))  # posterior
yrep = rng.normal(th[:, :, None], 1, (1000, 200, n))  # replicated datasets
ppp = np.mean(T(yrep) >= T(y)[:, None], axis=1)


def extreme(p):
    return 100 * np.mean((p < 0.05) | (p > 0.95))


print("Share of p-values below 0.05 or above 0.95 (uniform: 10%):")
print(f"classical {extreme(classical):.0f}%, posterior predictive "
      f"{extreme(ppp):.0f}%")

fig, ax = plt.subplots(1, 2, sharey=True)
ax[0].hist(classical, bins=20, color="0.7")
ax[0].set_title("Classical p-value")
ax[1].hist(ppp, bins=20, color="#2166ac")
ax[1].set_title("Posterior predictive p-value")
plt.show()
