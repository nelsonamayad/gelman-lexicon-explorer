# The wedding, never about the marriage: corrections get little attention.
import numpy as np
import matplotlib.pyplot as plt

delay = 24     # months until the error is found
loudness = 0.08  # correction attention relative to the original
half_life = 6  # attention half-life (months)
# Deterministic: no random numbers.

t = np.arange(121)
lam = np.log(2) / half_life
wedding = 100 * np.exp(-lam * t)                       # the publication
marriage = np.where(t >= delay,
                    100 * loudness * np.exp(-lam * (t - delay)), 0)
print(f"The correction gets {100 * marriage.sum() / wedding.sum():.1f}% as "
      "much attention as the original")
print(f"By the time the error is found, "
      f"{100 * (1 - np.exp(-lam * delay)):.0f}% of the paper's attention "
      "is already spent")

plt.plot(t, wedding, color="#2166ac", linewidth=2,
         label="Original publication")
plt.plot(t, marriage, color="#d6604d", linewidth=2, label="Correction")
plt.xlabel("Months since publication")
plt.ylabel("Attention")
plt.legend()
plt.show()
