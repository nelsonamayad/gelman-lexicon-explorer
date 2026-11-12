# Eureka bias: refusing to let go of a discovery.
import numpy as np
import matplotlib.pyplot as plt

phi = 0.05  # weight the eureka-biased researcher gives new data
rng = np.random.default_rng(72)

se = 0.3
first = rng.normal(0, se, 20).max()  # the "discovery": best of 20 looks
y = rng.normal(0, se, 20)            # 20 follow-ups; the true effect is zero
w0 = w = 1 / se ** 2
k = np.arange(1, 21)
neutral = (first * w0 + np.cumsum(y) * w) / (w0 + k * w)
eureka = (first * w0 + np.cumsum(y) * w * phi) / (w0 + k * w * phi)

print(f"Discovery: {first:.2f} | belief after 20 follow-ups: neutral "
      f"{neutral[-1]:.2f}, eureka-biased {eureka[-1]:.2f}")

plt.plot(range(21), np.r_[first, neutral], color="#2166ac", linewidth=2,
         label="Neutral updater")
plt.plot(range(21), np.r_[first, eureka], color="#d6604d", linewidth=2,
         label="Eureka-biased")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Follow-up studies")
plt.ylabel("Belief about the effect")
plt.legend()
plt.show()
