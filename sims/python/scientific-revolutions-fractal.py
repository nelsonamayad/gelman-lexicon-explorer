# Scientific revolutions are fractal: power-law sizes look the same at
# every scale (a toy model).
import numpy as np
import matplotlib.pyplot as plt

alpha = 1.2  # power-law exponent
rng = np.random.default_rng(145)

sizes = np.sort((1 - rng.uniform(size=5000)) ** (-1 / alpha))[::-1]
sub = sizes[sizes < 20] * 5  # zoom into a subfield, rescaled


def ccdf(s):  # share at least this big
    return np.arange(1, len(s) + 1) / len(s)


print(f"{np.sum(sizes > 100)} of 5000 changes are more than 100 times "
      "the minimum size")

plt.loglog(sizes, ccdf(sizes), color="#2166ac", linewidth=2,
           label="All of science")
plt.loglog(sub, ccdf(sub), "--", color="#d6604d", linewidth=2,
           label="Zoomed into a subfield")
plt.xlabel("Size of the change")
plt.ylabel("Share at least this big")
plt.legend()
plt.show()
