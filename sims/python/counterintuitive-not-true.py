# Just because something is counterintuitive doesn't mean it's true.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

power = 0.5  # power of each study
rng = np.random.default_rng(76)

N = NormalDist()
shift = N.inv_cdf(0.975) + N.inv_cdf(power)  # effect in s.e. units
priors = np.array([0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
ppv = []
for p in priors:  # share of significant results that are real
    real = rng.uniform(size=20000) < p
    z = rng.normal(np.where(real, shift, 0), 1)
    sig = np.abs(z) > 1.96
    ppv.append(real[sig].mean())
theory = priors * power / (priors * power + (1 - priors) * 0.05)
for p, s, t in zip(priors, ppv, theory):
    print(f"prior {p:.2f}: simulated {s:.2f}, theory {t:.2f}")

plt.semilogx(priors, ppv, "o", color="#2166ac", label="Simulated")
plt.semilogx(priors, theory, color="#d6604d", label="Theory")
plt.ylim(0, 1)
plt.xlabel("Prior probability the hypothesis is true (log scale)")
plt.ylabel("Share of significant results that are true")
plt.legend()
plt.show()
