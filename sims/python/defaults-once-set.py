# Defaults, once set, are hard to change: adoption with switching costs.
import numpy as np
import matplotlib.pyplot as plt

gap = 0.3   # quality advantage of the new method
cost = 1.1  # individual switching cost
coord = 1   # coordination benefit (grows with the share who switched)
rng = np.random.default_rng(39)

N = 1000
switched = rng.uniform(size=N) < 0.02  # a few early adopters
share = []
for t in range(61):
    share.append(switched.mean())
    tempted = gap + coord * switched.mean() - cost + rng.normal(0, 0.3, N) > 0
    switched = switched | (tempted & (rng.uniform(size=N) < 0.3))
share = np.array(share)
half = np.flatnonzero(share >= 0.5)

if half.size:
    print(f"Half the field switches after {half[0]} years")
else:
    print("Never reaches half adoption within 60 years")
print(f"Final share: {100 * share[-1]:.0f}%")

plt.plot(range(61), share, color="#2166ac", linewidth=2)
plt.axhline(0.5, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("Years after the better method appears")
plt.ylabel("Share using the new method")
plt.show()
