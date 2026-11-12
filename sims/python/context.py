# Context: in the coincidence frame, how often does an uncanny event happen?
import numpy as np
import matplotlib.pyplot as plt

readers = 100   # readers (thousands)
one_in = 1000   # chance a dead device revives in a year: 1 in ...
special = 3     # days a year that carry special meaning
rng = np.random.default_rng(111)

lam = readers * 1000 / one_in * special / 365  # expected per year
per_year = rng.poisson(lam, 50)                 # 50 simulated years

print(f"Expected coincidences per year: {lam:.1f}")
print(f"Years (of 50) with at least one: {(per_year > 0).sum()}")

plt.vlines(np.arange(1975, 2025), 0, per_year, color="#2166ac", linewidth=4)
plt.xlabel("Year")
plt.ylabel("Readers with an uncanny revival")
plt.show()
