# Noem's Razor: when a pattern of convenient errors stops looking innocent.
import numpy as np
import matplotlib.pyplot as plt

prior = 0.05  # prior probability of malice (charitable)
truth = "Motivated distortion"  # or "Honest mistakes"
rng = np.random.default_rng(150)

# Each error either favors the person's side or not. Honest mistakes favor
# them half the time; motivated distortion 90% of the time.
p_fav = 0.5 if truth == "Honest mistakes" else 0.9
fav = rng.uniform(size=15) < p_fav
steps = np.where(fav, np.log(0.9 / 0.5), np.log(0.1 / 0.5))
log_odds = np.log(prior / (1 - prior)) + np.cumsum(steps)
belief = np.concatenate([[prior], 1 / (1 + np.exp(-log_odds))])
print(f"{fav.sum()} of 15 errors favored their side; belief in malice "
      f"rises from {100 * prior:.0f}% to {100 * belief[-1]:.0f}%")

plt.plot(belief, "-", color="#d6604d")
plt.scatter(np.arange(1, 16)[fav], belief[1:][fav], color="#d6604d",
            label="Error favored their side")
plt.axhline(0.5, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("Errors observed")
plt.ylabel("Probability of malice")
plt.legend()
plt.show()
