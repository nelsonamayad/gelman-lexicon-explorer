# God is in every leaf of every tree: missing answers coded as 99.
import numpy as np
import matplotlib.pyplot as plt

miss_rate = 0.04        # share of responses missing
missing_related = True  # missingness more common among older respondents
rng = np.random.default_rng(27)

age = rng.uniform(18, 80, 1000)
rating = np.clip(np.round(6 - 0.03 * (age - 50) + rng.normal(0, 1.8, 1000)),
                 1, 10)
p_miss = miss_rate * 2 * (age - 18) / 62 if missing_related else miss_rate
missing = rng.uniform(size=1000) < p_miss
recorded = np.where(missing, 99, rating)  # the "trivial" coding detail

print(f"Mean rating: 99 treated as a number {recorded.mean():.2f} "
      f"| missing code dropped {rating[~missing].mean():.2f}")
print(f"Slope on age: {np.polyfit(age, recorded, 1)[0]:.3f} vs "
      f"{np.polyfit(age[~missing], rating[~missing], 1)[0]:.3f}")

plt.scatter(age, recorded, s=6, c=np.where(missing, "#d6604d", "#2166ac"))
plt.yscale("log")
plt.xlabel("Age")
plt.ylabel("Recorded rating (log scale)")
plt.show()
