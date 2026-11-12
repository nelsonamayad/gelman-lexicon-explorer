# Kangaroo: weighing a feather on a bouncing kangaroo.
import numpy as np
import matplotlib.pyplot as plt

bounce = 3        # kangaroo bounce: sd of one reading (kg)
n = 30            # readings with the feather, and again without it
feather = 0.005   # true weight of the feather (kg)
rng = np.random.default_rng(52)

# 1,000 experiments: the difference between the two average readings
est = (rng.normal(40 + feather, bounce, (1000, n)).mean(axis=1)
       - rng.normal(40, bounce, (1000, n)).mean(axis=1))
se = bounce * np.sqrt(2 / n)
sig = np.abs(est) > 1.96 * se

print(f"Significant experiments: {sig.sum()} of 1000")
print(f"Their estimates average {np.abs(est[sig]).mean() / feather:.0f} "
      "times the true weight")
print(f"Significant estimates with negative weight: {(est[sig] < 0).sum()}")

bins = np.histogram_bin_edges(est, 50)
plt.hist(est, bins, color="0.8", label="All experiments")
plt.hist(est[sig], bins, color="#d6604d", label="Significant")
plt.axvline(feather, color="#2166ac", linewidth=2)
plt.xlabel("Estimated feather weight (kg)")
plt.ylabel("Experiments")
plt.legend()
plt.show()
