# When researchers say "guarantee", they mean an assumption.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

skew = 1.2  # skewness: sigma of the log-normal distribution
n = 15      # sample size
rng = np.random.default_rng(115)

# 97.5% quantile of the t distribution, from a series in 1/df
z = NormalDist().inv_cdf(0.975)
df = n - 1
tcrit = (z + (z ** 3 + z) / (4 * df)
         + (5 * z ** 5 + 16 * z ** 3 + 3 * z) / (96 * df ** 2))

true_mean = np.exp(skew ** 2 / 2)
y = rng.lognormal(0, skew, (3000, n))
m, half = y.mean(axis=1), tcrit * y.std(axis=1, ddof=1) / np.sqrt(n)
too_low, too_high = m + half < true_mean, m - half > true_mean
covers = ~too_low & ~too_high

print(f"Coverage of the 'guaranteed' 95% t-interval: "
      f"{100 * covers.mean():.1f}%")
print(f"Intervals entirely below the true mean: {100 * too_low.mean():.1f}%")

plt.bar(["too low", "covers", "too high"],
        [too_low.mean(), covers.mean(), too_high.mean()],
        color=["#d6604d", "#2166ac", "#e6ab02"])
plt.axhline(0.95, color="black", linestyle="--")
plt.ylabel("Share of intervals")
plt.show()
