# Robustness checks: 30 specifications, only a few of them reported.
import numpy as np
import matplotlib.pyplot as plt

true_eff = 0  # true effect
corr = 0.7    # correlation among specifications
rng = np.random.default_rng(120)

se = 0.15
# Only datasets where some specification is significant become a paper
for tries in range(1, 501):
    common = rng.normal(0, se)
    est = (true_eff + np.sqrt(corr) * common
           + np.sqrt(1 - corr) * rng.normal(0, se, 30))
    if np.any(np.abs(est) > 1.96 * se):
        break
main = est[np.argmax(np.abs(est))]            # the headline specification
reported = np.argsort(np.abs(est - main))[:6]  # and five "robustness checks"
sig = np.abs(est) > 1.96 * se
print(f"Datasets tried before a significant one: {tries}")
print(f"Significant: {sig[reported].sum()} of 6 reported specifications, "
      f"{sig.sum()} of all 30")

o = np.argsort(est)
cols = np.where(np.isin(o, reported), "#d6604d", "0.5")
plt.errorbar(est[o], np.arange(30), xerr=1.96 * se, fmt="none",
             ecolor=cols)
plt.scatter(est[o], np.arange(30), c=cols, zorder=3)
plt.axvline(0, color="black")
plt.xlabel("Estimate with 95% interval (red: reported)")
plt.ylabel("Specification")
plt.show()
