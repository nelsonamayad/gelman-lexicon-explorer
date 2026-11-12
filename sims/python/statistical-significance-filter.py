# The Statistical Significance Filter: significant estimates are too big.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

theta = 0.2  # true effect
se = 0.25    # standard error
rng = np.random.default_rng(42)

est = rng.normal(theta, se, 400)       # 400 replications of the study
sig = np.abs(est) > 1.96 * se
Phi = NormalDist().cdf
power = 1 - Phi(1.96 - theta / se) + Phi(-1.96 - theta / se)
avg = np.abs(est[sig]).mean()
print(f"Power: {100 * power:.0f}%; {sig.sum()} of 400 significant")
print(f"Average significant estimate: {avg:.2f} ({avg / theta:.1f} times "
      f"the truth); {np.sum(sig & (np.sign(est) != np.sign(theta)))} with "
      "the wrong sign")

plt.scatter(np.arange(400), est, s=8, c=np.where(sig, "#d6604d", "0.7"))
plt.axhline(theta, color="#2166ac", linewidth=2)
plt.axhline(1.96 * se, color="black", linestyle="--")
plt.axhline(-1.96 * se, color="black", linestyle="--")
plt.xlabel("Replication")
plt.ylabel("Estimate")
plt.show()
