# The Bayesian cringe: using what the field already knows.
import numpy as np
import matplotlib.pyplot as plt

tau = 0.15  # typical effect size in the field
se = 0.3    # standard error of a typical study
rng = np.random.default_rng(97)

theta = rng.normal(0, tau, 2000)  # true effects
y = rng.normal(theta, se)         # flat prior: take the estimate as is
informed = tau ** 2 / (tau ** 2 + se ** 2) * y  # posterior mean


def rmse(est):
    return np.sqrt(np.mean((est - theta) ** 2))


print(f"Root-mean-square error: flat prior {rmse(y):.3f} "
      f"| informed prior {rmse(informed):.3f}")
print(f"Reduction in error: {100 * (1 - rmse(informed) / rmse(y)):.0f}%")

plt.scatter(theta[:500], y[:500], s=5, color="#d6604d", alpha=0.4,
            label="Flat prior (cringe)")
plt.scatter(theta[:500], informed[:500], s=5, color="#2166ac", alpha=0.6,
            label="Uses prior information")
lim = 4 * tau
plt.plot([-lim, lim], [-lim, lim], "k--")
plt.xlabel("True effect")
plt.ylabel("Estimate")
plt.legend()
plt.show()
