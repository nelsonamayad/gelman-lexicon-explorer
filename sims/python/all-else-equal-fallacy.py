# The "All Else Equal" Fallacy: a regression coefficient vs an intervention.
import numpy as np
import matplotlib.pyplot as plt

beta = 0.5    # direct effect of X on Y
delta = -1    # how Z responds to X
gamma = 0.8   # effect of Z on Y
rng = np.random.default_rng(17)


def simulate(shift):
    x = rng.normal(size=2000) + shift
    z = delta * x + rng.normal(size=2000)
    return x, z, beta * x + gamma * z + rng.normal(size=2000)


x, z, y = simulate(0)
X = np.column_stack([np.ones_like(x), x, z])
coef = np.linalg.lstsq(X, y, rcond=None)[0][1]  # "all else equal"
_, _, y_after = simulate(1)       # raise X by 1 and let Z respond
total = y_after.mean() - y.mean()

print(f"Regression coefficient (all else equal): {coef:.2f}")
print(f"Actual effect of raising X by 1: {total:.2f}")
print(f"Theory, beta + gamma * delta: {beta + gamma * delta:.2f}")

plt.barh(["Regression coefficient", "Actual effect"], [coef, total],
         color=["#2166ac", "#d6604d"])
plt.axvline(0, color="black", linewidth=0.8)
plt.xlim(-2.5, 2.5)
plt.xlabel("Change in Y")
plt.show()
