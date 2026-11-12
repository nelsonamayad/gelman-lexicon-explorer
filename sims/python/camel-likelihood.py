# The camel that is the likelihood: the data model outweighs the prior.
import math
import numpy as np
import matplotlib.pyplot as plt

n_out = 3      # number of outliers
out_size = 10  # outlier size
rng = np.random.default_rng(99)

y = np.concatenate([rng.normal(1, 1, 30), out_size + rng.normal(size=n_out)])
grid = np.arange(-4, 12.001, 0.02)  # grid of values for the mean


def post_mean(prior_sd, likelihood):
    z = y[None, :] - grid[:, None]
    if likelihood == "normal":
        loglik = (-0.5 * z ** 2).sum(axis=1)
    else:  # Student-t with 3 degrees of freedom (up to a constant)
        loglik = (-2 * np.log1p(z ** 2 / 3)).sum(axis=1)
    lp = -0.5 * (grid / prior_sd) ** 2 + loglik
    w = np.exp(lp - lp.max())
    return (w * grid).sum() / w.sum()


res = {(l, s): post_mean(s, l) for l in ("normal", "t3") for s in (1, 10)}
for (l, s), m in res.items():
    print(f"{l:6s} likelihood, prior sd {s:2d}: posterior mean {m:.3f}")
print(f"Changing the prior moves the estimate by "
      f"{abs(res['normal', 1] - res['normal', 10]):.3f} (the gnat)")
print(f"Changing the likelihood moves it by "
      f"{abs(res['normal', 10] - res['t3', 10]):.3f} (the camel)")

x = np.arange(2)
plt.bar(x - 0.2, [res["normal", 1], res["normal", 10]], 0.4,
        color="#d6604d", label="Normal")
plt.bar(x + 0.2, [res["t3", 1], res["t3", 10]], 0.4, color="#2166ac",
        label="Student-t (3 df)")
plt.xticks(x, ["Prior sd 1", "Prior sd 10"])
plt.ylabel("Posterior mean")
plt.legend()
plt.show()
