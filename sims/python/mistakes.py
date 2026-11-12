# Mistakes: admitting and learning from them lowers the error rate.
import numpy as np
import matplotlib.pyplot as plt

base_rate = 0.25  # initial chance a project has an error
learning = 0.2    # error-rate reduction per lesson learned
rng = np.random.default_rng(96)


def run(learns):  # average cumulative mistakes, 200 careers of 50 projects
    totals = np.zeros((200, 50))
    for c in range(200):
        rate, total = base_rate, 0
        for t in range(50):
            if rng.uniform() < rate:
                total += 1
                if learns and rng.uniform() < 0.8:
                    rate *= 1 - learning
            totals[c, t] = total
    return totals.mean(axis=0)


learns, denies = run(True), run(False)
print(f"Mistakes after 50 projects: admits and learns {learns[-1]:.1f}, "
      f"denies and repeats {denies[-1]:.1f}")

t = np.arange(1, 51)
plt.plot(t, learns, color="#2166ac", linewidth=2, label="Admits and learns")
plt.plot(t, denies, color="#d6604d", linewidth=2, label="Denies and repeats")
plt.xlabel("Project")
plt.ylabel("Cumulative mistakes (average career)")
plt.legend()
plt.show()
