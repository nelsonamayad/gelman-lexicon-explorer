# Freedom: it's not user friendly.
import numpy as np
import matplotlib.pyplot as plt

skill = 0.5  # average analyst skill
rng = np.random.default_rng(102)

s = np.clip(rng.normal(skill, 0.2, 2000), 0, 1)          # each analyst
constrained = 0.65 + rng.normal(0, 0.05, 2000)  # good defaults, low ceiling
free = np.maximum(-0.5, 0.95 - (1 - s) * np.abs(rng.normal(0, 0.6, 2000)))

for name, q in [("Constrained", constrained), ("Free", free)]:
    print(f"{name}: median quality {np.median(q):.2f}, "
          f"worst 10% {np.quantile(q, 0.1):.2f}")

plt.boxplot([constrained, free], patch_artist=True)
plt.xticks([1, 2], ["Constrained, user-friendly", "Free, flexible"])
plt.ylabel("Quality of the analysis")
plt.show()
