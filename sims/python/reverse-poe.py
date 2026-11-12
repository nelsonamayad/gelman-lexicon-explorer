# Reverse Poe: sincere work so absurd that readers take it for parody.
import numpy as np
import matplotlib.pyplot as plt

tail = 0.08     # share of sincere papers with absurd claims
threshold = 3   # reader's "must be a joke" threshold
rng = np.random.default_rng(63)

# Absurdity score of 2000 sincere papers and 300 parodies
sincere = np.where(rng.uniform(size=2000) < tail, rng.normal(4, 0.8, 2000),
                   rng.normal(1, 0.8, 2000))
parody = rng.normal(4.2, 0.8, 300)
rp, pp = np.sum(sincere > threshold), np.sum(parody > threshold)
print(f"{rp + pp} texts look like jokes; {rp} of them "
      f"({100 * rp / (rp + pp):.0f}%) are sincere")

bins = np.arange(-3, 8.01, 0.25)
plt.hist(sincere, bins=bins, color="#2166ac", alpha=0.6, label="Sincere")
plt.hist(parody, bins=bins, color="#d6604d", alpha=0.6, label="Parody")
plt.axvline(threshold, color="black", linestyle="--")
plt.xlabel("Absurdity score")
plt.ylabel("Texts")
plt.legend()
plt.show()
