# sqrt(12^2 + 5^2) = 13: independent errors add in quadrature.
import numpy as np
import matplotlib.pyplot as plt

s1 = 12  # error source 1 (sd)
s2 = 5   # error source 2 (sd)
rng = np.random.default_rng(101)


def mc(a, b):
    return np.std(rng.normal(0, a, 20000) + rng.normal(0, b, 20000))


scen = {"As is": (s1, s2), "Halve source 1": (s1 / 2, s2),
        "Halve source 2": (s1, s2 / 2), "Eliminate source 2": (s1, 0)}
for k, (a, b) in scen.items():
    print(f"{k}: formula {np.hypot(a, b):.2f}, simulated {mc(a, b):.2f}")

plt.barh(list(scen)[::-1], [np.hypot(a, b) for a, b in scen.values()][::-1],
         color="#2166ac")
plt.xlabel("Total error (sd)")
plt.tight_layout()
plt.show()
