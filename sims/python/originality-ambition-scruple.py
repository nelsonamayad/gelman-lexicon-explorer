# Originality, ambition, and lack of scruple: who rises to the top?
import numpy as np
import matplotlib.pyplot as plt

reward = 1  # how much citations reward exaggeration
rng = np.random.default_rng(151)

N = 5000
O, A, S = rng.normal(size=(3, N))  # originality, ambition, scruple
exaggeration = np.maximum(0, A - S)
cites = O + reward * exaggeration + rng.normal(0, 0.5, N)
top = np.argsort(-cites).argsort() < 100  # the top 2% by citations

traits = {"Originality": O, "Ambition": A, "Scruple": S}
for name, v in traits.items():
    print(f"{name}: top 2% {v[top].mean():.2f}, "
          f"everyone else {v[~top].mean():.2f}")

x = np.arange(3)
plt.bar(x - 0.2, [v[top].mean() for v in traits.values()], 0.4,
        color="#d6604d", label="Top 2% by citations")
plt.bar(x + 0.2, [v[~top].mean() for v in traits.values()], 0.4,
        color="0.7", label="Everyone else")
plt.xticks(x, list(traits))
plt.axhline(0, color="black")
plt.ylabel("Average (standard units)")
plt.legend()
plt.show()
