# The Self-Cleaning Oven: fake-data simulation catches a bug.
import numpy as np
import matplotlib.pyplot as plt

buggy = True  # introduce the standard-error bug
n_fake = 300  # fake datasets
rng = np.random.default_rng(18)

truth, n = 0.4, 50
t = rng.normal(truth, 1, (n_fake, n))
c = rng.normal(0, 1, (n_fake, n))
est = t.mean(axis=1) - c.mean(axis=1)
if buggy:
    se = np.sqrt(t.var(axis=1, ddof=1) / n)  # bug: forgets the control
else:
    se = np.sqrt(t.var(axis=1, ddof=1) / n + c.var(axis=1, ddof=1) / n)
lo, hi = est - 1.96 * se, est + 1.96 * se
covered = (lo <= truth) & (truth <= hi)
print(f"95% intervals cover the true effect {100 * covered.mean():.0f}% of "
      "the time" + (" (the bug shows up)" if buggy else ""))

k = np.arange(min(100, n_fake))
cols = np.where(covered[k], "#2166ac", "#d6604d")
plt.hlines(k, lo[k], hi[k], colors=cols)
plt.scatter(est[k], k, s=8, c=cols)
plt.axvline(truth, color="black", linestyle="--")
plt.xlabel("Estimate with 95% interval")
plt.ylabel("Fake dataset")
plt.show()
