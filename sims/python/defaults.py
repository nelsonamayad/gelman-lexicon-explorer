# Defaults: one default prior scale for thousands of different problems.
import numpy as np
import matplotlib.pyplot as plt

spread = 1  # typical effect size across users
rng = np.random.default_rng(37)

tau = spread * np.exp(rng.normal(0, 0.7, 3000))  # each user's effect scale
se = np.exp(rng.normal(-0.3, 0.6, 3000))         # each user's standard error
theta = rng.normal(0, tau)
y = rng.normal(theta, se)
scales = np.array([0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10, 100])
rmse = []
for s in scales:
    w = s ** 2 / (s ** 2 + se ** 2)  # posterior mean under a N(0, s) prior
    rmse.append(np.sqrt(np.mean((w * y - theta) ** 2)))
rmse = np.array(rmse)

print(f"Best default scale: {scales[rmse.argmin()]} "
      f"(RMSE {rmse.min():.3f})")
print(f"Flat 'no default' (scale 100): RMSE {rmse[-1]:.3f}")

plt.semilogx(scales, rmse, "o-", color="#2166ac")
plt.xlabel("Default prior scale s (log scale)")
plt.ylabel("Average error across users (RMSE)")
plt.show()
