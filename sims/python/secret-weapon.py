# The Secret Weapon: fit the same model to each year, then plot them all.
import numpy as np
import matplotlib.pyplot as plt

n_per_year = 300  # respondents per survey
trend = "Rising"  # or "Flat", "Rise and fall"
rng = np.random.default_rng(11)

years = np.arange(1972, 2025, 2)


def truth(yr):
    t = (yr - 1972) / 52
    return {"Rising": 0.1 + 0.5 * t, "Flat": 0.3 + 0 * t,
            "Rise and fall": 0.1 + 1.2 * t * (1 - t) * 1.6}[trend]


est, se = [], []
for year in years:
    x = rng.normal(size=n_per_year)
    y = 1 + truth(year) * x + rng.normal(size=n_per_year)
    (b, a), cov = np.polyfit(x, y, 1, cov="unscaled")
    resid = y - (a + b * x)
    est.append(b)
    se.append(np.sqrt(cov[0, 0] * resid @ resid / (n_per_year - 2)))
est, se = np.array(est), np.array(se)
inside = np.abs(est - truth(years)) <= se
print(f"{inside.sum()} of {len(years)} intervals (+/- 1 se) cover the "
      "true coefficient")

plt.errorbar(years, est, yerr=se, fmt="o", color="black")
plt.plot(years, truth(years), "--", color="#d6604d", linewidth=2)
plt.xlabel("Year")
plt.ylabel("Coefficient estimate")
plt.show()
