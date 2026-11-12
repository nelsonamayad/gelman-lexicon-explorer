# A picture plus 1000 words: the same scatterplot, with and without words.
import numpy as np
import matplotlib.pyplot as plt

words = True  # add grouping and annotation
rng = np.random.default_rng(73)

# Three clinics: within each, more dose means a better outcome
k = np.repeat([0, 1, 2], 60)
x = rng.normal(2 + 2.5 * k, 0.8)
y = 10 - 3 * k + 1.2 * (x - 2 - 2.5 * k) + rng.normal(0, 0.7, 180)

overall = np.polyfit(x, y, 1)
X = np.column_stack([x, k == 0, k == 1, k == 2])
within = np.linalg.lstsq(X, y, rcond=None)[0][0]
print(f"Slope ignoring clinics: {overall[0]:.2f}")
print(f"Slope within clinics: {within:.2f}")

cols = np.array(["#2166ac", "#d6604d", "#1a9850"])
plt.scatter(x, y, c=cols[k] if words else "0.25", s=12)
xs = np.linspace(x.min(), x.max(), 2)
plt.plot(xs, np.polyval(overall, xs), "k--")
if words:
    for j, name in enumerate(["Clinic A", "Clinic B", "Clinic C"]):
        fit = np.polyfit(x[k == j], y[k == j], 1)
        xj = np.array([x[k == j].min(), x[k == j].max()])
        plt.plot(xj, np.polyval(fit, xj), color=cols[j], linewidth=2,
                 label=name)
    plt.text(7.5, 9.5, "Within each clinic,\nmore dose -> better outcome")
    plt.legend()
plt.xlabel("Dose")
plt.ylabel("Outcome")
plt.show()
