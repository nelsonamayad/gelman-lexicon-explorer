# Anthropic principle: which effects can statistics study at all?
import numpy as np
import matplotlib.pyplot as plt

n_max = 3     # log10 of the largest feasible sample size
obvious = 2   # naked-eye threshold (effect in sd units)
rng = np.random.default_rng(119)

detect = 2.8 / np.sqrt(10 ** n_max)  # detectable with ~80% power
eff = 10 ** rng.uniform(-4, 1, 4000)  # effects over five orders of magnitude
zones = {"Too small to detect": eff < detect,
         "Statistics territory": (eff >= detect) & (eff <= obvious),
         "Obvious without statistics": eff > obvious}
for name, inside in zones.items():
    print(f"{name}: {100 * inside.mean():.0f}%")

bins = np.linspace(-4, 1, 51)
colors = ["0.7", "#2166ac", "#d6604d"]
plt.hist([np.log10(eff[m]) for m in zones.values()], bins=bins,
         stacked=True, color=colors, label=list(zones))
plt.xlabel("True effect size (sd units, log10 scale)")
plt.ylabel("Phenomena")
plt.legend()
plt.show()
