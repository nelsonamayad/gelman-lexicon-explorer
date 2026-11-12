# Between regularization and discovery: ranking noisy estimates.
import numpy as np
import matplotlib.pyplot as plt

spread_n = 1.2  # variation in sample sizes (log scale)
rng = np.random.default_rng(122)

# 300 groups: most effects tiny, 8% large; sample sizes vary
theta = np.where(rng.uniform(size=300) < 0.08, rng.normal(0, 1.5, 300),
                 rng.normal(0, 0.2, 300))
n = np.round(30 * np.exp(rng.normal(0, spread_n, 300))) + 2
se = 2 / np.sqrt(n)
y = rng.normal(theta, se)
tau2 = max(0.01, np.mean(y ** 2 - se ** 2))
shrunk = tau2 / (tau2 + se ** 2) * y


def top(v):  # the 20 most extreme groups
    return set(np.argsort(-np.abs(v))[:20])


print(f"Of the true top 20, the raw estimates find "
      f"{len(top(y) & top(theta))} and the regularized estimates find "
      f"{len(top(shrunk) & top(theta))}")

raw_top, reg_top = list(top(y)), list(top(shrunk))
plt.scatter(theta, y, s=8, color="0.6")
plt.scatter(theta[raw_top], y[raw_top], s=60, facecolors="none",
            edgecolors="#d6604d", label="Raw top 20")
plt.scatter(theta[reg_top], shrunk[reg_top], color="#2166ac",
            label="Regularized top 20")
plt.xlabel("True effect")
plt.ylabel("Estimate")
plt.legend()
plt.show()
