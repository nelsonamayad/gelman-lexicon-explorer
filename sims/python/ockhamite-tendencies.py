# Ockhamite Tendencies: zeroing out small effects vs partial pooling.
import numpy as np
import matplotlib.pyplot as plt

tau = 0.4  # spread of true effects
se = 0.4   # standard error of each estimate
rng = np.random.default_rng(22)

truth = rng.normal(0, tau, 40)
est = rng.normal(truth, se)
tau2_hat = max(0.0001, np.mean(est ** 2) - se ** 2)
selected = np.where(np.abs(est / se) > 2, est, 0)  # keep "significant"
pooled = tau2_hat / (tau2_hat + se ** 2) * est     # shrink everything


def rmse(x):
    return np.sqrt(np.mean((x - truth) ** 2))


print(f"Error (RMSE): raw {rmse(est):.2f}, select-or-zero "
      f"{rmse(selected):.2f} ({np.sum(selected != 0)} of 40 kept), "
      f"partial pooling {rmse(pooled):.2f}")

plt.scatter(truth, selected, color="#d6604d", label="Select or zero")
plt.scatter(truth, pooled, color="#2166ac", label="Partial pooling")
lim = [truth.min(), truth.max()]
plt.plot(lim, lim, "k--")
plt.xlabel("True effect")
plt.ylabel("Estimate")
plt.legend()
plt.show()
