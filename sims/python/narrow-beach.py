# That narrow beach: where statistics beats eyeballing the data.
import numpy as np
import matplotlib.pyplot as plt

n = 30  # observations per decision
rng = np.random.default_rng(135)

# For each signal-to-noise ratio, 600 decisions about the sign of an effect
snr = 10 ** (-2 + np.arange(25) * 0.125)
eye, stat = [], []
for s in snr:
    sign = np.where(rng.uniform(size=600) < 0.5, 1, -1)
    y = rng.normal(sign[:, None] * s, 1, (600, n))
    glance = np.median(y[:, :3], axis=1)  # eyeball: a quick look at 3 points
    eye.append(np.mean(np.sign(glance) == sign))
    stat.append(np.mean(np.sign(y.mean(axis=1)) == sign))
eye, stat = np.array(eye), np.array(stat)
k = np.argmax(stat - eye)
print(f"Statistics helps most at signal/noise {snr[k]:.2g}: "
      f"{100 * stat[k]:.0f}% right vs {100 * eye[k]:.0f}% by eye")

plt.semilogx(snr, eye, color="#d6604d", linewidth=2, label="Eyeball")
plt.semilogx(snr, stat, color="#2166ac", linewidth=2, label="Statistics")
plt.ylim(0.5, 1)
plt.xlabel("Signal-to-noise ratio")
plt.ylabel("Share of correct decisions")
plt.legend()
plt.show()
