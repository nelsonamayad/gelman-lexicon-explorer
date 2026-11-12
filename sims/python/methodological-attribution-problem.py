# The Methodological Attribution Problem: credit the analyst, not the method.
import numpy as np
import matplotlib.pyplot as plt

method_effect = 0.1  # true effect of the fancy method
selection = 2        # how strongly skill predicts using it
rng = np.random.default_rng(40)

skill = rng.normal(size=1000)
uses = rng.binomial(1, 1 / (1 + np.exp(-selection * skill)))
quality = method_effect * uses + skill + rng.normal(0, 0.5, 1000)

naive = quality[uses == 1].mean() - quality[uses == 0].mean()
X = np.column_stack([np.ones(1000), uses, skill])
adjusted = np.linalg.lstsq(X, quality, rcond=None)[0][1]
print(f"Naive credit to the method: {naive:.2f}")
print(f"Adjusted for skill: {adjusted:.2f} (true effect {method_effect})")

plt.boxplot([quality[uses == 0], quality[uses == 1]], patch_artist=True)
plt.xticks([1, 2], ["Standard method", "Fancy method"])
plt.ylabel("Quality of the analysis")
plt.show()
