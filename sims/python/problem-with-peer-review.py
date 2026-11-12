# The problem with peer review: more reviewers don't catch shared errors.
import numpy as np
import matplotlib.pyplot as plt

p_catch = 0.5  # reviewer skill: chance of catching an error they see
m = 0.85       # share of the field sharing the misconception
rng = np.random.default_rng(61)

reviewers = [1, 2, 3, 4, 5, 6, 8, 10]
caught = {"Idiosyncratic error": [], "Shared misconception": []}
for k in reviewers:
    for kind, shared in [("Idiosyncratic error", False),
                         ("Shared misconception", True)]:
        blind = shared & (rng.uniform(size=(2000, k)) < m)
        hit = (~blind & (rng.uniform(size=(2000, k)) < p_catch)).any(axis=1)
        caught[kind].append(hit.mean())
print(f"With 10 reviewers: an idiosyncratic error is caught "
      f"{100 * caught['Idiosyncratic error'][-1]:.0f}% of the time, "
      f"a shared misconception "
      f"{100 * caught['Shared misconception'][-1]:.0f}%")

for (kind, v), c in zip(caught.items(), ["#2166ac", "#d6604d"]):
    plt.plot(reviewers, v, "o-", color=c, label=kind)
plt.ylim(0, 1)
plt.xlabel("Number of reviewers")
plt.ylabel("Share of errors caught")
plt.legend()
plt.show()
