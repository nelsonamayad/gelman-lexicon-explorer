# The Taxonomy of Confusion: which questions still reach the TA?
import numpy as np
import matplotlib.pyplot as plt

help_scale = 1  # how well the self-help steps work (1 = baseline)
rng = np.random.default_rng(19)

kinds = ["1. Prerequisite statistics", "2. Course statistics",
         "3. Don't know the function's name",
         "4. Don't know how the function works",
         "5. Code gives an error", "6. Code runs but is wrong"]
share = np.array([0.15, 0.25, 0.15, 0.15, 0.18, 0.12])
self_help = np.array([0.8, 0.6, 0.85, 0.75, 0.6, 0.35])
q = rng.choice(6, 300, p=share)                      # a semester
solved = rng.uniform(size=300) < np.minimum(1, self_help[q] * help_scale)
asked = np.bincount(q, minlength=6)
reach = np.bincount(q[~solved], minlength=6)
for k, a, r in zip(kinds, asked, reach):
    print(f"{k}: {a} asked, {r} reach the TA")
print(f"{reach.sum()} of 300 questions reach the TA")

y = np.arange(6)[::-1]
plt.barh(y + 0.2, asked, 0.4, color="0.8", label="Asked")
plt.barh(y - 0.2, reach, 0.4, color="#d6604d", label="Reach the TA")
plt.yticks(y, kinds)
plt.xlabel("Questions in a semester")
plt.legend()
plt.tight_layout()
plt.show()
