# Looking for a needle in a pile of needles: a placebo test.
import numpy as np
import matplotlib.pyplot as plt

beta = 0.05     # true effect of the intervention
confound = 0.6  # correlation of the intervention with background growth
rng = np.random.default_rng(88)


def slope(x, y):
    return np.polyfit(x, y, 1)[0]


# 500 replications of a 43-city study
placebo, claimed = [], []
for _ in range(500):
    g = rng.normal(size=43)               # background growth of each city
    x = confound * g + np.sqrt(1 - confound ** 2) * rng.normal(size=43)
    pre = g + rng.normal(0, 0.5, 43)      # growth before 1918
    post = g + beta * x + rng.normal(0, 0.5, 43)  # growth after 1918
    placebo.append(slope(x, pre))
    claimed.append(slope(x, post))
print(f"Average estimate: claimed effect {np.mean(claimed):.2f}, placebo "
      f"(before 1918) {np.mean(placebo):.2f}, true effect {beta}")

plt.boxplot([placebo, claimed])
plt.xticks([1, 2], ["Placebo: before 1918", "Claimed: after 1918"])
plt.axhline(beta, color="black", linestyle="--")
plt.ylabel("Estimated effect")
plt.show()
