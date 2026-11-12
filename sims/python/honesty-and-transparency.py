# Honesty and transparency are not enough: noisy studies stay uninformative.
import numpy as np
import matplotlib.pyplot as plt

meas_noise = 3  # measurement noise (sd)
n = 60          # participants per arm
rng = np.random.default_rng(77)

theta = 0.2                      # small true effect
se = meas_noise * np.sqrt(2 / n)
est = rng.normal(theta, se, 200)  # 200 honest, preregistered studies
lo, hi = est - 1.96 * se, est + 1.96 * se
# Informative: rules out negligible effects (< 0.05), or meaningful ones
informative = (lo > 0.05) | (hi < 0.05)

print(f"Each interval is {2 * 1.96 * se:.2f} wide; true effect 0.2")
print(f"Studies that can tell a meaningful effect from a negligible one: "
      f"{100 * informative.mean():.0f}%")

k = np.arange(50)
plt.vlines(k, lo[:50], hi[:50], color="#2166ac")
plt.plot(k, est[:50], "o", color="black", markersize=3)
plt.axhline(theta, color="#d6604d", linewidth=2)
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Study")
plt.ylabel("Estimate with 95% interval")
plt.show()
