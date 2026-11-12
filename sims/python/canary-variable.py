# Canary variable: a known quantity that warns of hidden selection.
import numpy as np
import matplotlib.pyplot as plt

hidden = 1         # strength of hidden selection
canary_link = 0.7  # canary's correlation with the hidden trait
rng = np.random.default_rng(117)


def logistic(x):
    return 1 / (1 + np.exp(-x))


def population(n):
    old = rng.binomial(1, 0.5, n)
    u = rng.normal(size=n)  # trait we can't adjust for
    target = rng.binomial(1, logistic(-0.2 + 0.4 * old + 0.8 * u))
    canary = rng.binomial(1, logistic(canary_link * 1.5 * u + 0.3 * old))
    return old, u, target, canary


_, _, t_pop, c_pop = population(40000)
truth_target, truth_canary = t_pop.mean(), c_pop.mean()

canary_err, target_err = [], []
for _ in range(200):
    h = hidden * rng.uniform(0.2, 1.2)  # selection strength varies
    old, u, target, canary = population(4000)
    resp = rng.uniform(size=4000) < logistic(-2 + 0.8 * old + h * u)
    o = old[resp]
    w = np.where(o == 1, 0.5 / o.mean(), 0.5 / (1 - o.mean()))
    canary_err.append(np.average(canary[resp], weights=w) - truth_canary)
    target_err.append(np.average(target[resp], weights=w) - truth_target)

print(f"Correlation of canary error with target error: "
      f"{np.corrcoef(canary_err, target_err)[0, 1]:.2f}")
print(f"Average target error after weighting: {np.mean(target_err):.3f}")

plt.scatter(canary_err, target_err, color="#2166ac")
plt.axhline(0, color="black", linestyle="--")
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("Canary's error after weighting")
plt.ylabel("Target's error after weighting")
plt.show()
