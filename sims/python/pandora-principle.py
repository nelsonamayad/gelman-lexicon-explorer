# The Pandora Principle: once you think of a confounder, you can't unthink it.
import numpy as np
import matplotlib.pyplot as plt

confound = 0.6   # strength of confounding by U
p_matters = 0.5  # your belief that U matters
rng = np.random.default_rng(67)

u = rng.normal(size=500)
z = rng.binomial(1, 1 / (1 + np.exp(-confound * 1.5 * u)))  # depends on U
y = 0.3 * z + confound * u + rng.normal(size=500)          # true effect 0.3


def ols(X, y):  # coefficient and standard error for z (column 1)
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (len(y) - X.shape[1])
    return beta[1], np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])


mA, sA = ols(z, y)                            # ignores U
mB, sB = ols(np.column_stack([z, u]), y)      # adjusts for U
# Honest answer: a mixture of the two models, weighted by belief
mix = (1 - p_matters) * mA + p_matters * mB
sd_mix = np.sqrt((1 - p_matters) * (sA ** 2 + mA ** 2)
                 + p_matters * (sB ** 2 + mB ** 2) - mix ** 2)
rows = {"Ostrich (never thought of U)": (mA, sA), "Adjusted for U": (mB, sB),
        "Honest (unsure whether U matters)": (mix, sd_mix)}
for k, (m, s) in rows.items():
    print(f"{k}: {m:.2f} ({m - 1.96 * s:.2f} to {m + 1.96 * s:.2f})")

for i, (k, (m, s)) in enumerate(rows.items()):
    plt.errorbar(m, -i, xerr=1.96 * s, fmt="o", color="black")
plt.yticks([0, -1, -2], list(rows))
plt.axvline(0.3, color="black", linestyle="--")
plt.xlabel("Estimated effect of z (95% interval)")
plt.tight_layout()
plt.show()
