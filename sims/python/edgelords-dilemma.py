# The Edgelord's Dilemma: who stands near you far from the consensus?
import numpy as np
import matplotlib.pyplot as plt

my_pos = 2.2      # your distance from consensus (sd units)
bad_share = 0.05  # bad-faith actors as a share of everyone
rng = np.random.default_rng(148)

N = 10000
n_bad = round(N * bad_share)
careful = rng.normal(size=N - n_bad)                    # careful thinkers
bad = rng.choice([-1, 1], n_bad) * rng.normal(3, 0.7, n_bad)
near_careful = np.sum(np.abs(careful - my_pos) < 0.25)
near_bad = np.sum(np.abs(bad - my_pos) < 0.25)

share = near_bad / (near_bad + near_careful)
print(f"Near you: {near_bad} bad-faith actors and {near_careful} careful "
      f"thinkers ({100 * share:.0f}% bad faith)")

bins = np.arange(-7, 7.01, 0.25)
plt.hist([careful, bad], bins=bins, stacked=True,
         color=["#2166ac", "#d6604d"],
         label=["Careful thinkers", "Bad-faith actors"])
plt.axvline(my_pos, color="black", linestyle="--")
plt.xlabel("Position (sd units from consensus)")
plt.ylabel("People")
plt.legend()
plt.show()
