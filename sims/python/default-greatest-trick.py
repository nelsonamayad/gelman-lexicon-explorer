# Default, the greatest trick it ever pulled: silently dropping missing data.
import numpy as np
import matplotlib.pyplot as plt

miss_strength = 1.5  # how strongly low income predicts skipping the question
rng = np.random.default_rng(38)

educ = rng.normal(size=2000)
income = 50 + 12 * educ + rng.normal(0, 10, 2000)
p_miss = 1 / (1 + np.exp(1.5 + miss_strength * (income - 50) / 12))
missing = rng.uniform(size=2000) < p_miss

slope, intercept = np.polyfit(educ[~missing], income[~missing], 1)
imputed = np.where(missing, intercept + slope * educ, income)

print(f"Skipped the question: {100 * missing.mean():.0f}%")
print(f"Truth: {income.mean():.1f} | drop missing rows (the default): "
      f"{income[~missing].mean():.1f} | impute from education: "
      f"{imputed.mean():.1f}")

est = {"Truth": income.mean(), "Drop missing rows": income[~missing].mean(),
       "Impute": imputed.mean()}
plt.scatter(list(est.values()), list(est), s=80,
            color=["black", "#d6604d", "#2166ac"])
plt.xlabel("Estimated average income")
plt.tight_layout()
plt.show()
