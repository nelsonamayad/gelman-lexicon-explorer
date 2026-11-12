# As They Say in the Stagecoach Business: remove the padding and the ride
# gets rough. How much smoothing helps you read the signal?
import numpy as np
import matplotlib.pyplot as plt

padding = 1  # smoothing window (odd number of points)
rng = np.random.default_rng(28)

n = 200
i = np.arange(n)
msg = np.sin(i / 18) + 0.5 * np.sin(i / 7)  # the message
obs = msg + rng.normal(0, 0.6, n)           # what arrives


def smooth(w):
    h = (w - 1) // 2
    return np.array([obs[max(0, k - h):min(n, k + h + 1)].mean()
                     for k in i])


def err(w):
    return np.sqrt(np.mean((smooth(w) - msg) ** 2))


widths = range(1, 62, 2)
best = min(widths, key=err)
print(f"Error with padding {padding}: {err(padding):.3f}")
print(f"Best padding: {best} (error {err(best):.3f})")

plt.scatter(i, obs, s=6, color="0.7")
plt.plot(i, msg, "k--", linewidth=2, label="Message")
plt.plot(i, smooth(padding), color="#2166ac", linewidth=2, label="Reader")
plt.xlabel("Time")
plt.ylabel("Signal")
plt.legend()
plt.show()
