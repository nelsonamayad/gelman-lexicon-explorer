# Basketball, or knitting: judging scatterplots is learned by practice.
import numpy as np
import matplotlib.pyplot as plt

true_r = 0.4  # correlation when the pattern is real
lr = 0.01     # how quickly feedback adjusts judgment
rng = np.random.default_rng(98)

real = rng.uniform(size=300) < 0.5
r_obs = []
for is_real in real:
    rho = true_r if is_real else 0
    x = rng.normal(size=20)
    y = rho * x + np.sqrt(1 - rho ** 2) * rng.normal(size=20)
    r_obs.append(abs(np.corrcoef(x, y)[0, 1]))
threshold = 0.05  # the learner starts by seeing patterns everywhere
rules = 0.05      # the rules-only learner never adjusts
feedback_ok, rules_ok = [], []
for r, is_real in zip(r_obs, real):
    says = r > threshold
    feedback_ok.append(says == is_real)
    rules_ok.append((r > rules) == is_real)
    if says != is_real:
        threshold += lr if says else -lr
feedback_ok, rules_ok = np.array(feedback_ok), np.array(rules_ok)

print(f"Accuracy in the last 100 judgments: with feedback "
      f"{100 * feedback_ok[200:].mean():.0f}%, rules only "
      f"{100 * rules_ok[200:].mean():.0f}% (chance: 50%)")

blocks = np.arange(1, 16)
plt.plot(blocks, feedback_ok.reshape(15, 20).mean(axis=1), "o-",
         color="#2166ac", label="Practice with feedback")
plt.plot(blocks, rules_ok.reshape(15, 20).mean(axis=1), "o-",
         color="#d6604d", label="Read the rules only")
plt.axhline(0.5, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("Block of 20 judgments")
plt.ylabel("Accuracy")
plt.legend()
plt.show()
