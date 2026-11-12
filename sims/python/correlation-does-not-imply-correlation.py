# Correlation does not even imply correlation.
import numpy as np
import matplotlib.pyplot as plt

n = 25            # sample size
selection = False  # only observe units with x + y > 1 (Berkson)
k = 20            # number of variable pairs examined
rng = np.random.default_rng(70)


def draw():
    """x and y are independent in the population."""
    x, y = rng.normal(size=20 * n), rng.normal(size=20 * n)
    keep = np.flatnonzero(x + y > 1)[:n] if selection else np.arange(n)
    return x[keep], y[keep]


samples = [draw() for _ in range(k)]
r = np.array([np.corrcoef(x, y)[0, 1] for x, y in samples])
best = np.argmax(np.abs(r))
print(f"True correlation: 0. Most striking of {k} sample correlations: "
      f"{r[best]:.2f}")

x, y = samples[best]
slope, intercept = np.polyfit(x, y, 1)
xs = np.linspace(x.min(), x.max(), 2)
plt.scatter(x, y, color="#2166ac")
plt.plot(xs, intercept + slope * xs, color="#d6604d", linewidth=2)
plt.title(f"r = {r[best]:.2f}")
plt.show()
