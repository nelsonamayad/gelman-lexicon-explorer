# You have no obligation to share your data and code (but it is a signal).
import numpy as np
import matplotlib.pyplot as plt

e = 0.25        # base rate of serious errors
s_right = 0.7   # probability of sharing if the analysis is sound
s_wrong = 0.35  # probability of sharing if the analysis is flawed
rng = np.random.default_rng(150)

wrong = rng.uniform(size=5000) < e
shared = rng.uniform(size=5000) < np.where(wrong, s_wrong, s_right)
caught = shared & wrong & (rng.uniform(size=5000) < 0.7)  # 70% found
groups = {"Shared: checks out": shared & ~caught, "Not shared": ~shared,
          "Shared: error found": caught}
correct = {k: 100 * np.mean(~wrong[g]) for k, g in groups.items()}
for k, v in correct.items():
    print(f"{k}: {v:.0f}% of analyses are correct")

plt.bar(list(correct), list(correct.values()),
        color=["#2166ac", "0.7", "#d6604d"])
plt.ylim(0, 100)
plt.ylabel("Analyses that are correct (%)")
plt.show()
