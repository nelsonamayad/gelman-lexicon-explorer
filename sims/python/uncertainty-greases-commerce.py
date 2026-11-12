# Uncertainty: it greases the wheels of commerce. An added error term
# lets a Metropolis sampler move.
import numpy as np
import matplotlib.pyplot as plt

tau = 0  # added error term; try 0.03
rng = np.random.default_rng(134)

x = np.arange(2, 21)
se = 0.003 * (1 + np.arange(19) / 3)     # very precise data
y = 2 - 0.15 * x + 0.004 * x ** 2 + rng.normal(0, se)  # slightly curved


def lp(a, b):
    return -0.5 * np.sum((y - a - b * x) ** 2 / (se ** 2 + tau ** 2))


def run(a, b):  # random-walk Metropolis
    l, acc, draws = lp(a, b), 0, []
    for _ in range(3000):
        a2, b2 = a + rng.normal(0, 0.02), b + rng.normal(0, 0.002)
        l2 = lp(a2, b2)
        if np.log(rng.uniform()) < l2 - l:
            a, b, l, acc = a2, b2, l2, acc + 1
        draws.append(b)
    return np.array(draws), acc / 3000


(b1, acc1), (b2, acc2) = run(1.5, -0.1), run(2.5, -0.05)
b_hat = np.mean(np.concatenate([b1[1500:], b2[1500:]]))
print(f"With tau = {tau}, the sampler accepts "
      f"{100 * (acc1 + acc2) / 2:.1f}% of proposals; fitted slope "
      f"{b_hat:.4f}")

plt.plot(b1, color="#2166ac")
plt.plot(b2, color="#d6604d")
plt.xlabel("Iteration")
plt.ylabel("Slope b")
plt.show()
