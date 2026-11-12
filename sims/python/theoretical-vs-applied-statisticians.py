# Theoretical and applied statisticians: model y given x, then transfer.
import numpy as np
import matplotlib.pyplot as plt

skew = 1   # how over-sampled high-x units are
slope = 1  # slope of y on x
rng = np.random.default_rng(12)

target_x = rng.normal(0, 1, 5000)   # the population we care about
x = rng.normal(skew, 1, 300)        # the sample over-represents high x
y = 2 + slope * x + rng.normal(size=300)
b, a = np.polyfit(x, y, 1)
print("True population mean of y: 2")
print(f"Sample mean of y: {y.mean():.2f}")
print(f"Regression, averaged over the population's x: "
      f"{np.mean(a + b * target_x):.2f}")

plt.scatter(x, y, s=6, color="0.5")
xs = np.array([-4, 4])
plt.plot(xs, a + b * xs, color="#2166ac", linewidth=2)
plt.plot(target_x[:600], np.full(600, y.min() - 0.5), "|", color="#d6604d")
plt.xlabel("x (red ticks: the population)")
plt.ylabel("y")
plt.show()
