# In a dark room with most lights covered, a weak beam looks brilliant.
import numpy as np
import matplotlib.pyplot as plt

true_pct = 0.4  # true percentile of the focal idea
favored = 0.7   # how much the covering favors weaker rivals
rng = np.random.default_rng(140)

others = np.sort(rng.normal(size=199))  # brightness of 199 rivals
focal = others[int(true_pct * 198)]     # a middling idea
visible = 1 - np.arange(20) * 0.05      # share of rivals left uncovered
apparent = []
for vis in visible:
    cover = np.minimum(1, (1 - vis) * np.where(others > focal, 1 + favored,
                                               1 - favored))
    shares = []
    for _ in range(200):
        seen = others[rng.uniform(size=199) >= cover]
        shares.append((seen < focal).mean() if seen.size else 1)
    apparent.append(np.mean(shares))

print(f"Truly outshines {100 * true_pct:.0f}% of rivals; appears to outshine "
      f"{100 * apparent[0]:.0f}% with every light visible and "
      f"{100 * apparent[-1]:.0f}% with most covered")

plt.plot(visible, apparent, color="#e6ab02", linewidth=3)
plt.axhline(true_pct, color="black", linestyle="--")
plt.xlim(1, 0.05)
plt.ylim(0, 1)
plt.xlabel("Share of rival lights left uncovered")
plt.ylabel("Share of visible rivals it outshines")
plt.show()
