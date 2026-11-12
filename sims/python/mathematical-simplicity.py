# Mathematical Simplicity: the golf-putting geometry model vs a logistic fit.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

sigma_deg = 1.5  # true angular error (degrees)
n_per = 200      # putts per distance
rng = np.random.default_rng(90)

R_hole, r_ball = 4.25 / 2 / 12, 1.68 / 2 / 12  # radii, in feet
cdf = np.vectorize(NormalDist().cdf)


def p_geo(x, sigma):
    return 2 * cdf(np.arcsin((R_hole - r_ball) / x) / sigma) - 1


sigma_true = sigma_deg * np.pi / 180
x = np.arange(2, 21)
y = rng.binomial(n_per, p_geo(x, sigma_true))

# Geometric model: one parameter, by maximum likelihood on a grid
grid_s = np.arange(0.002, 0.08, 0.0002)
loglik = [np.sum(y * np.log(np.clip(p_geo(x, s), 1e-9, 1 - 1e-9))
                 + (n_per - y) * np.log(np.clip(1 - p_geo(x, s), 1e-9, 1)))
          for s in grid_s]
sigma_hat = grid_s[np.argmax(loglik)]
# Logistic regression: two parameters, by Newton's method
beta = np.zeros(2)
X = np.column_stack([np.ones_like(x), x])
for _ in range(50):
    p = 1 / (1 + np.exp(-X @ beta))
    W = n_per * p * (1 - p)
    beta += np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (y - n_per * p))


def p_logit(d):
    return 1 / (1 + np.exp(-(beta[0] + beta[1] * d)))


print(f"Geometric model: sigma = {np.degrees(sigma_hat):.2f} degrees "
      f"(truth: {sigma_deg})")
print(f"At 40 feet: truth {p_geo(40, sigma_true):.3f}, geometry "
      f"{p_geo(40, sigma_hat):.3f}, logistic {p_logit(40):.3f}")

grid = np.arange(2, 40.01, 0.5)
plt.axvspan(20, 40, color="0.9")
plt.plot(x, y / n_per, "o", color="black")
plt.plot(grid, p_geo(grid, sigma_true), "--", color="0.4", label="Truth")
plt.plot(grid, p_geo(grid, sigma_hat), color="#2166ac", linewidth=2,
         label="Geometry (1 parameter)")
plt.plot(grid, p_logit(grid), color="#d6604d", linewidth=2,
         label="Logistic (2 parameters)")
plt.ylim(0, 1)
plt.xlabel("Distance (feet)")
plt.ylabel("Probability of success")
plt.legend()
plt.show()
