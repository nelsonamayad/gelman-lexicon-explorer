# Uncertainty Interval: confidence and credible intervals cover alike, and
# fail alike.
import numpy as np
import matplotlib.pyplot as plt

prior_sd = 5       # prior sd for the Bayesian interval
clustered = False  # do the data have unmodeled clustering?
rng = np.random.default_rng(54)

truth = 1
if clustered:
    shift = np.repeat(rng.normal(0, 0.8, (400, 10)), 10, axis=1)
    y = rng.normal(truth + shift, 1)
else:
    y = rng.normal(truth, 1, (400, 100))
est = y.mean(axis=1)
se = y.std(axis=1, ddof=1) / 10
prec = 1 / prior_sd ** 2 + 1 / se ** 2       # normal prior centered at 0
post_mean, post_sd = (est / se ** 2) / prec, np.sqrt(1 / prec)
classical = np.mean(np.abs(est - truth) < 1.96 * se)
bayesian = np.mean(np.abs(post_mean - truth) < 1.96 * post_sd)
print(f"Coverage over 400 replications: classical {100 * classical:.1f}%, "
      f"Bayesian {100 * bayesian:.1f}%"
      + (" (both too narrow)" if clustered else ""))

plt.bar(["Classical", "Bayesian"], [100 * classical, 100 * bayesian],
        color=["0.7", "#2166ac"])
plt.axhline(95, color="black", linestyle="--")
plt.ylim(0, 100)
plt.ylabel("Coverage of the 95% interval (%)")
plt.show()
