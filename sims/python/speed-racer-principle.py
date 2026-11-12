# The Speed Racer Principle: an interaction on one scale vanishes on another.
import numpy as np
import matplotlib.pyplot as plt

growth = 0.15  # common growth rate per period
ratio = 2.5    # group A starts this many times higher
rng = np.random.default_rng(53)

t = rng.integers(0, 7, 400)
a = rng.binomial(1, 0.5, 400)
y = 10 * np.where(a == 1, ratio, 1) * np.exp(growth * t
                                             + rng.normal(0, 0.1, 400))
X = np.column_stack([np.ones(400), t, a, t * a])


def interaction(v):  # coefficient and se of time x group
    beta, *_ = np.linalg.lstsq(X, v, rcond=None)
    s2 = np.sum((v - X @ beta) ** 2) / (400 - 4)
    return beta[3], np.sqrt(s2 * np.linalg.inv(X.T @ X)[3, 3])


print("Interaction (time x group), estimate and se:")
print("raw scale {:.2f} ({:.2f}), ".format(*interaction(y))
      + "log scale {:.3f} ({:.3f})".format(*interaction(np.log(y))))

cols = np.where(a == 1, "#d6604d", "#2166ac")
jit = t + rng.uniform(-0.2, 0.2, 400)
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].scatter(jit, y, s=6, c=cols)
ax[0].set_title("Raw scale")
ax[1].scatter(jit, np.log(y), s=6, c=cols)
ax[1].set_title("Log scale")
plt.show()
