# Tall-Person Syndrome: the view from up there exaggerates the advantage.
import numpy as np
import matplotlib.pyplot as plt

real_slope = 0.1  # real association: outcome per sd of height
perceived = 0.8   # perceived importance per sd of height
rng = np.random.default_rng(110)

h = rng.normal(size=1000)
outcome = real_slope * h + rng.normal(size=1000)
feel = perceived * h + rng.normal(0, 0.5, 1000)
print(f"Correlation of height with the actual outcome: "
      f"{np.corrcoef(h, outcome)[0, 1]:.2f}")
print(f"With felt importance: {np.corrcoef(h, feel)[0, 1]:.2f}")

fig, ax = plt.subplots(1, 2, figsize=(9, 4), sharex=True)
ax[0].scatter(h, outcome, s=4, color="#2166ac")
ax[0].set_title("Reality")
ax[1].scatter(h, feel, s=4, color="#d6604d")
ax[1].set_title("How it feels")
for a in ax:
    a.set_xlabel("Height (sd)")
plt.show()
