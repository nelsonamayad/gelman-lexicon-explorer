# The Backseat Driver Principle: listen to criticism, even rude criticism.
import numpy as np
import matplotlib.pyplot as plt

precision = 0.25     # share of critiques that are correct
rude_correct = 0.6   # probability that a correct critique is rude
rng = np.random.default_rng(10)


def run(listen_to_all):
    errors, path = 12, [12]
    for _ in range(40):                   # one critique per round
        correct = errors > 0 and rng.uniform() < precision
        rude = rng.uniform() < (rude_correct if correct else 0.5)
        if correct and (listen_to_all or not rude):
            errors -= 1
        path.append(errors)
    return path


everyone, polite_only = run(True), run(False)
print(f"Errors left after 40 rounds: listens to everyone {everyone[-1]} "
      f"| ignores rude critics {polite_only[-1]}")

plt.step(range(41), everyone, color="#2166ac", label="Listen to everyone")
plt.step(range(41), polite_only, color="#d6604d",
         label="Ignore rude critics")
plt.xlabel("Round")
plt.ylabel("Errors left (of 12)")
plt.legend()
plt.show()
