# The Groovy Grandma Problem: weighting fixes the age mix, not grooviness.
import numpy as np
import matplotlib.pyplot as plt

groovy = 2.5  # how much grooviness boosts response among older people
rng = np.random.default_rng(149)

N = 60000
old = rng.binomial(1, 0.4, N)
g = rng.binomial(1, np.where(old == 1, 0.15, 0.5))  # "groovy"
support = rng.binomial(1, 0.35 + 0.3 * g - 0.1 * old)
logit = -3 + np.where(old == 1, -1 + groovy * g, 0.5 * g)
resp = rng.uniform(size=N) < 1 / (1 + np.exp(-logit))


def cell(o):
    return support[resp & (old == o)].mean()


weighted = 0.4 * cell(1) + 0.6 * cell(0)  # weighted to the census age mix
print(f"Groovy among older respondents: "
      f"{100 * g[resp & (old == 1)].mean():.0f}% (15% in the population)")
print(f"Truth: {100 * support.mean():.1f}% | weighted estimate: "
      f"{100 * weighted:.1f}%")

est = {"Truth": support.mean(), "Raw sample": support[resp].mean(),
       "Weighted by age": weighted}
plt.scatter([100 * v for v in est.values()], list(est), s=80,
            color=["black", "#d6604d", "#d6604d"])
plt.xlabel("Support (%)")
plt.tight_layout()
plt.show()
