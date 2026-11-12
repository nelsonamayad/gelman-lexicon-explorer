# More Vampirical Than Empirical: theories that explain away every failure.
import numpy as np
import matplotlib.pyplot as plt

m = 0.85   # probability a failure is explained away
lr = 0.4   # likelihood ratio of each failed test
rng = np.random.default_rng(45)

# Belief in a false theory, starting at 80%, over 20 tests
emp = vam = np.log(4)
empirical, vampirical = [0.8], [0.8]
for k in range(20):
    success = rng.uniform() < 0.08        # occasional false positive
    step = np.log(1 / lr) if success else np.log(lr)
    emp += step
    vam += step if success or rng.uniform() >= m else 0
    empirical.append(1 / (1 + np.exp(-emp)))
    vampirical.append(1 / (1 + np.exp(-vam)))
print(f"Belief in the theory after 20 tests: empirical "
      f"{100 * empirical[-1]:.0f}%, vampirical {100 * vampirical[-1]:.0f}%")

plt.plot(empirical, color="#2166ac", linewidth=2, label="Empirical")
plt.plot(vampirical, color="#d6604d", linewidth=2, label="Vampirical")
plt.ylim(0, 1)
plt.xlabel("Tests of the theory")
plt.ylabel("Belief the theory is true")
plt.legend()
plt.show()
