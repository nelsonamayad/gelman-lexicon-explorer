# Meritocracy won't happen: selection on merit turns into inheritance.
import numpy as np
import matplotlib.pyplot as plt

gamma = 2.5  # advantage passed on by elite status
noise = 0.7  # measurement noise in the merit score
rng = np.random.default_rng(128)

N = 3000
elite = np.zeros(N, dtype=bool)
inherited, merit_cor = [], []
for g in range(10):
    merit = rng.normal(size=N)
    score = merit + gamma * elite + rng.normal(0, noise, N)
    new_elite = score > np.sort(score)[::-1][int(N * 0.1)]
    inherited.append(0.1 if g == 0 else elite[new_elite].mean())
    merit_cor.append(np.corrcoef(new_elite.astype(float), merit)[0, 1])
    elite = new_elite

print(f"Generation 10: {100 * inherited[-1]:.0f}% of the elite had elite "
      "parents (10% = no inheritance)")
print(f"Correlation of elite status with true merit: generation 1 "
      f"{merit_cor[0]:.2f} | generation 10 {merit_cor[-1]:.2f}")

gens = np.arange(1, 11)
plt.plot(gens, inherited, "o-", color="#d6604d",
         label="Elite with elite parents")
plt.plot(gens, merit_cor, "o-", color="#2166ac",
         label="Correlation with merit")
plt.ylim(0, 1)
plt.xlabel("Generation")
plt.legend()
plt.show()
