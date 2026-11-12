# Scaffolding: complete pooling, no pooling, then partial pooling.
import numpy as np
import matplotlib.pyplot as plt

tau = 0.3  # true between-group sd
rng = np.random.default_rng(21)

n = np.array([2, 3, 5, 8, 12, 20, 35, 60, 100, 200])  # group sizes
theta = rng.normal(0, tau, 10)
ybar = np.array([rng.normal(t, 1, k).mean() for t, k in zip(theta, n)])
v = 1 / n
grand = np.sum(ybar * n) / n.sum()                # 1. complete pooling
mu = np.sum(ybar / v) / np.sum(1 / v)
tau2 = max(0.002, np.mean((ybar - mu) ** 2) - v.mean())
partial = mu + tau2 / (tau2 + v) * (ybar - mu)    # 3. partial pooling
for k, y, p in zip(n, ybar, partial):
    print(f"n = {k:3d}: complete {grand:.2f}, none {y:.2f}, "
          f"partial {p:.2f}")

x = np.arange(10)
plt.plot(x, np.full(10, grand), "o-", color="0.5", label="Complete pooling")
plt.plot(x, ybar, "o-", color="#d6604d", label="No pooling")
plt.plot(x, partial, "o-", color="#2166ac", label="Partial pooling")
plt.xticks(x, n)
plt.xlabel("Group (size)")
plt.ylabel("Estimate")
plt.legend()
plt.show()
