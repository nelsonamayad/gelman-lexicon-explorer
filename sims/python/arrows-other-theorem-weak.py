# Arrow's Other Theorem (weak form): no result is published more than 5 times.
import numpy as np
import matplotlib.pyplot as plt

p = 0.5  # probability a result is repackaged once more
rng = np.random.default_rng(33)

pubs = []
for _ in range(500):
    k = 1
    while k < 5 and rng.uniform() < p:
        k += 1
    pubs.append(k)
pubs = np.array(pubs)
theory = 5 if p == 1 else (1 - p ** 5) / (1 - p)

print(f"500 distinct results produced {pubs.sum()} publications")
print(f"Redundancy ratio: {pubs.mean():.2f} (theory: {theory:.2f})")

counts = [(pubs == k).sum() for k in range(1, 6)]
plt.bar(range(1, 6), counts, color="#2166ac")
plt.xlabel("Publications per result")
plt.ylabel("Results")
plt.show()
