# Random in, random out: regressions on pure noise still find "effects".
import numpy as np
import matplotlib.pyplot as plt

n = 80           # observations per dataset
real_effect = 0  # true effect of predictor 1 (the others are zero)
rng = np.random.default_rng(79)

# 25 datasets, each a regression of y on 10 predictors
sig = np.zeros((25, 10), dtype=bool)
for rep in range(25):
    X = np.column_stack([np.ones(n), rng.normal(size=(n, 10))])
    y = real_effect * X[:, 1] + rng.normal(size=n)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    s2 = np.sum((y - X @ beta) ** 2) / (n - 11)
    se = np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))
    sig[rep] = np.abs(beta / se)[1:] > 1.96
print(f"{np.sum(sig.any(axis=1))} of 25 datasets have at least one "
      f"'significant' predictor\nPredictor 1 is significant in "
      f"{sig[:, 0].sum()} of 25")

plt.imshow(sig, cmap="Reds", aspect="auto", vmin=0, vmax=1.5,
           extent=[0.5, 10.5, 25.5, 0.5])
plt.xlabel("Predictor")
plt.ylabel("Dataset")
plt.show()
