# Steelmanning: adopting X's framing of Y biases your view of Y.
import numpy as np
import matplotlib.pyplot as plt

w = 0.6     # how much the observer adopts X's framing
exag = 1    # how much X caricatures Y
rng = np.random.default_rng(142)

q_Y = rng.normal(size=500)                       # true quality of Y's work
direct = q_Y + rng.normal(0, 0.5, 500)           # the observer's own look
x_account = q_Y - exag + rng.normal(0, 0.5, 500)  # X's description of Y
view = (1 - w) * direct + w * x_account
print(f"On average the observer rates Y's work {np.mean(view - q_Y):.2f} "
      "relative to its true quality")

plt.scatter(q_Y, view, s=6, color="#d6604d")
lim = [q_Y.min(), q_Y.max()]
plt.plot(lim, lim, "k--")
plt.xlabel("True quality of Y's work")
plt.ylabel("Observer's view")
plt.show()
