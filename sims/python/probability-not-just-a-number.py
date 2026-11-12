# A probability isn't just a number: correlated outcomes in two states.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

p_A = 0.7  # P(win state A) = P(win state B)
rho = 0.7  # correlation between the states' outcomes
rng = np.random.default_rng(114)

N = 40000
cut = NormalDist().inv_cdf(1 - p_A)
z1 = rng.normal(size=N)
z2 = rho * z1 + np.sqrt(1 - rho ** 2) * rng.normal(size=N)
A, B = z1 > cut, z2 > cut
probs = {"P(A)": A.mean(), "P(B)": B.mean(), "P(A and B)": (A & B).mean(),
         "P(B | won A)": B[A].mean(), "P(B | lost A)": B[~A].mean()}
for k, v in probs.items():
    print(f"{k}: {v:.2f}")
print(f"If the states were independent, P(A and B) would be {p_A ** 2:.2f}")

plt.barh(list(probs)[::-1], list(probs.values())[::-1], color="#2166ac")
plt.xlim(0, 1)
plt.xlabel("Probability")
plt.tight_layout()
plt.show()
