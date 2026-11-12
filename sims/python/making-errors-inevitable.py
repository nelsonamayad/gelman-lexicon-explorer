# Making errors is inevitable; learning from them is not.
import numpy as np
import matplotlib.pyplot as plt

detect = 0.5  # probability an error is detected
report = 0.2  # probability a detected error is reported openly
rng = np.random.default_rng(136)


def run(q):  # error rate over 30 years, 100 analyses a year
    rate, path = 0.2, [0.2]
    for _ in range(30):
        u = rng.uniform(size=(3, 100))
        lessons = np.sum((u[0] < rate) & (u[1] < detect) & (u[2] < q))
        rate = max(0.01, rate * 0.97 ** lessons)  # each shared lesson helps
        path.append(rate)
    return path


paths = {"Your setting": run(report), "Every detected error reported": run(1),
         "Errors hidden": run(0)}
for (k, p), c in zip(paths.items(), ["#2166ac", "#4daf4a", "#d6604d"]):
    print(f"{k}: {100 * p[-1]:.1f}% after 30 years")
    plt.plot(p, color=c, linewidth=2, label=k)
plt.ylim(0, 0.22)
plt.xlabel("Year")
plt.ylabel("Share of analyses with an error")
plt.legend()
plt.show()
