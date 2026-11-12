# A chicken: Bill James's check of a fielding rating, in miniature.
import numpy as np
import matplotlib.pyplot as plt

adjust = False   # False: rate by raw assists; True: adjust for team
gb_effect = 0.8  # how much team ground balls drive assists
rng = np.random.default_rng(118)

gb = np.repeat(rng.normal(size=30), 2)  # team tendency, 2 fielders per team
skill = rng.normal(size=60)             # fielders' true skill
assists = 300 + 15 * skill + 40 * gb_effect * gb + rng.normal(0, 10, 60)
if adjust:
    slope, intercept = np.polyfit(gb, assists, 1)
    score = assists - (intercept + slope * gb)
else:
    score = assists
rating = (score - score.mean()) / score.std(ddof=1)

top10 = np.argsort(-rating)[:10]
cut = np.sort(gb)[::-1][19]  # top third of fielders by team
print(f"Top-10 fielders on ground-ball teams: {(gb[top10] >= cut).sum()}"
      " of 10")
print(f"Correlation with team ground balls: "
      f"{np.corrcoef(rating, gb)[0, 1]:.2f}")
print(f"Correlation with true skill: {np.corrcoef(rating, skill)[0, 1]:.2f}")

slope, intercept = np.polyfit(gb, rating, 1)
xs = np.linspace(gb.min(), gb.max(), 2)
plt.scatter(gb, rating, color="#2166ac")
plt.plot(xs, intercept + slope * xs, color="#d6604d", linewidth=2)
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Team ground-ball tendency (sd units)")
plt.ylabel("Fielder rating (sd units)")
plt.show()
