# Breadcrumbs: undocumented decisions make results irreproducible.
import numpy as np
import matplotlib.pyplot as plt

documented = 3  # decision points documented (of 10)
rng = np.random.default_rng(78)

shifts = rng.normal(0, 0.08, (10, 4))  # 10 decisions x 4 options
chosen = rng.integers(0, 4, 10)        # what the authors did
published = 0.25 + shifts[np.arange(10), chosen].sum()
reanalyses = []
for _ in range(300):
    pick = chosen.copy()
    pick[documented:] = rng.integers(0, 4, 10 - documented)
    reanalyses.append(0.25 + shifts[np.arange(10), pick].sum())
reanalyses = np.array(reanalyses)

print(f"Published estimate: {published:.3f}")
print(f"Spread (sd) of re-analyses with {documented} of 10 steps documented: "
      f"{reanalyses.std(ddof=1):.3f}")

plt.hist(reanalyses, bins=30, color="#2166ac")
plt.axvline(published, color="#d6604d", linewidth=3)
plt.xlabel("Re-analysis estimate")
plt.ylabel("Re-analyses")
plt.show()
