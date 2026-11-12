# The Edlin Factor: how much to scale down published estimates.
import numpy as np
import matplotlib.pyplot as plt

tau = 0.2  # spread of true effects
se = 0.25  # standard error of each study
rng = np.random.default_rng(51)

theta = rng.normal(0, tau, 5000)
est = rng.normal(theta, se)
pub = np.abs(est) > 1.96 * se  # only significant results get published
factor = np.sum(theta[pub] * est[pub]) / np.sum(est[pub] ** 2)

print(f"Published: {pub.sum()} of 5000")
print(f"Average magnitude: published estimates "
      f"{np.abs(est[pub]).mean():.2f} | their true effects "
      f"{np.abs(theta[pub]).mean():.2f}")
print(f"Edlin factor: {factor:.2f} "
      f"(theory: {tau ** 2 / (tau ** 2 + se ** 2):.2f})")

xs = np.array([est[pub].min(), est[pub].max()])
plt.scatter(est[pub], theta[pub], s=5, color="#2166ac", alpha=0.4)
plt.plot(xs, xs, "k--")
plt.plot(xs, factor * xs, color="#d6604d", linewidth=2)
plt.xlabel("Published estimate")
plt.ylabel("True effect")
plt.show()
