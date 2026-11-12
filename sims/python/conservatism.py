# Conservatism: is the familiar method (no pooling) the cautious one?
import numpy as np
import matplotlib.pyplot as plt

tau = 0.3   # true between-group sd
avg_n = 10  # average group size
rng = np.random.default_rng(19)

theta = rng.normal(0, tau, 40)              # 40 groups' true means
n_j = np.maximum(2, rng.poisson(avg_n, 40))
ybar = np.array([rng.normal(t, 1, n).mean() for t, n in zip(theta, n_j)])
v = 1 / n_j                                 # sampling variance of each mean
mu = np.sum(ybar / v) / np.sum(1 / v)
tau2 = max(0.001, np.mean((ybar - mu) ** 2) - v.mean())
pooled = mu + tau2 / (tau2 + v) * (ybar - mu)  # partial pooling


def rmse(est):
    return np.sqrt(np.mean((est - theta) ** 2))


print(f"RMSE: no pooling {rmse(ybar):.3f} | partial pooling "
      f"{rmse(pooled):.3f}")
best = np.argmax(ybar)
print(f"No pooling's 'best' group: estimate {ybar[best]:.2f} "
      f"but true mean {theta[best]:.2f}")

plt.scatter(theta, ybar, color="#d6604d", label="No pooling")
plt.scatter(theta, pooled, color="#2166ac", label="Partial pooling")
lim = [theta.min(), theta.max()]
plt.plot(lim, lim, "k--")
plt.xlabel("True group mean")
plt.ylabel("Estimate")
plt.legend()
plt.show()
