# The Causal Identification Kool-Aid: forking paths in a discontinuity design.
import numpy as np
import matplotlib.pyplot as plt

n = 200        # observations
noise_sd = 1   # outcome noise (sd)
rng = np.random.default_rng(83)

specs = [("Local linear, h = 0.25", 0.25, 1),
         ("Local linear, h = 0.5", 0.5, 1),
         ("Global linear", 1, 1), ("Global quadratic", 1, 2),
         ("Global cubic", 1, 3), ("Global quartic", 1, 4)]


def z_jump(x, y, h, order):
    """z statistic of the jump at x = 0, separate polynomials each side."""
    keep = np.abs(x) <= h
    x, y = x[keep], y[keep]
    cut = (x >= 0).astype(float)
    cols = [np.ones_like(x), cut]
    for k in range(1, order + 1):
        cols += [x ** k, cut * x ** k]
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (len(y) - X.shape[1])
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return beta[1] / se


sig = np.zeros((300, len(specs)), dtype=bool)
for rep in range(300):
    x = rng.uniform(-1, 1, n)  # the true discontinuity is zero
    y = 0.5 * x ** 2 + 0.3 * x + rng.normal(0, noise_sd, n)
    sig[rep] = [abs(z_jump(x, y, h, o)) > 1.96 for _, h, o in specs]

rates = list(sig.mean(axis=0)) + [sig.any(axis=1).mean()]
labels = [s[0] for s in specs] + ["Any of the six"]
for label, rate in zip(labels, rates):
    print(f"{label}: {100 * rate:.0f}% false positives")

plt.barh(labels[::-1], rates[::-1], color=["#d6604d"] + ["#2166ac"] * 6)
plt.axvline(0.05, color="black", linestyle="--")
plt.xlabel("False-positive rate (true jump is zero)")
plt.tight_layout()
plt.show()
