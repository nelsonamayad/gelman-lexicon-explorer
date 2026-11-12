# Brilliance: an upper bound on the quality of reasoning, but no lower bound.
import numpy as np
import matplotlib.pyplot as plt

compromised = 0.3  # share compromised on this question
rng = np.random.default_rng(105)

B = rng.beta(2, 2, 1000)                      # brilliance
comp = rng.uniform(size=1000) < compromised   # motivated or out of field
M = np.where(comp, rng.beta(4, 1.5, 1000), rng.beta(1, 8, 1000))
Q = B * (1 - M)                               # quality of reasoning

top = B > 0.8
print(f"Of the {top.sum()} most brilliant thinkers (brilliance > 0.8), "
      f"{(Q[top] < 0.3).sum()} reason worse than 0.3 on this question")

plt.scatter(B, Q, s=6, c=np.where(comp, "#d6604d", "#2166ac"))
plt.plot([0, 1], [0, 1], "k--")  # brilliance is a ceiling
plt.xlabel("Brilliance")
plt.ylabel("Quality of reasoning on this question")
plt.show()
