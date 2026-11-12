# What would you do if you had all the data? Choosing the estimand.
import numpy as np
import matplotlib.pyplot as plt

heterogeneity = 1.2  # variation in individual effects
self_select = 0.6    # do people who benefit more choose treatment?
rng = np.random.default_rng(55)

# Both potential outcomes, visible only in a simulation
y0 = rng.normal(size=3000)
effect = 0.3 + heterogeneity * rng.normal(size=3000)
y1 = y0 + effect
chooses = rng.uniform(size=3000) < 0.5 + self_select * np.tanh(effect) / 2
randomized = rng.uniform(size=3000) < 0.5

estimands = {"Average effect (everyone)": effect.mean(),
             "Effect on those who choose": effect[chooses].mean(),
             "Median individual effect": np.median(effect),
             "Share who benefit": np.mean(effect > 0)}
for k, v in estimands.items():
    print(f"{k}: {v:.2f}")
rct = y1[randomized].mean() - y0[~randomized].mean()
print(f"A randomized experiment estimates {rct:.2f} "
      "(it targets the average effect)")

plt.hist(effect, bins=50, color="#2166ac")
for v, c in zip(list(estimands.values())[:3],
                ["black", "#d6604d", "#b8860b"]):
    plt.axvline(v, color=c, linewidth=2)
plt.axvline(rct, color="black", linestyle="--")
plt.xlabel("Individual treatment effect")
plt.ylabel("People")
plt.show()
