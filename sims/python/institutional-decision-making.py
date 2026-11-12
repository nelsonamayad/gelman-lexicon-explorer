# Institutional decision making: when to test homes for radon.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

test_cost = 50   # cost of a test ($)
fix_cost = 1500  # cost of remediation ($)
benefit = 700    # health value per unit of radon removed ($)
rng = np.random.default_rng(5)

s = 0.6                               # model's predictive sd (log scale)
pred = rng.normal(0.4, 0.7, 2000)     # predicted log radon for each home
level = np.exp(rng.normal(pred, s))   # true radon level


def gain(lv):        # test first, fix only if worth it
    return np.maximum(0, benefit * (lv - 1) - fix_cost)


def fix_gain(lv):    # fix without testing
    return benefit * np.maximum(0, lv - 1) - fix_cost


# Expected values over each home's predictive distribution (grid over z)
z = np.arange(-4, 4.001, 0.05)
wz = np.array([NormalDist().pdf(v) for v in z]) * 0.05
L = np.exp(pred[:, None] + s * z[None, :])
e_fix = benefit * (np.maximum(0, L - 1) @ wz) - fix_cost
e_test = gain(L) @ wz - test_cost
best = np.maximum(0, np.maximum(e_fix, e_test))
decision = np.where(best == 0, 0, np.where(best == e_fix, fix_gain(level),
                                           gain(level) - test_cost))
per_home = {"Do nothing": 0, "Remediate all": fix_gain(level).mean(),
            "Test all": (gain(level) - test_cost).mean(),
            "Decision analysis": decision.mean()}
for k, v in per_home.items():
    print(f"{k}: {v:.0f} dollars per home")

plt.barh(list(per_home), list(per_home.values()),
         color=["0.7", "0.7", "0.7", "#2166ac"])
plt.xlabel("Net value per home ($)")
plt.tight_layout()
plt.show()
