# The Javert Paradox: persistent enough to work, not so much as to be Javert.
import numpy as np
import matplotlib.pyplot as plt

responsiveness = 0.06  # how much each push moves the authors
tolerance = 4          # pushes the community tolerates before "obsessive"
# Deterministic: no random numbers.

pushes = np.arange(21)
corrected = 1 - np.exp(-responsiveness * pushes ** 2 / 4)  # chance of a fix
obsessive = 1 / (1 + np.exp(-(pushes - tolerance)))       # seen as Javert
sweet = pushes[(corrected > 0.5) & (obsessive < 0.5)]

if sweet.size:
    print(f"Sweet spot: {sweet.min()} to {sweet.max()} pushes")
else:
    print("No persistence level works without looking like Javert")

plt.plot(pushes, corrected, color="#2166ac", linewidth=2,
         label="Error gets corrected")
plt.plot(pushes, obsessive, color="#d6604d", linewidth=2,
         label="Critic seen as obsessive")
plt.axhline(0.5, color="black", linestyle="--")
plt.xlabel("Times the critic pushes")
plt.ylabel("Probability")
plt.legend()
plt.show()
