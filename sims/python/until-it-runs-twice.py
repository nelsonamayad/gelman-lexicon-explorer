# Until it runs twice: two runs of a sampler expose a stuck chain.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

gap = 5     # distance between the two modes
step = 0.5  # proposal step size
rng = np.random.default_rng(2)

# A posterior with two well-separated modes; its true mean is 0
left, right = NormalDist(-gap / 2, 0.7), NormalDist(gap / 2, 0.7)


def logp(x):
    return np.log(0.5 * left.pdf(x) + 0.5 * right.pdf(x) + 1e-300)


def run(x):  # random-walk Metropolis
    out, lp = [], logp(x)
    for _ in range(2000):
        y = x + rng.normal(0, step)
        ly = logp(y)
        if np.log(rng.uniform()) < ly - lp:
            x, lp = y, ly
        out.append(x)
    return np.array(out)


r1, r2 = run(rng.uniform(-gap, gap)), run(rng.uniform(-gap, gap))
m1, m2 = r1[1000:].mean(), r2[1000:].mean()
print(f"Second-half means: run 1 {m1:.2f}, run 2 {m2:.2f} (true mean 0)")
print("The runs disagree." if abs(m1 - m2) > 1 else "The runs agree.")

plt.plot(r1, color="#2166ac")
plt.plot(r2, color="#d6604d")
plt.xlabel("Iteration")
plt.ylabel("x")
plt.show()
