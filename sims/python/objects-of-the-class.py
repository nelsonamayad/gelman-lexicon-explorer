# Objects of the class: broad, narrow, or partially pooled reference class.
import numpy as np
import matplotlib.pyplot as plt

n_narrow = 12   # members of the narrow class
gap_rate = 0.2  # how different the narrow class really is
rng = np.random.default_rng(141)

p_broad = 0.35
p_med = p_broad + gap_rate / 2
p_narrow = p_broad + gap_rate  # the rate we want to estimate
broad = rng.binomial(3000, p_broad, 2000) / 3000
medium = rng.binomial(300, p_med, 2000) / 300
narrow = rng.binomial(n_narrow, p_narrow, 2000) / n_narrow
w = n_narrow / (n_narrow + 25)  # shrink the narrow class toward medium
est = {"Broad": broad, "Medium": medium, "Narrow": narrow,
       "Partial pooling": w * narrow + (1 - w) * medium}
rmse = {k: np.sqrt(np.mean((v - p_narrow) ** 2)) for k, v in est.items()}
for k, v in rmse.items():
    print(f"{k}: RMSE {v:.3f}")

plt.bar(list(rmse), list(rmse.values()),
        color=["0.7", "0.7", "0.7", "#2166ac"])
plt.ylabel("Root mean squared error")
plt.show()
