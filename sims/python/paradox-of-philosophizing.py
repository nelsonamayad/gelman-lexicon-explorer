# The Paradox of Philosophizing: what share of discoveries are false?
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

pi_true = 0.1  # share of tested hypotheses that are true
power = 0.4    # power of each study
rng = np.random.default_rng(36)

q = NormalDist().inv_cdf
shift = q(0.975) + q(power)  # effect (in se units) with that power
real = rng.uniform(size=5000) < pi_true
z = rng.normal(np.where(real, shift, 0), 1)
sig = np.abs(z) > 1.96
theory = 0.05 * (1 - pi_true) / (0.05 * (1 - pi_true) + power * pi_true)

print(f"{sig.sum()} significant results, {np.sum(sig & ~real)} of them "
      f"false ({100 * np.mean(~real[sig]):.0f}%; theory {100 * theory:.0f}%)")

plt.bar(["True discoveries", "False discoveries"],
        [np.sum(sig & real), np.sum(sig & ~real)],
        color=["#2166ac", "#d6604d"])
plt.ylabel("Significant results")
plt.show()
