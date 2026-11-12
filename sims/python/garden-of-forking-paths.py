# The Garden of Forking Paths: one test, chosen by looking at the data.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

n = 100  # participants per arm
rng = np.random.default_rng(44)
N = NormalDist()


def p_value(a, b):
    """Two-sample test (normal approximation)."""
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return 2 * N.cdf(-abs(a.mean() - b.mean()) / se)


def trim(a):
    return a[np.abs(a - a.mean()) < 2.5 * a.std(ddof=1)]


def diff(a, b):
    return abs(a.mean() - b.mean())


def make():
    """Heavy-ish tails, so outliers occur; the true effect is zero."""
    y1 = rng.standard_t(5, n)
    y2 = 0.5 * y1 + np.sqrt(0.75) * rng.standard_t(5, n)
    return {"y1": y1, "y2": y2, "sex": rng.binomial(1, 0.5, n)}


def pick(D, grp, out):
    return D[out] if grp == "all" else D[out][D["sex"] == grp]


pre = forked = fished = 0
for _ in range(1000):
    T, C = make(), make()
    # 1. Preregistered: always the same test
    pre += p_value(T["y1"], C["y1"]) < 0.05
    # 2. Forking paths: three choices made by looking at the data
    out = "y2" if diff(T["y2"], C["y2"]) > diff(T["y1"], C["y1"]) else "y1"
    d0 = diff(pick(T, 0, out), pick(C, 0, out))
    d1 = diff(pick(T, 1, out), pick(C, 1, out))
    grp = 1 if d1 > 2 * d0 else 0 if d0 > 2 * d1 else "all"
    a, b = pick(T, grp, out), pick(C, grp, out)
    if diff(trim(a), trim(b)) > diff(a, b):
        a, b = trim(a), trim(b)
    forked += p_value(a, b) < 0.05
    # 3. Fishing: test all 12 paths and report the smallest p-value
    ps = []
    for o in ("y1", "y2"):
        for tr in (False, True):
            for g in ("all", 0, 1):
                a, b = pick(T, g, o), pick(C, g, o)
                if tr:
                    a, b = trim(a), trim(b)
                ps.append(p_value(a, b))
    fished += min(ps) < 0.05

rates = {"Preregistered": pre / 1000, "Forking paths": forked / 1000,
         "Fishing (best of 12)": fished / 1000}
for k, v in rates.items():
    print(f"{k}: {100 * v:.1f}% false positives (true effect zero)")

plt.bar(list(rates), list(rates.values()),
        color=["0.6", "#d6604d", "#67001f"])
plt.axhline(0.05, color="black", linestyle="--")
plt.ylim(0, 0.5)
plt.ylabel("False-positive rate (true effect is zero)")
plt.show()
