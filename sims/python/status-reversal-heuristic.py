# The Status-Reversal Heuristic: would you believe it from a low-status
# source?
import numpy as np
import matplotlib.pyplot as plt

bonus = 1.2  # status bonus (log-odds)
rng = np.random.default_rng(58)


def inv_logit(v):
    return 1 / (1 + np.exp(-v))


high = np.arange(4000) % 2 == 0
evidence = rng.normal(0, 1.5, 4000)                  # what the paper shows
correct = rng.uniform(size=4000) < inv_logit(evidence)  # calibrated truth
judged = inv_logit(evidence + np.where(high, bonus / 2, -bonus / 2))
for name, g in [("High-status source", high), ("Low-status source", ~high)]:
    print(f"{name}: confidence {100 * judged[g].mean():.0f}%, accuracy "
          f"{100 * correct[g].mean():.0f}%")

plt.plot([0, 1], [0, 1], "k--")
bins = np.digitize(judged, np.arange(0.1, 1, 0.1))
for name, g, c in [("High-status source", high, "#d6604d"),
                   ("Low-status source", ~high, "#2166ac")]:
    xs = [judged[g & (bins == b)].mean() for b in range(10)
          if np.sum(g & (bins == b)) > 20]
    ys = [correct[g & (bins == b)].mean() for b in range(10)
          if np.sum(g & (bins == b)) > 20]
    plt.plot(xs, ys, "o-", color=c, label=name)
plt.xlabel("Judged probability")
plt.ylabel("Share actually correct")
plt.legend()
plt.show()
