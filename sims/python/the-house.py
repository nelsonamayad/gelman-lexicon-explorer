# The house: regression with non-normal errors still stands.
import numpy as np
import matplotlib.pyplot as plt

err_dist = "Skewed"  # "Normal", "Skewed", "Heavy-tailed" or "Bimodal"
n = 50               # sample size
rng = np.random.default_rng(138)


def err(size):
    if err_dist == "Normal":
        return rng.normal(size=size)
    if err_dist == "Skewed":
        return rng.exponential(1, size) - 1
    if err_dist == "Heavy-tailed":
        return rng.standard_t(3, size) / np.sqrt(3)
    return rng.choice([-1, 1], size) + rng.normal(0, 0.3, size)


x = rng.normal(size=(1500, n))
y = 1 + 0.5 * x + err((1500, n))
xc = x - x.mean(axis=1, keepdims=True)
b = np.sum(xc * y, axis=1) / np.sum(xc ** 2, axis=1)
a = y.mean(axis=1) - b * x.mean(axis=1)
resid = y - a[:, None] - b[:, None] * x
se = np.sqrt(np.sum(resid ** 2, axis=1) / (n - 2) / np.sum(xc ** 2, axis=1))
cover = np.abs(b - 0.5) < 1.96 * se
print(f"With {err_dist.lower()} errors and n = {n}, the 95% interval "
      f"covers the true slope {100 * cover.mean():.1f}% of the time")
print(f"Average slope estimate: {b.mean():.3f} (truth 0.5)")

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].hist(err(800), bins=40, color="0.7")
ax[0].set_title("The errors")
ax[1].hist(b, bins=40, color="#2166ac")
ax[1].axvline(0.5, color="black", linewidth=2)
ax[1].set_title("Slope estimates")
plt.show()
