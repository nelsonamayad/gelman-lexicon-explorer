# Weakly Informative Priors: logistic regression with small samples.
import numpy as np
import matplotlib.pyplot as plt

n = 20           # observations per study
true_beta = 1.5  # true slope
prior_sd = 2.5   # prior sd on the slope
rng = np.random.default_rng(13)


def fit_logit(x, y, s):
    # Posterior mode by Newton-Raphson; intercept prior sd 10, slope prior
    # sd s (s = 0 means a flat prior: the maximum likelihood estimate)
    prec = np.array([1 / 100, 1 / s ** 2 if s > 0 else 0])
    beta, X = np.zeros(2), np.column_stack([np.ones(len(x)), x])
    for _ in range(60):
        p = 1 / (1 + np.exp(-X @ beta))
        grad = X.T @ (y - p) - prec * beta
        H = -(X.T * (p * (1 - p))) @ X - np.diag(prec)
        if abs(np.linalg.det(H)) < 1e-12:
            beta[1] += np.sign(grad[1]) * 5
            continue
        beta -= np.linalg.solve(H, grad)
        if abs(beta[1]) > 1e3:
            break
    return np.clip(beta[1], -50, 50)


flat, weak = [], []
for _ in range(200):
    x = rng.normal(size=n)
    y = rng.binomial(1, 1 / (1 + np.exp(-(-0.3 + true_beta * x))))
    flat.append(fit_logit(x, y, 0))
    weak.append(fit_logit(x, y, prior_sd))
flat, weak = np.array(flat), np.array(weak)


def rmse(v):
    return np.sqrt(np.mean((v - true_beta) ** 2))


print(f"Flat prior: {100 * np.mean(np.abs(flat) > 20):.0f}% of estimates "
      f"blow up past +/-20; RMSE {rmse(flat):.2f}")
print(f"Weakly informative N(0, {prior_sd}): RMSE {rmse(weak):.2f}")

plt.boxplot([np.clip(flat, -10, 10), np.clip(weak, -10, 10)])
plt.xticks([1, 2], ["Flat prior (MLE)", "Weakly informative"])
plt.axhline(true_beta, color="black", linestyle="--")
plt.ylabel("Estimated slope (clipped at +/-10)")
plt.show()
