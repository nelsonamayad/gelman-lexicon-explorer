# The Foxhole Fallacy: selective memory turns two-way traffic one-way.
import numpy as np
import matplotlib.pyplot as plt

to_mine = 0.05     # true rate of switching to my method
from_mine = 0.05   # true rate of switching away
memory_bias = 0.8  # memory selectivity
rng = np.random.default_rng(30)

# 500 practitioners use my method and 500 don't
to = rng.uniform(size=500) < to_mine
away = rng.uniform(size=500) < from_mine
to_remembered = to & (rng.uniform(size=500) < 0.5 + memory_bias / 2)
away_remembered = away & (rng.uniform(size=500) < 0.5 - memory_bias / 2)

print(f"Actually happened: {to.sum()} switched to my side, "
      f"{away.sum()} switched away")
print(f"What I remember: {to_remembered.sum()} switched to my side, "
      f"{away_remembered.sum()} switched away")

x = np.arange(2)
plt.bar(x - 0.2, [to.sum(), to_remembered.sum()], 0.4, color="#2166ac",
        label="Switched to my side")
plt.bar(x + 0.2, [away.sum(), away_remembered.sum()], 0.4, color="#d6604d",
        label="Switched away")
plt.xticks(x, ["Actually happened", "What I remember"])
plt.ylabel("Practitioners")
plt.legend()
plt.show()
