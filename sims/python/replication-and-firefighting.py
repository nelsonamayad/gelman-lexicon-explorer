# Replication and firefighting: suppressing small fires feeds a big one.
import numpy as np
import matplotlib.pyplot as plt

suppression = 0.85  # suppression of routine criticism
rng = np.random.default_rng(139)

crisis_year = rng.integers(30, 56)  # when the crisis comes


def run(sup):
    fuel, path, burned = 10, [], 0
    for t in range(61):
        if t == crisis_year:
            burned, fuel = fuel, 0
        path.append(fuel)
        fuel = fuel + 20 - fuel * 0.25 * (1 - sup)  # criticism burns 25%/yr
    return path, burned


yours, burned_yours = run(suppression)
none, burned_none = run(0)
print(f"Crisis in year {crisis_year}: it burns {burned_yours:.0f} units of "
      f"unexamined work with your suppression level, {burned_none:.0f} "
      "with none")

plt.plot(yours, color="#d6604d", linewidth=2,
         label="Your suppression level")
plt.plot(none, color="#2166ac", linewidth=2,
         label="No suppression (controlled burns)")
plt.axvline(crisis_year, color="black", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Unexamined work (fuel)")
plt.legend()
plt.show()
