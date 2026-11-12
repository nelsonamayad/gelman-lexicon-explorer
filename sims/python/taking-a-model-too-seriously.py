# Taking a Model Too Seriously: a straight line, extrapolated far away.
import numpy as np
import matplotlib.pyplot as plt

curve = 0.12  # curvature in the truth
x_far = 15    # extrapolate to this x
rng = np.random.default_rng(26)


def truth(v):
    return 1 + 0.8 * v - curve * v ** 2


x = rng.uniform(0, 5, 60)
y = truth(x) + rng.normal(0, 0.6, 60)
b, a = np.polyfit(x, y, 1)
resid = y - (a + b * x)
sigma = np.sqrt(resid @ resid / 58)
se_far = sigma * np.sqrt(1 / 60 + (x_far - x.mean()) ** 2
                         / np.sum((x - x.mean()) ** 2))
print(f"The line predicts y({x_far}) = {a + b * x_far:.1f} +/- "
      f"{1.96 * se_far:.1f}; the truth is {truth(x_far):.1f}")

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
xs = np.linspace(0, x_far, 100)
ax[0].scatter(x, y, s=10, color="black")
ax[0].plot(xs, a + b * xs, color="#2166ac", linewidth=2)
ax[0].plot(xs, truth(xs), "--", color="#d6604d", linewidth=2)
ax[1].scatter(x, resid, s=10, color="black")
ax[1].axhline(0, color="black", linestyle="--")
ax[1].set_ylabel("Residual")
plt.show()
