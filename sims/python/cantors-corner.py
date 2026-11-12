# Cantor's Corner: find the statistic your model can't reproduce.
import numpy as np
import matplotlib.pyplot as plt

zero_infl = 0.25  # share of structural zeros in the truth
rng = np.random.default_rng(69)

y = np.where(rng.uniform(size=300) < zero_infl, 0,
             rng.poisson(rng.gamma(4, 1, 300)))
lam = y.mean()  # fit a Poisson model
stats = {"Mean": np.mean, "Variance": lambda v: v.var(ddof=1),
         "Share of zeros": lambda v: np.mean(v == 0), "Maximum": np.max}
reps = rng.poisson(lam, (400, 300))  # 400 datasets from the fit

fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, (name, f) in zip(axes.flat, stats.items()):
    sim = np.array([f(r) for r in reps])
    obs = f(y)
    print(f"{name}: observed {obs:.3f}, simulated mean {sim.mean():.3f}, "
          f"p = {np.mean(sim >= obs):.3f}")
    ax.hist(sim, bins=20, color="0.8")
    ax.axvline(obs, color="#d6604d", linewidth=3)
    ax.set_title(name)
plt.tight_layout()
plt.show()
