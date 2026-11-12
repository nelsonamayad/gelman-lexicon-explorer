# The Blessing of Dimensionality: more predictors, with regularization.
import numpy as np
import matplotlib.pyplot as plt

signal = 0.15  # size of each true coefficient
lam = 40       # ridge penalty
rng = np.random.default_rng(20)

P, n = 90, 100
beta = signal * rng.choice([-1, 1], P)


def make(m):
    X = rng.normal(size=(m, P))
    return X, X @ beta + rng.normal(size=m)


X_train, y_train = make(n)
X_test, y_test = make(500)


def ridge(X, y, lam):
    """Ridge with an unpenalized intercept (lam = 0: least squares)."""
    mx, my = X.mean(axis=0), y.mean()
    Xc = X - mx
    b = np.linalg.solve(Xc.T @ Xc + (lam + 1e-9) * np.eye(X.shape[1]),
                        Xc.T @ (y - my))
    return my - mx @ b, b


def r2(fit, p):
    a, b = fit
    pred = a + X_test[:, :p] @ b
    sst = np.sum((y_test - y_test.mean()) ** 2)
    return max(-0.5, 1 - np.sum((y_test - pred) ** 2) / sst)


ps = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90]
ls = [r2(ridge(X_train[:, :p], y_train, 0), p) for p in ps]
rd = [r2(ridge(X_train[:, :p], y_train, lam), p) for p in ps]
for p, a, b in zip(ps, ls, rd):
    print(f"{p:3d} predictors: least squares R2 {a:5.2f}, ridge R2 {b:5.2f}")

plt.plot(ps, ls, "o-", color="#d6604d", label="Least squares")
plt.plot(ps, rd, "o-", color="#2166ac", label="Ridge (regularized)")
plt.xlabel("Number of predictors")
plt.ylabel("Out-of-sample R squared (floored at -0.5)")
plt.legend()
plt.show()
