# Premature collapsing of the wave function: decide with the uncertainty.
import numpy as np
import matplotlib.pyplot as plt

cost = 0.2  # cost of implementing an intervention
se = 0.4    # standard error of each study
rng = np.random.default_rng(152)

tau = 0.4
theta = rng.normal(0.1, tau, 5000)  # true effects of 5000 interventions
y = rng.normal(theta, se)           # one study of each
collapsed = np.where(np.abs(y / se) > 1.96, y, 0)  # significant, else 0
post = (0.1 / tau ** 2 + y / se ** 2) / (1 / tau ** 2 + 1 / se ** 2)

value = {"Collapse early (significance, then decide)": collapsed > cost,
         "Carry uncertainty to the decision": post > cost,
         "Oracle (knows the true effects)": theta > cost}
value = {k: np.sum((theta - cost)[act]) / 5000 for k, act in value.items()}
for k, v in value.items():
    print(f"{k}: {v:.3f}")

plt.barh(list(value), list(value.values()),
         color=["#d6604d", "#2166ac", "0.7"])
plt.xlabel("Average net value per intervention")
plt.tight_layout()
plt.show()
