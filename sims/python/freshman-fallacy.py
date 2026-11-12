# The Freshman Fallacy: an experiment on college students only.
import numpy as np
import matplotlib.pyplot as plt

gamma = -0.015  # change in the treatment effect per year of age
rng = np.random.default_rng(43)


def effect(age):
    return 0.5 + gamma * (age - 20)


age = rng.uniform(18, 22, 600)      # the experiment: ages 18 to 22
z = rng.binomial(1, 0.5, 600)       # randomized treatment
y = effect(age) * z + rng.normal(size=600)
est = y[z == 1].mean() - y[z == 0].mean()
pop_effect = effect(rng.uniform(18, 80, 5000)).mean()  # ages 18 to 80

print(f"Experiment's estimate: {est:.2f}")
print(f"Population-average effect: {pop_effect:.2f}")

ages = np.linspace(18, 80, 100)
plt.axvspan(18, 22, color="#2166ac", alpha=0.1)
plt.plot(ages, effect(ages), color="#2166ac", linewidth=2)
plt.axhline(est, color="#2166ac", linestyle="--")
plt.axhline(pop_effect, color="#d6604d", linestyle="--")
plt.xlabel("Age")
plt.ylabel("Treatment effect")
plt.show()
