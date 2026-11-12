# The Pinch-Hitter Syndrome: part-time players look worse than they are.
import numpy as np
import matplotlib.pyplot as plt

starter_share = 0.6   # share of players who start
cold_penalty = 0.015  # cold-start penalty on the batting average
rng = np.random.default_rng(8)

talent = np.sort(np.clip(rng.normal(0.26, 0.025, 400), 0.17, 0.36))[::-1]
starter = np.arange(400) < round(starter_share * 400)  # the best start
at_bats = np.where(starter, 500, 60)
p = np.where(starter, talent, talent - cold_penalty)
avg = rng.binomial(at_bats, p) / at_bats

for name, g in [("Starters", starter), ("Pinch hitters", ~starter)]:
    print(f"{name}: true talent {talent[g].mean():.3f}, observed average "
          f"{avg[g].mean():.3f}")

plt.scatter(talent[starter], avg[starter], s=8, color="#2166ac",
            label="Starter")
plt.scatter(talent[~starter], avg[~starter], s=8, color="#d6604d",
            label="Pinch hitter")
plt.plot([0.17, 0.36], [0.17, 0.36], "k--")
plt.xlabel("True talent")
plt.ylabel("Observed batting average")
plt.legend()
plt.show()
