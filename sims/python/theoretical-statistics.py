# Theoretical statistics is the theory of applied statistics: analyze the
# procedure people actually use.
import numpy as np
import matplotlib.pyplot as plt

beta2 = 0.2  # true effect of x2
rho_x = 0.7  # correlation between x1 and x2
rng = np.random.default_rng(121)

beta1, n = 0.5, 80


def ols(X, y):  # coefficients and standard errors, with an intercept
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    s2 = np.sum((y - X @ beta) ** 2) / (len(y) - X.shape[1])
    return beta, np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))


textbook = practice = dropped = 0
for _ in range(1000):
    x1 = rng.normal(size=n)
    x2 = rho_x * x1 + np.sqrt(1 - rho_x ** 2) * rng.normal(size=n)
    y = beta1 * x1 + beta2 * x2 + rng.normal(size=n)
    b, se = ols(np.column_stack([x1, x2]), y)
    in_full = abs(b[1] - beta1) < 1.96 * se[1]
    textbook += in_full
    if abs(b[2] / se[2]) < 1.96:          # pretest: drop x2 if n.s.
        dropped += 1
        b, se = ols(x1, y)
        practice += abs(b[1] - beta1) < 1.96 * se[1]
    else:
        practice += in_full
print(f"x2 dropped in {dropped / 10:.0f}% of datasets")
print(f"Coverage of the reported 95% interval: textbook "
      f"{textbook / 10:.1f}%, as practiced {practice / 10:.1f}%")

plt.bar(["Always fit the full model", "Pretest, drop, report"],
        [textbook / 10, practice / 10], color=["#2166ac", "#d6604d"])
plt.axhline(95, color="black", linestyle="--")
plt.ylim(0, 100)
plt.ylabel("Coverage of the 95% interval (%)")
plt.show()
