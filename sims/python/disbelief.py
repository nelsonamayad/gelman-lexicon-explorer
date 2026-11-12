# Disbelief remains an option: published results are selected results.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

n_pub = 8    # published significant studies
prior = 0.1  # prior probability the effect is real
rng = np.random.default_rng(103)
N = NormalDist()

delta = 2.5  # z-score shift if the effect were real
# The truth is no effect: published z-scores are draws above 1.96
z = np.array([N.inv_cdf(u) for u in rng.uniform(N.cdf(1.96), 1, n_pub)])
d_real = np.array([NormalDist(delta).pdf(v) for v in z])
d_null = np.array([N.pdf(v) for v in z])
lr_naive = d_real / d_null
lr_aware = ((d_real / (1 - N.cdf(1.96 - delta)))
            / (d_null / (1 - N.cdf(1.96))))  # conditions on selection
logit_prior = np.log(prior / (1 - prior))
naive = 1 / (1 + np.exp(-(logit_prior + np.cumsum(np.log(lr_naive)))))
aware = 1 / (1 + np.exp(-(logit_prior + np.cumsum(np.log(lr_aware)))))

print(f"After {n_pub} published studies, the naive reader is "
      f"{100 * naive[-1]:.1f}% convinced; the selection-aware reader is "
      f"{100 * aware[-1]:.1f}%")

k = np.arange(n_pub + 1)
plt.plot(k, np.r_[prior, naive], "o-", color="#d6604d",
         label="Naive (no selection)")
plt.plot(k, np.r_[prior, aware], "o-", color="#2166ac",
         label="Selection-aware")
plt.ylim(0, 1)
plt.xlabel("Published significant studies")
plt.ylabel("Probability the effect is real")
plt.legend()
plt.show()
