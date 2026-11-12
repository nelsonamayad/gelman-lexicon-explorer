# Probability: a long-run frequency, and a degree of belief that learns.
import numpy as np
import matplotlib.pyplot as plt

p = 0.3      # true probability of heads
flips = 200  # number of flips
rng = np.random.default_rng(10)

heads = np.cumsum(rng.binomial(1, p, flips))
n = np.arange(1, flips + 1)
a, b = 1 + heads, 1 + n - heads           # Beta posterior, uniform prior
post = a / (a + b)
sdv = np.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
lo, hi = np.maximum(0, post - 1.645 * sdv), np.minimum(1, post + 1.645 * sdv)
print(f"After {flips} flips: frequency {heads[-1] / flips:.3f}, "
      f"90% interval {lo[-1]:.2f} to {hi[-1]:.2f}")

plt.plot(n, heads / n, color="0.5", label="Running frequency")
plt.fill_between(n, lo, hi, color="#2166ac", alpha=0.2)
plt.plot(n, post, color="#2166ac", linewidth=2, label="Posterior mean")
plt.axhline(p, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("Flips")
plt.ylabel("Probability of heads")
plt.legend()
plt.show()
