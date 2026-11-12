# The One-Way Street Fallacy: an average effect hides effects in both
# directions.
import numpy as np
import matplotlib.pyplot as plt

mu = -0.2   # average effect
sigma = 1   # spread of individual effects
rng = np.random.default_rng(45)

tau = rng.normal(mu, sigma, 5000)  # each person's own effect
helped, hurt = tau[tau > 0], tau[tau <= 0]
print(f"Average effect: {tau.mean():.2f}")
print(f"{100 * helped.size / tau.size:.0f}% are helped (average "
      f"+{helped.mean():.2f}), {100 * hurt.size / tau.size:.0f}% are hurt "
      f"(average {hurt.mean():.2f})")

bins = np.linspace(tau.min(), tau.max(), 61)
plt.hist(hurt, bins=bins, color="#d6604d", label="Hurt")
plt.hist(helped, bins=bins, color="#2166ac", label="Helped")
plt.axvline(tau.mean(), color="black", linewidth=2)
plt.xlabel("Individual effect")
plt.ylabel("People")
plt.legend()
plt.show()
