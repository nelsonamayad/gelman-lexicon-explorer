# The worst visual display of all time: the Stroop test in black and white.
import numpy as np
import matplotlib.pyplot as plt

bw = False  # print in black and white?
rng = np.random.default_rng(109)


# Reaction times (ms). Ink that conflicts with the word slows reading,
# but only if the reader can see the colors.
def trial(incongruent):
    base = rng.lognormal(np.log(600), 0.15, 400)
    return base + (rng.normal(120, 40, 400) if incongruent and not bw else 0)


congruent, incongruent = trial(False), trial(True)
print(f"Interference effect (incongruent minus congruent): "
      f"{incongruent.mean() - congruent.mean():.0f} ms")

plt.boxplot([congruent, incongruent])
plt.xticks([1, 2], ["Congruent", "Incongruent"])
plt.ylabel("Reaction time (ms)")
plt.show()
