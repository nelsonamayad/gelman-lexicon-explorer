# Bayesians are frequentists: coverage averaged over the prior.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

se = 1  # data standard error
rng = np.random.default_rng(24)


def covers(theta, y):
    """Prior N(0, 1): does the 90% posterior interval contain theta?"""
    w1 = 1 / se ** 2
    m, s = w1 * y / (1 + w1), np.sqrt(1 / (1 + w1))
    return np.abs(m - theta) < 1.645 * s


grid = np.round(np.arange(-3, 3.01, 0.2), 1)
cov_fixed = np.array([covers(th, rng.normal(th, se, 800)).mean()
                      for th in grid])
theta = rng.normal(size=5000)  # theta drawn from the prior
averaged = covers(theta, rng.normal(theta, se)).mean()

print(f"Coverage at theta = 0: {100 * cov_fixed[grid == 0][0]:.0f}%; "
      f"at theta = 3: {100 * cov_fixed[-1]:.0f}%")
print(f"Averaged over the prior: {100 * averaged:.1f}%")

prior = np.array([NormalDist().pdf(t) for t in grid])
plt.fill_between(grid, prior, color="#2166ac", alpha=0.12)
plt.plot(grid, cov_fixed, color="#2166ac", linewidth=2)
plt.axhline(0.9, color="#d6604d", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("True value of theta")
plt.ylabel("Coverage of the 90% interval")
plt.show()
