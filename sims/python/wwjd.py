# WWJD (What would Jennifer Hill do?): restrict to the region of overlap.
import numpy as np
import matplotlib.pyplot as plt

separation = 2   # covariate gap between groups
curvature = 0.5  # nonlinearity in the outcome
rng = np.random.default_rng(6)

z = rng.binomial(1, 0.5, 600)
x = np.where(z == 1, rng.normal(separation, 0.6, 600),
             rng.normal(0, 1.2, 600))
y = curvature * x ** 2 + 1 * z + rng.normal(size=600)  # true effect: 1


def coef_z(cols, keep):  # OLS coefficient on z
    X = np.column_stack([np.ones(keep.sum())] + [c[keep] for c in cols])
    return np.linalg.lstsq(X, y[keep], rcond=None)[0][1]


everyone = np.ones(600, dtype=bool)
naive = coef_z([z, x], everyone)
lo = max(x[z == 1].min(), x[z == 0].min())
hi = min(x[z == 1].max(), x[z == 0].max())
cs = (x >= lo) & (x <= hi)                 # common support
restricted = coef_z([z, x, x ** 2], cs)
print(f"Naive linear regression, all units: {naive:.2f}")
print(f"Overlap only ({cs.sum()} units), with a quadratic: "
      f"{restricted:.2f}\nTrue effect: 1")

plt.axvspan(lo, hi, color="0.9")
plt.scatter(x, y, s=6, c=np.where(z == 1, "#d6604d", "#2166ac"))
plt.xlabel("Covariate x (shaded: overlap)")
plt.ylabel("Outcome y")
plt.show()
