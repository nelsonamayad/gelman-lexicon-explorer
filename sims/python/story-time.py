# Story Time: a subgroup "finding" when every true effect is zero.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

n_per = 60  # people per arm per subgroup
rng = np.random.default_rng(25)

subgroups = ["Young men", "Young women", "Older men", "Older women",
             "Urban", "Rural", "Low income", "High income", "College",
             "No college"]
res = []
for g in subgroups:
    t, c = rng.normal(size=n_per), rng.normal(size=n_per)  # no effect
    est = t.mean() - c.mean()
    se = np.sqrt(t.var(ddof=1) / n_per + c.var(ddof=1) / n_per)
    p = 2 * (1 - NormalDist().cdf(abs(est / se)))  # normal approximation
    res.append((g, est, p))
res.sort(key=lambda r: -r[1])
for g, est, p in res:
    print(f"{g:12s} estimate {est:6.3f}  p = {p:.3f}")
phrase = {"Urban": "urban residents", "Rural": "rural residents",
          "Low income": "people with low incomes",
          "High income": "people with high incomes",
          "College": "college graduates",
          "No college": "people without a college degree"}
who = phrase.get(res[0][0], res[0][0].lower())
print(f'Tonight\'s story: "The program was especially effective for '
      f'{who}" (p = {res[0][2]:.3f})')

y = np.arange(10)[::-1]
plt.scatter([r[1] for r in res], y,
            c=["#d6604d" if r[2] < 0.05 else "0.25" for r in res])
plt.yticks(y, [r[0] for r in res])
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("Estimated effect (true effect: 0)")
plt.tight_layout()
plt.show()
