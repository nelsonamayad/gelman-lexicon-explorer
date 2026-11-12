# Mister P: multilevel regression and poststratification for state opinion.
import numpy as np
import matplotlib.pyplot as plt

n_total = 1200   # total sample size
old_share = 0.75  # share of the sample that is old
rng = np.random.default_rng(7)

S, age_gap = 50, 0.15                  # young support 15 points higher
base = 0.45 + rng.normal(0, 0.08, S)   # old-person support in each state
young_share = rng.uniform(0.3, 0.6, S)  # census share young
size = rng.lognormal(0, 0.8, S)         # relative population
truth = young_share * (base + age_gap) + (1 - young_share) * base

# Respondents: state proportional to size, age skewed old
state = rng.choice(S, n_total, p=size / size.sum())
young = (rng.uniform(size=n_total) > old_share).astype(float)
y = rng.binomial(1, np.clip(base[state] + age_gap * young, 0, 1))

# Step 1: common age effect, then partially pooled state intercepts
age_eff = y[young == 1].mean() - y[young == 0].mean()
n = np.bincount(state, minlength=S)
ok = n > 0
safe_n = np.maximum(n, 1)
raw = np.where(ok, np.bincount(state, y, S) / safe_n, np.nan)
resid = np.where(ok, np.bincount(state, y - age_eff * young, S) / safe_n,
                 np.nan)
mu = np.sum(resid[ok] * n[ok]) / n[ok].sum()
v = 0.25
tau2 = max(0.0005, np.mean((resid[ok] - mu) ** 2) - np.mean(v / n[ok]))
w = np.where(ok, tau2 / (tau2 + v / safe_n), 0)
old = mu + w * (np.where(ok, resid, mu) - mu)
# Step 2: poststratify with census age shares
mrp = young_share * (old + age_eff) + (1 - young_share) * old


def rmse(est):
    return np.sqrt(np.nanmean((est - truth) ** 2))


print(f"Error (RMSE, percentage points): raw state means "
      f"{100 * rmse(raw):.1f}, MRP {100 * rmse(mrp):.1f}")
print(f"States with no respondents: {np.sum(~ok)}")

plt.scatter(truth, raw, s=10 + 3 * n, facecolors="none", edgecolors="0.5",
            label="Raw state mean")
plt.scatter(truth, mrp, color="#2166ac", label="MRP")
plt.plot([0, 1], [0, 1], "k--")
plt.xlim(0.2, 0.9)
plt.ylim(0, 1)
plt.xlabel("True state support")
plt.ylabel("Estimate")
plt.legend()
plt.show()
