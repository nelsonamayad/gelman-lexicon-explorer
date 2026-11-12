# The Paradox of Influence: pander more, get heeded more, add less.
import numpy as np
import matplotlib.pyplot as plt

my_w = 0.7  # how much you pander (w)
rng = np.random.default_rng(68)

truth, pref = rng.normal(size=(2, 3000))  # what's right; what boss wants
signal = truth + rng.normal(0, 0.5, 3000)  # your honest read
w = np.arange(21) / 20
heeded = 0.2 + 0.75 * w                    # pandering gets you listened to
info = []
for wk in w:
    advice = (1 - wk) * signal + wk * pref
    resid = advice - wk * pref             # what the boss didn't know
    r = np.corrcoef(resid, truth)[0, 1] if wk < 1 else 0
    info.append(max(0, r) * (1 - wk))
impact = heeded * np.array(info)
me, best = np.argmin(np.abs(w - my_w)), np.argmax(impact)
print(f"At w = {my_w}: heeded {100 * heeded[me]:.0f}%, impact "
      f"{impact[me]:.2f}")
print(f"Impact is largest at w = {w[best]} ({impact[best]:.2f})")

plt.plot(w, heeded, color="0.5", linewidth=2, label="Heeded")
plt.plot(w, info, color="#2166ac", linewidth=2, label="Information added")
plt.plot(w, impact, color="#d6604d", linewidth=2, label="Real impact")
plt.xlabel("How much you pander (w)")
plt.legend()
plt.show()
