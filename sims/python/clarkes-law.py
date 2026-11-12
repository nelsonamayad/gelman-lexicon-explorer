# Clarke's Law: the GRIM test can't tell crappy research from fraud.
import numpy as np
import matplotlib.pyplot as plt

error_rate = 0.4  # sloppiness: probability a reported mean has an error
rng = np.random.default_rng(59)


def grim_ok(m, n):
    """Can n integers have a mean that rounds to m (2 decimals)?"""
    k = round(m * n)
    return any(f"{round(s / n, 2):.2f}" == f"{m:.2f}"
               for s in (k - 1, k, k + 1))


def report(kind):
    ok = []
    for _ in range(2000):
        n = int(rng.integers(10, 41))
        m = round(rng.integers(1, 8, n).mean(), 2)  # a 1-7 rating scale
        if kind == "Sloppy" and rng.uniform() < error_rate:
            m = round(m + rng.choice([-1, 1]) * rng.integers(1, 10) / 100, 2)
        if kind == "Fabricated":
            m = round(rng.uniform(2, 6), 2)
        ok.append(grim_ok(m, n))
    return np.mean(ok)


kinds = ["Honest", "Sloppy", "Fabricated"]
fail = [1 - report(k) for k in kinds]
for k, f in zip(kinds, fail):
    print(f"{k}: {100 * f:.0f}% fail the GRIM test")

plt.bar(kinds, fail, color=["#2166ac", "#b8860b", "#d6604d"])
plt.ylim(0, 1)
plt.ylabel("Share of means that fail the GRIM test")
plt.show()
