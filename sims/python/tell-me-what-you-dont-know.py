# Tell Me What You Don't Know: asking about uncertainty widens intervals.
import numpy as np
import matplotlib.pyplot as plt

k = 0.5       # overconfidence factor (1 = calibrated)
prompt = 0.6  # how much the question helps
rng = np.random.default_rng(49)

k_after = k + prompt * (1 - k)
sigma = np.exp(rng.normal(0, 0.5, 200))  # real uncertainty of 200 questions
truth = rng.normal(0, sigma)             # error of the expert's best guess
cover_before = np.abs(truth) < 1.645 * k * sigma      # stated 90% interval
cover_after = np.abs(truth) < 1.645 * k_after * sigma  # after the question
print(f"Coverage of stated 90% intervals: initial "
      f"{100 * cover_before.mean():.0f}%, after \"tell me what you don't "
      f"know\" {100 * cover_after.mean():.0f}%")

q = np.arange(50)
plt.vlines(q, -1.645 * k_after * sigma[q], 1.645 * k_after * sigma[q],
           color="#2166ac", linewidth=3, label="After the question")
plt.vlines(q, -1.645 * k * sigma[q], 1.645 * k * sigma[q],
           color="#d6604d", linewidth=2, label="Initial")
plt.scatter(q, truth[q], s=10, color="black", zorder=3)
plt.xlabel("Question")
plt.ylabel("Error")
plt.legend()
plt.show()
