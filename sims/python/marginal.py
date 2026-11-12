# Marginal: an integral in statistics, a derivative in economics.
import numpy as np
import matplotlib.pyplot as plt

b = 1.2   # slope (log-odds per unit x)
x0 = 0.5  # point for the derivative
rng = np.random.default_rng(126)

a = -0.5
x = rng.normal(0.3, 1, 5000)  # the distribution of x


def p(v):
    return 1 / (1 + np.exp(-(a + b * v)))


stat_marginal = p(x).mean()          # Pr(y = 1), averaging over x
slope = b * p(x0) * (1 - p(x0))      # dPr/dx at x0
ame = np.mean(b * p(x) * (1 - p(x)))  # average marginal effect

print(f"Statistics' marginal: Pr(y = 1) = {stat_marginal:.3f}")
print(f"Economics' marginal at x0: {slope:.3f} per unit x")
print(f"Average marginal effect over x: {ame:.3f}")

xs = np.linspace(-4, 4, 200)
plt.plot(xs, p(xs), color="#2166ac", linewidth=2)
plt.axhline(stat_marginal, color="#2166ac", linestyle="--")
plt.plot([x0 - 1, x0 + 1], [p(x0) - slope, p(x0) + slope],
         color="#d6604d", linewidth=2)
plt.plot(x[:800], np.zeros(800), "|", color="0.6")
plt.ylim(-0.02, 1)
plt.xlabel("x")
plt.ylabel("Pr(y = 1)")
plt.show()
