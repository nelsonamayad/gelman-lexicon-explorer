# The 80% Power Lie: planning sample sizes from published effect sizes.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

d_true = 0.2   # true effect size d
n_pilot = 30   # n per group in the published original study
rng = np.random.default_rng(82)
N = NormalDist()

se0 = np.sqrt(2 / n_pilot)
k = N.inv_cdf(0.975) + N.inv_cdf(0.8)
# Published originals are the significant ones: draw 2,000 estimates from
# the normal distribution truncated at the significance threshold.
lo = N.cdf((1.96 * se0 - d_true) / se0)
published = d_true + se0 * np.array(
    [N.inv_cdf(u) for u in rng.uniform(lo, 1, 2000)])
n_plan = np.ceil(2 * (k / published) ** 2)  # n per group "for 80% power"
actual = np.array([1 - N.cdf(1.96 - d_true / np.sqrt(2 / n))
                   for n in n_plan])

print(f"Average published effect size: {published.mean():.2f}")
print(f"True effect size: {d_true}")
print(f"Median actual power: {100 * np.median(actual):.0f}%")

plt.hist(actual, bins=np.arange(0, 1.001, 0.025), color="#d6604d")
plt.axvline(0.8, color="black", linestyle="--")
plt.xlabel("Actual power of studies planned for 80% power")
plt.ylabel("Studies")
plt.show()
