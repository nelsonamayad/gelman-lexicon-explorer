# The Piranha Principle: there can't be many large independent effects.
import numpy as np
import matplotlib.pyplot as plt

r = 0.3  # claimed correlation of each factor with the outcome
K = 20   # number of claimed independent factors
# Deterministic: no random numbers. Independent factors with correlation
# r each explain r^2 of the variance, and the shares can't add past 100%.

explained = K * r ** 2
max_k = int(1 / r ** 2)
print(f"{K} factors with r = {r} would explain {100 * explained:.0f}% of "
      f"the variance\nAt most {max_k} such factors can coexist")

k = np.arange(1, 51)
plt.bar(k, k * r ** 2, color=np.where(k * r ** 2 > 1, "#d6604d", "#2166ac"))
plt.axhline(1, color="black", linestyle="--")
plt.axvline(K, color="0.5")
plt.xlabel("Number of independent factors")
plt.ylabel("Share of variance explained")
plt.show()
