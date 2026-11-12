# A bunch of hoops: checks that false findings pass easily.
import numpy as np
import matplotlib.pyplot as plt

pi_true = 0.4  # share of findings that are true
gaming = 0.85  # how easily false findings pass each hoop
rng = np.random.default_rng(93)

real = rng.uniform(size=2000) < pi_true


def passes(p_true, p_false):
    return rng.uniform(size=2000) < np.where(real, p_true, p_false)


hoops = passes(0.95, gaming) & passes(0.95, gaming) & passes(0.95, gaming)
substantive = passes(0.8, 0.15)  # e.g. a replication

print(f"True among findings that pass the hoops: "
      f"{100 * real[hoops].mean():.0f}% (base rate {100 * pi_true:.0f}%)")
print(f"True among findings that pass the substantive check: "
      f"{100 * real[substantive].mean():.0f}%")

x = np.arange(2)
plt.bar(x - 0.2, [hoops[real].mean(), substantive[real].mean()], 0.4,
        color="#2166ac", label="True findings")
plt.bar(x + 0.2, [hoops[~real].mean(), substantive[~real].mean()], 0.4,
        color="#d6604d", label="False findings")
plt.xticks(x, ["Hoops", "Substantive check"])
plt.ylabel("Share that pass")
plt.legend()
plt.show()
