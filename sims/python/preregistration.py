# Preregistration: a plan that adjusts for a baseline covariate.
import numpy as np
import matplotlib.pyplot as plt

rho = 0.7  # correlation of the baseline covariate with the outcome
n = 60     # participants per arm
rng = np.random.default_rng(133)

effect = 0.3
z = np.repeat([1, 0], n)
floor_est, floor_se, adj_est, adj_se = [], [], [], []
for _ in range(500):
    x = rng.normal(size=2 * n)
    y = effect * z + rho * x + np.sqrt(1 - rho ** 2) * rng.normal(size=2 * n)
    t, c = y[z == 1], y[z == 0]
    floor_est.append(t.mean() - c.mean())   # difference in means
    floor_se.append(np.sqrt(t.var(ddof=1) / n + c.var(ddof=1) / n))
    X = np.column_stack([np.ones(2 * n), z, x])  # adjusted regression
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    s2 = np.sum((y - X @ beta) ** 2) / (2 * n - 3)
    adj_est.append(beta[1])
    adj_se.append(np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1]))


def cover(e, s):
    return 100 * np.mean(np.abs(np.array(e) - effect) < 1.96 * np.array(s))


print(f"Difference in means: average se {np.mean(floor_se):.3f}, "
      f"coverage {cover(floor_est, floor_se):.0f}%")
print(f"Adjusted for baseline: average se {np.mean(adj_se):.3f}, "
      f"coverage {cover(adj_est, adj_se):.0f}%")

plt.boxplot([floor_est, adj_est])
plt.xticks([1, 2], ["Difference in means", "Adjusted for baseline"])
plt.axhline(effect, color="black", linestyle="--")
plt.ylabel("Estimated effect")
plt.show()
