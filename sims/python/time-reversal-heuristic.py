# The Time-Reversal Heuristic: what if the big replication had come first?
import numpy as np
import matplotlib.pyplot as plt

n_orig = 20   # original study n per group
n_rep = 800   # replication n per group
anchor = 8    # how much the anchored reader over-weights the original
rng = np.random.default_rng(57)

theta = 0.05
se1, se2 = np.sqrt(2 / n_orig), np.sqrt(2 / n_rep)
est1 = rng.normal(theta, se1)
while est1 < 1.96 * se1:                # the famous significant original
    est1 = rng.normal(theta, se1)
est2 = rng.normal(theta, se2)


def combine(wa=1):
    return ((wa * est1 / se1 ** 2 + est2 / se2 ** 2)
            / (wa / se1 ** 2 + 1 / se2 ** 2))


est = {"Original": est1, "Replication": est2,
       "Combined (either order)": combine(),
       "Anchored on the original": combine(anchor)}
for k, v in est.items():
    print(f"{k}: {v:.3f}")
print(f"Truth: {theta}")

plt.errorbar([est1, est2], [3, 2], xerr=[1.96 * se1, 1.96 * se2], fmt="o",
             color="black")
plt.scatter([est["Combined (either order)"],
             est["Anchored on the original"]], [1, 0], color="#2166ac")
plt.yticks([3, 2, 1, 0], list(est))
plt.axvline(theta, color="black", linestyle="--")
plt.xlabel("Estimate")
plt.tight_layout()
plt.show()
