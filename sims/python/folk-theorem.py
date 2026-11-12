# The Folk Theorem: computational trouble often means a model problem.
import numpy as np
import matplotlib.pyplot as plt

log_tau = 3.5  # log10 of the prior sd; large means nearly unidentified
iters = 3000   # iterations per chain
rng = np.random.default_rng(21)

y = rng.normal(1.5, 1, 50)
ybar, n = y.mean(), 50
tau = 10 ** log_tau


def log_post(a, b):
    """y depends on a + b only: a and b are identified only by the prior."""
    return -0.5 * n * (ybar - a - b) ** 2 - 0.5 * (a * a + b * b) / tau ** 2


def run(a, b):  # random-walk Metropolis
    out, lp = np.empty(iters), log_post(a, b)
    for t in range(iters):
        a2, b2 = a + rng.normal(0, 0.3), b + rng.normal(0, 0.3)
        lp2 = log_post(a2, b2)
        if np.log(rng.uniform()) < lp2 - lp:
            a, b, lp = a2, b2, lp2
        out[t] = a
    return out


c1, c2 = run(-5, 5), run(5, -5)
h1, h2 = c1[iters // 2:], c2[iters // 2:]  # second halves
m = len(h1)
W = (h1.var(ddof=1) + h2.var(ddof=1)) / 2
B = m * (h1.mean() - h2.mean()) ** 2 / 2
rhat = np.sqrt(((m - 1) / m * W + B / m) / W)
print(f"R-hat for a: {rhat:.2f} (well above 1.01: chains disagree)")
print("Try log_tau = 0: a weakly informative prior fixes the computation.")

plt.plot(c1, color="#2166ac", linewidth=0.8, label="Chain 1")
plt.plot(c2, color="#d6604d", linewidth=0.8, label="Chain 2")
plt.xlabel("Iteration")
plt.ylabel("Parameter a")
plt.legend()
plt.show()
