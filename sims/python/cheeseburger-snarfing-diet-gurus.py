# Cheeseburger-snarfing diet gurus: evaluating teaching by ratings.
import numpy as np
import matplotlib.pyplot as plt

learn_effect = 0.05  # true effect on learning (sd units)
enthusiasm = 0.8     # novelty/enthusiasm boost to ratings
rng = np.random.default_rng(91)

treated, gain, rating = [], [], []
for k in range(20):
    t = k % 2 == 0
    inst = rng.normal(0, 0.3)  # instructor effect
    pre = rng.normal(size=40)
    post = 0.6 * pre + inst + t * learn_effect + rng.normal(0, 0.8, 40)
    rate = 3.5 + inst + t * enthusiasm * 0.5 + rng.normal(0, 0.6, 40)
    treated.append(t)
    gain.append(np.mean(post - 0.6 * pre))
    rating.append(rate.mean())
treated, gain, rating = map(np.array, (treated, gain, rating))


def compare(v):
    a, b = v[treated], v[~treated]
    se = np.sqrt(a.var(ddof=1) / 10 + b.var(ddof=1) / 10)
    return a.mean() - b.mean(), se


r_diff, r_se = compare(rating)
l_diff, l_se = compare(gain)
print(f"Ratings up by {r_diff:.2f} points (se {r_se:.2f})")
print(f"Effect on learning: {l_diff:.2f} sd (se {l_se:.2f}); "
      f"true effect {learn_effect}")

plt.scatter(gain[treated], rating[treated], color="#d6604d",
            label="New method")
plt.scatter(gain[~treated], rating[~treated], color="#2166ac",
            label="Old method")
plt.xlabel("Learning gain (section average)")
plt.ylabel("Student rating (section average)")
plt.legend()
plt.show()
