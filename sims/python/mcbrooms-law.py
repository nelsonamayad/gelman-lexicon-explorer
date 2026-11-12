# McBroom's Law: sources that never correct their errors lose credibility.
import numpy as np
import matplotlib.pyplot as plt

n_errors = 4             # number of falsehoods exposed
p_fix_reliable = 0.8     # chance a reliable source corrects an error
p_fix_unreliable = 0.3   # chance an unreliable source corrects an error
# Deterministic: no random numbers. A reader starts 80% sure the source is
# reliable; an exposed error is 3 times likelier from an unreliable source.

lr_error = np.log(0.1 / 0.3)
lr_fix = np.log(p_fix_reliable / p_fix_unreliable)
lr_no_fix = np.log((1 - p_fix_reliable) / (1 - p_fix_unreliable))
k = np.arange(n_errors + 1)
corrects = 1 / (1 + np.exp(-(np.log(4) + k * (lr_error + lr_fix))))
never = 1 / (1 + np.exp(-(np.log(4) + k * (lr_error + lr_no_fix))))

print(f"Belief the source is reliable after {n_errors} exposed errors: "
      f"corrects {100 * corrects[-1]:.0f}% | never corrects "
      f"{100 * never[-1]:.0f}%")

plt.plot(k, corrects, "o-", color="#2166ac", label="Takes accountability")
plt.plot(k, never, "o-", color="#d6604d", label="Never takes accountability")
plt.ylim(0, 1)
plt.xlabel("Falsehoods exposed")
plt.ylabel("Belief the source is reliable")
plt.legend()
plt.show()
