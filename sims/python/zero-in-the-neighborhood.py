# If zero is in the neighborhood, invite it in.
import numpy as np
import matplotlib.pyplot as plt

level = 5  # typical level of the series
rng = np.random.default_rng(100)

v = level + np.cumsum(rng.normal(0.15, 0.6, 24))  # a series, 24 periods
lo, hi = v.min(), v.max()
invite = lo <= 0 or lo < 1.5 * (hi - lo)  # is zero in the neighborhood?
print(f"The data range from {lo:.1f} to {hi:.1f}: "
      + ("zero is in the neighborhood, so include it" if invite
         else "zero is far away, so keep the zoomed axis"))

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
for a, title in zip(ax, ["Zoomed axis", "Axis including zero"]):
    a.plot(np.arange(1, 25), v, "o-", color="#2166ac")
    a.set_title(title)
    a.set_xlabel("Period")
ax[1].set_ylim(min(0, lo), hi * 1.05)
plt.show()
