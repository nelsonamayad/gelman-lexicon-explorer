# Web of Trust: more checks catch more bugs, unless they share blind spots.
import numpy as np
import matplotlib.pyplot as plt

p_catch = 0.4  # power of each check
shared = 0     # correlation between checks (shared blind spots)
rng = np.random.default_rng(106)

K = np.arange(9)
missed = []
for k in K:
    blind = rng.uniform(size=4000) < shared   # bug in a common blind spot
    caught = (rng.uniform(size=(4000, k)) < p_catch).any(axis=1) & ~blind
    missed.append(np.mean(~caught))
print(f"Share of bugs that get through: 1 check {100 * missed[1]:.0f}%, "
      f"5 checks {100 * missed[5]:.0f}%, 8 checks {100 * missed[8]:.1f}%")

plt.plot(K, missed, "o-", color="#2166ac", label="Simulated")
plt.plot(K, (1 - p_catch) ** K, "k--", label="Independent-checks ideal")
plt.ylim(0, 1)
plt.xlabel("Number of independent checks")
plt.ylabel("Share of bugs missed")
plt.legend()
plt.show()
