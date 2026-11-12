# Assumptions and Rigor: difference-in-differences without parallel trends.
import numpy as np
import matplotlib.pyplot as plt

delta = 0.4  # violation of parallel trends
n = 100      # units per group
rng = np.random.default_rng(86)

est, lo, hi = [], [], []
for _ in range(300):
    c_pre, c_post = rng.normal(0, 1, n), rng.normal(0.5, 1, n)  # control
    t_pre = rng.normal(0.3, 1, n)
    t_post = rng.normal(0.3 + 0.5 + delta + 1, 1, n)
    e = (t_post.mean() - t_pre.mean()) - (c_post.mean() - c_pre.mean())
    se = np.sqrt((t_post.var(ddof=1) + t_pre.var(ddof=1) + c_post.var(ddof=1)
                  + c_pre.var(ddof=1)) / n)
    est.append(e); lo.append(e - 1.96 * se); hi.append(e + 1.96 * se)
est, lo, hi = map(np.array, (est, lo, hi))
covered = (lo <= 1) & (hi >= 1)  # the true effect is 1

print(f"Coverage of the nominal 95% interval: {100 * covered.mean():.1f}%")
print(f"Average estimate: {est.mean():.2f} (true effect: 1)")

k = np.arange(50)
plt.vlines(k, lo[:50], hi[:50],
           colors=np.where(covered[:50], "#2166ac", "#d6604d"))
plt.plot(k, est[:50], "o", color="black", markersize=3)
plt.axhline(1, color="black", linestyle="--")
plt.xlabel("Replication")
plt.ylabel("Estimate with 95% interval")
plt.show()
