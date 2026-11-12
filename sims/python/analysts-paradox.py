# The Analyst's Paradox: 29 teams, one dataset, different choices.
import numpy as np
import matplotlib.pyplot as plt

choice_impact = 0.12  # how much each analytic choice moves the estimate
rng = np.random.default_rng(127)

se, base = 0.1, 0.3
shifts = rng.normal(0, choice_impact, (4, 3))  # 4 choices x 3 options
picks = rng.integers(0, 3, (29, 4))            # one option per choice
est = base + shifts[np.arange(4), picks].sum(axis=1) + rng.normal(0, 0.02, 29)
est = np.sort(est)

print(f"Estimates range from {est.min():.2f} to {est.max():.2f} "
      f"(sd across teams {est.std(ddof=1):.2f})")
print(f"Each team's own standard error: {se}")
print(f"Teams finding a significant positive effect: "
      f"{(est - 1.96 * se > 0).sum()} of 29")

teams = np.arange(1, 30)
plt.errorbar(teams, est, yerr=1.96 * se, fmt="o", color="#2166ac")
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Team (sorted by estimate)")
plt.ylabel("Estimate with the team's own 95% interval")
plt.show()
