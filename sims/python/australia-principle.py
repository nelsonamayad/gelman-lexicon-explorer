# The Australia principle: build the prior where the likelihood is weak.
import numpy as np
import matplotlib.pyplot as plt

n = 3000  # survey sample size
rng = np.random.default_rng(75)


def posterior(prior_mean, prior_sd, est, se):
    w0, w1 = 1 / prior_sd ** 2, 1 / se ** 2
    m, s = (w0 * prior_mean + w1 * est) / (w0 + w1), np.sqrt(1 / (w0 + w1))
    return 100 * m, 100 * (m - 1.96 * s), 100 * (m + 1.96 * s)


# Q1: an opinion proportion (truth 0.52); effects of interest ~5 points
se1 = 0.5 / np.sqrt(n)
est1 = 0.52 + rng.normal(0, se1)
# Q2: difference in Pr(girl) between two groups (truth 0.002)
se2 = np.sqrt(2 * 0.25 / (n / 2))
est2 = 0.002 + rng.normal(0, se2)

res = {"Q1": [posterior(0.5, 1, est1, se1), posterior(0.5, 0.05, est1, se1)],
       "Q2": [posterior(0, 1, est2, se2), posterior(0, 0.003, est2, se2)]}
for q, rows in res.items():
    for label, (m, lo, hi) in zip(["vague", "informative"], rows):
        print(f"{q}, {label} prior: {m:.2f} [{lo:.2f}, {hi:.2f}] points")
print(f"Q2 standard error: {100 * se2:.2f} points, "
      "against a true effect of 0.2 points")

fig, axes = plt.subplots(2, 1, figsize=(6, 4))
for ax, (q, rows), truth in zip(axes, res.items(), [52, 0.2]):
    for y, ((m, lo, hi), col) in enumerate(zip(rows,
                                               ["#d6604d", "#2166ac"])):
        ax.plot([lo, hi], [y, y], color=col, linewidth=3)
        ax.plot(m, y, "o", color="black")
    ax.axvline(truth, color="black", linestyle="--")
    ax.set_yticks([0, 1], ["Vague prior", "Informative prior"])
    ax.set_ylim(-0.5, 1.5)
    ax.set_title(q)
axes[1].set_xlabel("Percentage points")
plt.tight_layout()
plt.show()
