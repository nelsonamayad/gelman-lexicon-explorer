# In high-dimensional space, no one can hear you scream.
import numpy as np
import matplotlib.pyplot as plt

d = 100  # dimension
rng = np.random.default_rng(132)

dist = np.sqrt((rng.normal(size=(5000, d)) ** 2).sum(axis=1))  # from mode

print(f"Distance from the mode: {dist.mean():.2f} +/- {dist.std(ddof=1):.2f}"
      f" (sqrt(d) = {np.sqrt(d):.2f})")
print(f"Share of draws within distance 1 of the mode: "
      f"{100 * np.mean(dist < 1):.2f}%")

plt.hist(dist, bins=40, color="#2166ac")
plt.axvline(0, color="#d6604d", linewidth=3)
plt.xlim(0, dist.max())
plt.xlabel("Distance from the mode")
plt.ylabel("Draws")
plt.show()
