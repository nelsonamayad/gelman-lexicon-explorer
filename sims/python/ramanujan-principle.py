# The Ramanujan Principle: partition numbers and the Hardy-Ramanujan formula.
import math
import matplotlib.pyplot as plt

n_max = 100  # largest n
# Deterministic: no random numbers. Python integers are exact.

# Euler's pentagonal-number recurrence for p(n), the number of partitions
p = [1]
for n in range(1, 201):
    s, k = 0, 1
    while k * (3 * k - 1) // 2 <= n:
        sign = 1 if k % 2 else -1
        g1, g2 = k * (3 * k - 1) // 2, k * (3 * k + 1) // 2
        s += sign * p[n - g1]
        if g2 <= n:
            s += sign * p[n - g2]
        k += 1
    p.append(s)


def asymptotic(n):
    return math.exp(math.pi * math.sqrt(2 * n / 3)) / (4 * n * math.sqrt(3))


for n in range(10, n_max + 1, 10):
    print(f"p({n}) = {p[n]:,}")
print(f"Formula / exact at n = {n_max}: "
      f"{asymptotic(n_max) / p[n_max]:.3f}")

ns = range(1, n_max + 1)
plt.plot(ns, [math.log10(p[n]) for n in ns], color="#2166ac", linewidth=2,
         label="Exact")
plt.plot(ns, [math.log10(asymptotic(n)) for n in ns], "--",
         color="#d6604d", linewidth=2, label="Hardy-Ramanujan formula")
plt.xlabel("n")
plt.ylabel("log10 p(n)")
plt.legend()
plt.show()
