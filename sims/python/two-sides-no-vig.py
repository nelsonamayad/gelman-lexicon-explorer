# Two sides, no vig: a theory that bets on both outcomes risks nothing.
import numpy as np
import matplotlib.pyplot as plt

true_effect = 0  # true effect
rng = np.random.default_rng(137)

z = rng.normal(true_effect / 0.2, 1, 30)  # 30 studies
noticed = np.abs(z) > 1                   # a "noticeable" result
committed_conf = np.cumsum(noticed & (z > 0))  # predicted positive
two_sided_conf = np.cumsum(noticed)            # either sign "confirms" it
# Evidence for the committed theory: it predicts a positive result with
# probability 0.8, against 0.5 with no theory. The two-sided theory
# predicts both signs, so its evidence never moves from 50%.
lo = np.cumsum(np.where(noticed, np.where(z > 0, np.log(0.8 / 0.5),
                                          np.log(0.2 / 0.5)), 0))
p_committed = 1 / (1 + np.exp(-lo))
print(f"After 30 studies: 'confirmations' two-sided {two_sided_conf[-1]}, "
      f"committed {committed_conf[-1]}")
print(f"Probability the theory is right: two-sided 50%, committed "
      f"{100 * p_committed[-1]:.0f}%")

k = np.arange(1, 31)
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].step(k, two_sided_conf, color="#d6604d", label="Two-sided")
ax[0].step(k, committed_conf, color="#2166ac", label="Committed")
ax[0].set_ylabel("'Confirmations'")
ax[0].legend()
ax[1].plot(k, p_committed, color="#2166ac", linewidth=2)
ax[1].axhline(0.5, color="#d6604d", linewidth=2)
ax[1].set_ylim(0, 1)
ax[1].set_ylabel("Probability theory is right")
plt.show()
