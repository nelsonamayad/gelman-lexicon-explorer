# The Superplot: rich people vote Republican, rich states vote Democratic.
import numpy as np
import matplotlib.pyplot as plt

state_shift = 0.9  # state-wealth effect (toward Democrats)
within = 0.35      # within-state income slope
rng = np.random.default_rng(3)


def inv_logit(v):
    return 1 / (1 + np.exp(-v))


names = ["Poor states", "Middle states", "Rich states"]
centers = np.array([2.2, 3, 3.8])
alpha = np.array([0, -state_shift / 2, -state_shift])
g = np.repeat([0, 1, 2], 3000)
inc = np.clip(np.round(rng.normal(centers[g], 1)), 1, 5)  # categories
vote = rng.binomial(1, inv_logit(alpha[g] + within * (inc - 3)))  # Rep.

avg_inc = np.array([inc[g == k].mean() for k in range(3)])
avg_vote = np.array([vote[g == k].mean() for k in range(3)])
between = np.polyfit(avg_inc, avg_vote, 1)[0]
print("Within each kind of state, richer people vote more Republican.")
print(f"Across state averages, the slope is {between:.3f} per income "
      "category")

x = np.arange(1, 6)
for k, c in enumerate(["#d6604d", "0.5", "#2166ac"]):
    plt.plot(x, inv_logit(alpha[k] + within * (x - 3)), color=c,
             linewidth=2, label=names[k])
    plt.scatter(avg_inc[k], avg_vote[k], s=80, color=c)
plt.plot(avg_inc, avg_vote, "k--")
plt.ylim(0, 1)
plt.xlabel("Income category")
plt.ylabel("Share voting Republican")
plt.legend()
plt.show()
