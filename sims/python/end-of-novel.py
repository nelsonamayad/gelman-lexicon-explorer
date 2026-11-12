# End of novel. Beginning of job: when to stop thinking and start finishing.
import numpy as np
import matplotlib.pyplot as plt

tau = 6   # time scale of insight (weeks)
cost = 2  # cost of delay per week
# Deterministic: no random numbers.

t = np.arange(0, 40.001, 0.25)
value = 100 * (1 - np.exp(-t / tau))  # value of the analysis after t weeks
net = value - cost * t
t_star = max(0, tau * np.log(100 / (cost * tau)))  # where gains = cost

print(f"Stop thinking and start finishing after about {t_star:.1f} weeks,")
print(f"when the analysis has reached "
      f"{100 * (1 - np.exp(-t_star / tau)):.0f}% of its potential value")

plt.plot(t, value, color="#2166ac", linewidth=2,
         label="Value of the analysis")
plt.plot(t, net, color="#d6604d", linewidth=2,
         label="Value minus cost of delay")
plt.axvline(t_star, color="black", linestyle="--")
plt.xlabel("Weeks of thinking")
plt.ylabel("Value")
plt.legend()
plt.show()
