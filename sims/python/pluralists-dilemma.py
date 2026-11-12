# The Pluralist's Dilemma: which method is best depends on your problems.
import numpy as np
import matplotlib.pyplot as plt

my_ratio = 0.7  # typical signal/noise in my problems
J = 8           # groups per problem
rng = np.random.default_rng(46)

ratios = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5])
sep, pool = [], []
for ratio in ratios:
    th = rng.normal(0, ratio, (300, J))     # 300 problems
    y = rng.normal(th, 1)
    m = y.mean(axis=1, keepdims=True)
    t2 = np.maximum(0, np.mean((y - m) ** 2, axis=1, keepdims=True) - 1)
    B = t2 / (t2 + 1)
    sep.append(np.sqrt(np.mean((y - th) ** 2)))
    pool.append(np.sqrt(np.mean((m + B * (y - m) - th) ** 2)))
near = np.argmin(np.abs(np.log(ratios / my_ratio)))
print(f"At signal/noise {ratios[near]}: separate estimates RMSE "
      f"{sep[near]:.2f}, partial pooling {pool[near]:.2f}")

plt.semilogx(ratios, sep, "o-", color="#d6604d", label="Separate estimates")
plt.semilogx(ratios, pool, "o-", color="#2166ac", label="Partial pooling")
plt.axvline(my_ratio, color="black", linestyle="--")
plt.xlabel("Signal/noise ratio")
plt.ylabel("Root mean squared error")
plt.legend()
plt.show()
