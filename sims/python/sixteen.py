# 16: you need 16 times the sample size to estimate an interaction.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

theta = 0.4      # main effect (in sd units)
int_ratio = 0.5  # interaction as a fraction of the main effect
rng = np.random.default_rng(80)

ns = [10, 20, 40, 80, 160, 320, 640, 1280]  # people per cell
gamma = int_ratio * theta
p_main, p_inter = [], []
for n in ns:
    # Cells (treatment a, group b); main effect theta, interaction gamma.
    # A cell mean of n draws is normal with sd 1 / sqrt(n).
    def cell(a, b):
        mu = theta * (a - 0.5) + gamma * (a - 0.5) * (b - 0.5)
        return rng.normal(mu, 1 / np.sqrt(n), 400)
    m00, m10, m01, m11 = cell(0, 0), cell(1, 0), cell(0, 1), cell(1, 1)
    main = ((m10 - m00) + (m11 - m01)) / 2
    inter = (m11 - m01) - (m10 - m00)
    p_main.append(np.mean(np.abs(main * np.sqrt(n)) > 1.96))
    p_inter.append(np.mean(np.abs(inter * np.sqrt(n) / 2) > 1.96))
q = NormalDist().inv_cdf
z = q(0.975) + q(0.8)
print(f"People per cell for 80% power: main effect "
      f"{np.ceil(z ** 2 / theta ** 2):.0f}, interaction "
      f"{np.ceil(z ** 2 * 4 / gamma ** 2):.0f}")

plt.semilogx(ns, p_main, "o-", color="#2166ac", label="Main effect")
plt.semilogx(ns, p_inter, "o-", color="#d6604d", label="Interaction")
plt.axhline(0.8, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("People per cell")
plt.ylabel("Power")
plt.legend()
plt.show()
