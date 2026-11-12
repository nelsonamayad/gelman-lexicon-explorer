# The most important aspect of a statistical method is what data it uses.
import numpy as np
import matplotlib.pyplot as plt

rho = 0.8  # pre-test correlation with the outcome
n = 60     # participants per arm
rng = np.random.default_rng(66)

effect = 0.3
z = np.repeat([1, 0], n)
X = np.column_stack([np.ones(2 * n), z, np.zeros(2 * n)])


def shrink(est, se):  # posterior mean with a N(0, 1) prior
    return (est / se ** 2) / (1 + 1 / se ** 2)


est = {"Frequentist, outcome only": [], "Bayesian, outcome only": [],
       "Frequentist + pre-test": [], "Bayesian + pre-test": []}
for _ in range(300):
    x = rng.normal(size=2 * n)
    y = effect * z + rho * x + np.sqrt(1 - rho ** 2) * rng.normal(size=2 * n)
    d = y[z == 1].mean() - y[z == 0].mean()
    se_d = np.sqrt(y[z == 1].var(ddof=1) / n + y[z == 0].var(ddof=1) / n)
    X[:, 2] = x
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    s2 = np.sum((y - X @ beta) ** 2) / (2 * n - 3)
    se_b = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    for k, v in zip(est, [d, shrink(d, se_d), beta[1],
                          shrink(beta[1], se_b)]):
        est[k].append(v)
rmse = {k: np.sqrt(np.mean((np.array(v) - effect) ** 2))
        for k, v in est.items()}
for k, v in rmse.items():
    print(f"{k}: RMSE {v:.3f}")

plt.barh(list(rmse)[::-1], list(rmse.values())[::-1],
         color=["#2166ac", "#2166ac", "0.7", "0.7"])
plt.xlabel("Root mean squared error")
plt.tight_layout()
plt.show()
