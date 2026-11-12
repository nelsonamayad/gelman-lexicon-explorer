# The Pinocchio Principle: a half-t prior on a group-level scale.
from math import lgamma, pi
import numpy as np
import matplotlib.pyplot as plt

A = 2.5  # scale of the prior
nu = 1   # degrees of freedom (1 = half-Cauchy)
rng = np.random.default_rng(31)

# |N(0, A)| * sqrt(nu / chi-squared(nu)) is A times the absolute value of a
# t variable with nu degrees of freedom: a half-t prior
tau = np.abs(rng.normal(0, A, 20000)) * np.sqrt(nu / rng.chisquare(nu, 20000))
for q in [50, 90, 95, 99]:
    print(f"{q}th percentile: {np.percentile(tau, q):.1f}")


def half_t(x):  # density of the half-t prior
    c = np.exp(lgamma((nu + 1) / 2) - lgamma(nu / 2)) / np.sqrt(nu * pi)
    return 2 / A * c * (1 + (x / A) ** 2 / nu) ** (-(nu + 1) / 2)


cap = np.percentile(tau, 95)
plt.hist(tau[tau < cap], bins=50, density=True, color="0.8")
xs = np.linspace(0, cap, 200)
plt.plot(xs, half_t(xs), color="#2166ac", linewidth=2)
plt.xlabel("Group-level scale tau")
plt.show()
