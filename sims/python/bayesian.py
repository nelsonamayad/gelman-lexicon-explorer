# Bayesian: a confident prior in the wrong place.
import numpy as np
import matplotlib.pyplot as plt

prior_off = 1.5  # prior center minus truth
prior_sd = 0.4   # prior sd (confidence)
se = 0.5         # data standard error
rng = np.random.default_rng(23)

truth = 0
est = rng.normal(truth, se, 500)
w0, w1 = 1 / prior_sd ** 2, 1 / se ** 2
post_mean = (w0 * (truth + prior_off) + w1 * est) / (w0 + w1)
post_sd = np.sqrt(1 / (w0 + w1))

data_cover = np.mean(np.abs(est - truth) < 1.645 * se)
bayes_cover = np.mean(np.abs(post_mean - truth) < 1.645 * post_sd)
print(f"Coverage of nominal 90% intervals: data only {100 * data_cover:.0f}%,"
      f" Bayesian {100 * bayes_cover:.0f}%")

bins = np.linspace(min(est.min(), post_mean.min()) - 0.1,
                   max(est.max(), post_mean.max()) + 0.1, 41)
plt.hist(est, bins, color="#2166ac", alpha=0.5, label="Data only")
plt.hist(post_mean, bins, color="#d6604d", alpha=0.6,
         label="Bayesian posterior mean")
plt.axvline(truth, color="black", linewidth=2)
plt.axvline(prior_off, color="#d6604d", linestyle="--")
plt.xlabel("Estimate")
plt.ylabel("Replications")
plt.legend()
plt.show()
